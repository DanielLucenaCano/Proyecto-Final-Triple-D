# Arquitectura

## Estado

Arquitectura de referencia para el despliegue **en contenedores Docker**
(sustituye al modelo inicial de "1 VM + servicios systemd"). Se ampliará en
iteraciones siguientes a medida que se incorporen hosts adicionales (ver
`config/agents/README.md`).

## Topología del laboratorio

Despliegue mediante **Docker Compose**: cada componente de Zabbix corre en
su propio contenedor, conectados entre sí por una red interna (`zabbix-net`)
y resolviéndose por nombre de servicio (no por IP fija de una VM). La
definición completa está en [`docker-compose.yml`](../docker-compose.yml)
(raíz del proyecto).

```text
                    Navegador (admin/operador)
                              |
                              | HTTP :${WEB_PORT} (host) -> :8080 (contenedor)
                              v
   +------------------------------------------------------------------+
   |  Host Docker  (red "zabbix-net", bridge)                         |
   |                                                                   |
   |   +----------------+   :8080    +-------------------------+      |
   |   | zabbix-web     |<-----------| navegador (publicado)   |      |
   |   | (apache+php)   |            +-------------------------+      |
   |   +-------+--------+                                             |
   |           | DB_SERVER_HOST=mysql-server (:3306, red interna)     |
   |           v                                                      |
   |   +----------------+        +----------------------------+      |
   |   | mysql-server   |<-------| zabbix-server              |      |
   |   | (MariaDB)      | :3306  | (zabbix-server-mysql)      |      |
   |   | vol: db_data   |        | vol: alertscripts/external |      |
   |   +----------------+        +-------------+--------------+      |
   |                                            | :10051 (publicado)  |
   |                                            v                     |
   |                              +----------------------------+      |
   |                              | zabbix-agent (agent2)      |      |
   |                              | :10050 (publicado)         |      |
   |                              +----------------------------+      |
   +------------------------------------------------------------------+
                              ^
                              | (futuro) agentes en otros hosts/contenedores
                              | conectan a :10051 del host Docker
                              v
                    Hosts monitorizados (config/agents/)
```

## Componentes

| Componente | Imagen Docker | Función | Puerto publicado |
|---|---|---|---|
| Zabbix Server | `zabbix/zabbix-server-mysql` | Recolecta, procesa y evalúa datos de monitorización (triggers, eventos, acciones) | `10051/tcp` |
| Frontend web | `zabbix/zabbix-web-apache-mysql` | Interfaz de administración y visualización (dashboards, hosts, plantillas); incluye Apache+PHP | `${WEB_PORT}/tcp` -> `8080` interno |
| Base de datos | `mariadb:10.11` | Almacena configuración, históricos y tendencias (BD `zabbix`, usuario `zabbix`) | `3306/tcp` (solo red interna `zabbix-net`, no publicado) |
| Agente | `zabbix/zabbix-agent2` | Recoge métricas del host monitorizado (CPU, memoria, disco, procesos) | `10050/tcp` |
| Inicializador | `mariadb:10.11` (cliente) | Contenedor *one-shot* (`zabbix-init`, no expone nada): corrige por SQL la interfaz del agente del host `Zabbix server` precargado por la imagen oficial — ver `scripts/fix-agent-interface.sh` | — |

Volúmenes con nombre (persistencia, gestionados por Docker): `db_data`
(datos de MariaDB), `zbx_alertscripts` y `zbx_externalscripts` (scripts
personalizados del servidor).

## Hosts monitorizados y flujo de datos

**Iteración actual**: un único host visible en Zabbix, `Zabbix server`
(el contenedor `zabbix-agent`, configurado con `ZBX_HOSTNAME` desde `.env`).

> **Nota sobre la interfaz del agente**: la imagen oficial precarga este host
> con su interfaz de agente apuntando a `127.0.0.1:10050` (asume servidor y
> agente en la misma máquina). Como aquí cada uno vive en su propio
> contenedor, el servicio `zabbix-init` la redirige automáticamente por DNS
> a `zabbix-agent` la primera vez que se levanta el stack — ver
> `scripts/fix-agent-interface.sh`. Si alguna vez ves el problema "Zabbix
> agent is not available" tras un `down -v` (que borra los volúmenes), basta
> con `docker compose up -d`: el inicializador lo vuelve a corregir solo.

Flujo de una métrica típica (p. ej. uso de CPU):

1. El contenedor `zabbix-agent` recoge el valor.
2. Lo envía de forma activa al Zabbix Server (`ZBX_SERVER_HOST=zabbix-server`,
   resolución por nombre de servicio dentro de `zabbix-net`) o responde a
   consultas pasivas — ver `config/agents/`.
3. El contenedor `zabbix-server` evalúa el valor frente a los items/triggers
   definidos en las plantillas vinculadas al host (ver `config/templates/`).
4. Si se supera un umbral, se genera un **problema/evento** con la
   severidad correspondiente (`Warning`, `High`/`Critical`), conforme a
   `docs/politicas-monitorizacion.md`.
5. El resultado (histórico, tendencias, problemas activos) se almacena en
   `mysql-server` (volumen `db_data`) y se visualiza en `zabbix-web`
   (`Monitoring -> Latest data`, `Monitoring -> Problems`, dashboards).

**Crecimiento previsto**: cada host adicional (físico, VM o contenedor) que
se quiera monitorizar añade un agente que se conecta al Zabbix Server por el
puerto `10051` publicado en el host Docker (modo activo) o `10050` (modo
pasivo). El procedimiento de alta está documentado en
`config/agents/README.md`.

## Consideraciones de red, puertos y dependencias

- **Tráfico de administración**: navegador -> `http://<host-docker>:${WEB_PORT}`,
  mapeado al puerto interno `8080` de `zabbix-web`. Si se requiere HTTPS,
  debe añadirse como mejora futura (proxy inverso con TLS delante del stack).
- **Tráfico de monitorización**: `10051/tcp` (servidor) y `10050/tcp`
  (agente) se publican en el host Docker para permitir agentes externos.
  Entre los contenedores del propio stack, la comunicación va por la red
  interna `zabbix-net` y no necesita publicarse.
- **Base de datos**: `3306/tcp` solo accesible dentro de `zabbix-net`
  (`DB_SERVER_HOST=mysql-server`); no se publica al host ni a la red externa.
- **Dependencias de arranque**: gestionadas declarativamente por Compose con
  `depends_on` + `healthcheck` — `mysql-server` debe estar `healthy` antes de
  que arranquen `zabbix-server` y `zabbix-web`; `zabbix-server` debe estar
  iniciado antes de `zabbix-web`. No requiere intervención manual (a
  diferencia del orden `MariaDB -> Apache -> zabbix-server -> frontend` que
  exigía el despliegue sobre VM).
- **Resolución de nombres**: el `ZBX_HOSTNAME` definido en `.env` debe
  coincidir exactamente con el nombre del host dado de alta en
  **Data collection -> Hosts** del frontend; de lo contrario el agente
  aparecerá como inalcanzable aunque el contenedor esté en ejecución.
- **Persistencia**: toda la información sobrevive a un `docker compose down`
  gracias a los volúmenes con nombre. Solo `docker compose down -v` destruye
  los datos — usarlo únicamente para un reinicio completo del laboratorio.
