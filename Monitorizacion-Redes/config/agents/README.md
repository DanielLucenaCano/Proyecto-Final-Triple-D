# config/agents/

Notas y procedimiento para los agentes Zabbix de los hosts monitorizados
del laboratorio.

## Contenido

Con el despliegue en Docker, la configuración del agente local
(`zabbix-agent`, imagen `zabbix/zabbix-agent2`) ya **no se gestiona editando
un fichero `.conf`**: se define mediante variables de entorno en
[`.env`](../../.env.example) (`ZBX_HOSTNAME`, `ZBX_SERVER_HOST`) dentro de
[`docker-compose.yml`](../../docker-compose.yml). No es necesario versionar
ningún `.snippet` de configuración para este agente.

Este directorio queda como referencia para documentar el **alta de nuevos
hosts monitorizados** (físicos, VMs o contenedores ajenos al stack).

## Cómo añadir un nuevo host monitorizado

1. Instala un agente Zabbix 7.4 en el host a monitorizar:
   - **Host con Docker**: ejecuta el contenedor oficial, p. ej.
     `docker run -d --name zabbix-agent --restart unless-stopped \
     -e ZBX_HOSTNAME=<nombre-host> -e ZBX_SERVER_HOST=<IP-del-host-Zabbix> \
     -p 10050:10050 zabbix/zabbix-agent2:alpine-7.4-latest`
   - **Host sin Docker**: instala `zabbix-agent2` desde el repositorio
     oficial de Zabbix para esa distribución y ajusta `Server`,
     `ServerActive` y `Hostname` en `/etc/zabbix/zabbix_agent2.conf`.
2. Asegúrate de que `Hostname`/`ZBX_HOSTNAME` coincide **exactamente** con
   el nombre que usarás al dar de alta el host en el frontend.
3. Verifica que el host tiene visibilidad de red hacia el puerto `10051`
   publicado por el contenedor `zabbix-server` (modo activo) o que el
   `zabbix-server` puede alcanzar el `10050` del nuevo host (modo pasivo).
4. Da de alta el host en **Data collection -> Hosts** del frontend, con el
   mismo nombre y la IP/hostname accesible.
5. Vincula la plantilla correspondiente (ver `config/templates/`) y verifica
   en **Monitoring -> Latest data** que empiezan a llegar métricas.
6. Documenta el alta (host, IP, plantilla aplicada, fecha) en
   `docs/arquitectura.md` y guarda evidencia en `docs/evidencias/`.
