# Scripts de Comprobación

Chequeos personalizados que extienden la recolección estándar de Zabbix
(plantilla `Linux by Zabbix agent`) con métricas e indicadores propios del
laboratorio — la "personalización y desarrollo de scripts" de la Fase 5
del guion.

## Inventario

| Script | Qué comprueba | Por qué hace falta (no lo cubre la plantilla estándar) |
|---|---|---|
| [`check_tcp_port.sh`](./check_tcp_port.sh) | Si un puerto TCP de un host/servicio está abierto y el tiempo de conexión (ms) | La plantilla `Linux by Zabbix agent` mide recursos del SO (CPU/memoria/disco), no la disponibilidad de **servicios concretos** ni de **dispositivos de red simulados** que se añadan al laboratorio (ver `config/agents/README.md`). Un único chequeo genérico parametrizable cubre cualquier servicio TCP sin duplicar scripts. |
| [`check_log_errors.sh`](./check_log_errors.sh) | Nº de líneas que coinciden con un patrón de error en un log, dentro de una ventana temporal | Detecta problemas **funcionales** (errores de aplicación, fallos de autenticación) que no se reflejan en métricas de sistema — complementa la vigilancia de "capacidad" con vigilancia de "salud funcional". |

Ambos siguen el mismo contrato de salida: texto simple en stdout, apto
para que Zabbix lo recoja directamente como valor de un item (sin
necesidad de parsers adicionales en el servidor).

## Cómo integrarlos en Zabbix agent2 (UserParameters)

Los `UserParameter` permiten que el agente ejecute un script local y
reporte su salida como si fuera un item nativo. Pasos para activarlos en
el contenedor `zabbix-agent` (imagen `zabbix/zabbix-agent2`):

1. **Monta los scripts y un fichero de configuración adicional** en el
   contenedor del agente. La forma más limpia con Docker Compose es añadir
   un volumen y una variable de entorno en `docker-compose.yml`:

   ```yaml
   zabbix-agent:
     # ...
     environment:
       ZBX_HOSTNAME: ${ZBX_HOSTNAME}
       ZBX_SERVER_HOST: zabbix-server
       ZBX_USERPARAMETERS: /etc/zabbix/zabbix_agent2.d/userparameters.conf
     volumes:
       - ./scripts/checks:/etc/zabbix/scripts:ro
       - ./config/zabbix/userparameters.conf:/etc/zabbix/zabbix_agent2.d/userparameters.conf:ro
   ```

   > La imagen oficial carga automáticamente cualquier fichero `.conf` en
   > `/etc/zabbix/zabbix_agent2.d/` mediante `Include=` — no es obligatorio
   > usar `ZBX_USERPARAMETERS`, pero documentarlo deja explícito qué
   > fichero define los chequeos personalizados.

2. **Crea `config/zabbix/userparameters.conf`** con la declaración de cada
   chequeo (sintaxis `UserParameter=clave[*],comando`):

   ```ini
   # Comprueba el puerto 8080 del propio frontend (demuestra el mecanismo;
   # en un laboratorio ampliado, $1/$2/$3 apuntarían a otros servicios/hosts)
   UserParameter=lab.tcp.check[*],sh /etc/zabbix/scripts/check_tcp_port.sh $1 $2 $3

   # Cuenta errores recientes en el log del propio servidor Zabbix
   UserParameter=lab.log.errors[*],sh /etc/zabbix/scripts/check_log_errors.sh $1 "$2" $3
   ```

3. **Reinicia el agente** (`docker compose up -d zabbix-agent`) y
   comprueba que el agente reconoce los parámetros:
   ```bash
   docker compose exec zabbix-agent zabbix_agent2 -t "lab.tcp.check[zabbix-web,8080,2]"
   ```
4. **Da de alta los items en Zabbix** (Data collection → Hosts →
   `Zabbix server` → Items → Create item):
   - *Type*: `Zabbix agent`.
   - *Key*: `lab.tcp.check[zabbix-web,8080,2]` (o la combinación deseada).
   - *Type of information*: `Text` (para `check_tcp_port.sh`, que devuelve
     `status=up;latency_ms=N`) o `Numeric (unsigned)` para
     `check_log_errors.sh`.
5. **Crea triggers** sobre esos items siguiendo el mismo criterio que
   `docs/politicas-monitorizacion.md` (ventanas temporales, severidades
   `Warning`/`High`), por ejemplo:
   - `find(/Zabbix server/lab.tcp.check[zabbix-web,8080,2],,"like","status=down")=1`
     → "Servicio zabbix-web inaccesible en {HOST.NAME}" (`High`).
   - `last(/Zabbix server/lab.log.errors[/var/log/zabbix/zabbix_server.log,ERROR,300])>5`
     → "Repunte de errores en el log de Zabbix Server" (`Warning`).

## Pruebas locales (sin desplegar en Zabbix)

Ambos scripts se pueden ejecutar de forma independiente para verificar su
salida antes de integrarlos:

```bash
sh check_tcp_port.sh zabbix-web 8080
# status=up;latency_ms=8

sh check_log_errors.sh /var/log/zabbix/zabbix_server.log "ERROR|CRITICAL" 300
# 0
```

Documenta en `docs/evidencias/` la salida de estas pruebas y, si llegas a
vincular los items/triggers en el frontend, una captura de
**Data collection → Hosts → Items** mostrando los chequeos personalizados
junto a los nativos de la plantilla estándar.
