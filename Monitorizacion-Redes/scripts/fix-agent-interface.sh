#!/bin/sh
# Corrige la interfaz del agente del host "Zabbix server" (preconfigurado en
# la imagen oficial de Zabbix con IP 127.0.0.1) para que apunte al contenedor
# real del agente dentro de la red de Docker Compose ("zabbix-agent").
#
# Motivo: el host "Zabbix server" viene precargado en la base de datos con
# una interfaz de agente apuntando a 127.0.0.1:10050, asumiendo que servidor
# y agente comparten la misma máquina. En este despliegue cada componente
# vive en su propio contenedor, así que el servidor nunca encuentra al agente
# y el frontend muestra el problema "Zabbix agent is not available".
#
# Este script espera a que Zabbix cree el esquema de la base de datos y, si
# la interfaz aún no apunta al contenedor correcto, la actualiza por DNS. Es
# idempotente: si ya está bien configurada, no hace nada.

set -eu

: "${MYSQL_USER:?Falta MYSQL_USER}"
: "${MYSQL_PASSWORD:?Falta MYSQL_PASSWORD}"
: "${MYSQL_DATABASE:?Falta MYSQL_DATABASE}"

DB_HOST="mysql-server"
AGENT_HOST_NAME="Zabbix server"
AGENT_DNS_NAME="zabbix-agent"

mysql_exec() {
  mariadb -h "$DB_HOST" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" "$@"
}

echo "[zabbix-init] Esperando a que Zabbix cree el esquema de la base de datos..."
until mysql_exec -e "SELECT 1 FROM interface LIMIT 1" >/dev/null 2>&1; do
  sleep 5
done

CURRENT_DNS=$(mysql_exec -N -e "
  SELECT dns FROM interface
   WHERE type = 1
     AND hostid IN (SELECT hostid FROM hosts WHERE host = '${AGENT_HOST_NAME}')
   LIMIT 1;
")

if [ "$CURRENT_DNS" = "$AGENT_DNS_NAME" ]; then
  echo "[zabbix-init] La interfaz de '${AGENT_HOST_NAME}' ya apunta a '${AGENT_DNS_NAME}'. Nada que hacer."
  exit 0
fi

echo "[zabbix-init] Redirigiendo la interfaz de '${AGENT_HOST_NAME}' de IP (127.0.0.1) a DNS='${AGENT_DNS_NAME}'..."
mysql_exec -e "
  UPDATE interface
     SET useip = 0, ip = '', dns = '${AGENT_DNS_NAME}'
   WHERE type = 1
     AND hostid IN (SELECT hostid FROM hosts WHERE host = '${AGENT_HOST_NAME}');
"

echo "[zabbix-init] Hecho. El servidor debería ver el agente disponible en 1-2 minutos."
echo "[zabbix-init] Si el problema persiste: docker compose restart zabbix-server"
