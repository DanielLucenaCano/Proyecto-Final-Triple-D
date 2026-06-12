# config/zabbix/

Configuración adicional del agente Zabbix que va más allá de las
variables de entorno de `docker-compose.yml`/`.env` — concretamente, la
declaración de **chequeos personalizados (UserParameters)** desarrollados
en [`scripts/checks/`](../../scripts/checks/) (Fase 5 del guion).

## Contenido

- [`userparameters.conf.example`](./userparameters.conf.example) — plantilla
  con la sintaxis `UserParameter=clave[*],comando` para los scripts
  `check_tcp_port.sh` y `check_log_errors.sh`. Cópiala a
  `userparameters.conf` (excluido de Git, igual que `.env`) para activarla.

## Por qué es un fichero `.example`

Igual que `.env.example`, este fichero es la plantilla versionada; la
copia activa (`userparameters.conf`) puede variar según qué chequeos
decida activar cada despliegue del laboratorio (por ejemplo, distintos
hosts/puertos a comprobar), y no debería forzar un único conjunto fijo
para todo el mundo.

## Procedimiento de integración completo

Ver [`scripts/checks/README.md`](../../scripts/checks/README.md) — incluye
los cambios necesarios en `docker-compose.yml` (montaje de volúmenes), el
alta de items en el frontend y ejemplos de triggers coherentes con
`docs/politicas-monitorizacion.md`.
