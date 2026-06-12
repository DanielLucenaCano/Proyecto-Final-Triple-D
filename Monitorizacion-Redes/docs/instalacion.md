# Instalación

## Alcance

La instalación del proyecto se basa en **Zabbix 7.4** desplegado con
**Docker Compose**, usando las imágenes oficiales de Zabbix
(`zabbix-server-mysql`, `zabbix-web-apache-mysql`, `zabbix-agent2`) y
**MariaDB** como backend de base de datos. Este enfoque sustituye al
despliegue inicial sobre una VM con `systemd`/`apt`: ya no se requiere una
máquina virtual dedicada, instalación de paquetes del sistema operativo ni
gestión manual de servicios — todo el stack se levanta y se destruye con
Docker Compose, lo que lo hace mucho más accesible y reproducible (en un
portátil, en un servidor o en un laboratorio compartido).

## Requisitos previos

- Docker Engine y el plugin Docker Compose (`docker compose version`).
- Puertos libres en el host: `8080` (frontend web, configurable), `10051`
  (Zabbix Server) y `10050` (agente).

## Pasos de instalación

1. Copia el fichero de variables de entorno y ajústalo:

   ```bash
   cp .env.example .env
   # edita .env: ZBX_HOSTNAME, ZBX_TIMEZONE, WEB_PORT, DB_*
   ```

   **Importante**: cambia `DB_PASS` y `DB_ROOT_PASS` antes de desplegar.
   `.env` está excluido de Git (ver `.gitignore`); solo `.env.example` se
   versiona.

2. Levanta el stack:

   ```bash
   docker compose up -d
   ```

   Docker Compose descarga las imágenes oficiales, crea la red `zabbix-net`,
   los volúmenes con nombre (`db_data`, `zbx_alertscripts`,
   `zbx_externalscripts`) y arranca los servicios en orden
   (`mysql-server` → `zabbix-server` → `zabbix-web` / `zabbix-agent`),
   respetando las dependencias (`depends_on` + `healthcheck`).

   Además se ejecuta automáticamente el servicio **`zabbix-init`**
   (one-shot): corrige la interfaz del agente del host `Zabbix server`
   —que la imagen oficial precarga apuntando a `127.0.0.1`, asumiendo
   servidor y agente en la misma máquina— para que apunte al contenedor
   real `zabbix-agent` por DNS. Sin este paso, el frontend mostraría el
   problema "Zabbix agent is not available" hasta corregirlo a mano. El
   script es idempotente (`scripts/fix-agent-interface.sh`): en arranques
   posteriores detecta que ya está bien configurado y no hace nada.

3. Comprueba que los contenedores están arriba y sanos:

   ```bash
   docker compose ps
   docker compose logs -f zabbix-server
   ```

4. Accede al asistente web en `http://localhost:${WEB_PORT}` (por defecto
   `http://localhost:8080`). Credenciales iniciales: `Admin` / `zabbix`.
   **Cambia la contraseña del usuario `Admin`** nada más entrar — es el
   mismo paso que en el despliegue tradicional sobre VM.

5. Verifica en **Monitoring -> Latest data** que el host `Zabbix server`
   (agente local, contenedor `zabbix-agent`) está enviando métricas.

## Resultado esperado

Al finalizar el despliegue deben quedar validados los siguientes puntos:

- `docker compose ps` muestra los 4 servicios en estado `running`/`healthy`.
- Asistente web accesible en `http://localhost:${WEB_PORT}/`.
- Contraseña de `Admin` cambiada.
- Host `Zabbix server` visible y enviando datos en **Monitoring -> Latest data**.
- Puertos `10051` (servidor) y `10050` (agente) escuchando en el host.

## Evidencias mínimas a capturar

- Salida de `docker compose ps`.
- Salida de `docker compose logs zabbix-server` (arranque sin errores de BD).
- Captura de la pantalla de login o del asistente inicial de Zabbix.
- Salida de `ss -lntp | grep -E '10051|10050|8080'` (puertos publicados).

## Operación habitual

```bash
docker compose stop          # detener sin perder datos (volúmenes persisten)
docker compose start         # reanudar
docker compose down          # detener y eliminar contenedores (mantiene volúmenes)
docker compose down -v       # ¡destruye también los volúmenes! solo para reset total
docker compose pull && docker compose up -d   # actualizar a una imagen más reciente
```

## Referencia

La definición completa del stack está en
[`docker-compose.yml`](../docker-compose.yml) (raíz del proyecto) y las
variables de entorno en [`.env.example`](../.env.example). El detalle de la
topología y el flujo de datos entre contenedores está documentado en
[`docs/arquitectura.md`](./arquitectura.md).
