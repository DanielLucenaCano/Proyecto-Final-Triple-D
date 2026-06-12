#!/bin/sh
# Chequeo personalizado: comprueba si un puerto TCP está abierto y mide
# el tiempo de conexión (en milisegundos). Pensado para integrarse como
# UserParameter de Zabbix agent2 y cubrir la "personalización de chequeos"
# pedida en la Fase 5 del guion — útil tanto para servicios del propio
# laboratorio como para los "dispositivos de red simulados" (Fase 3):
# cualquier servicio expuesto por TCP (HTTP, base de datos, SSH, un socket
# simulando un dispositivo de red) puede comprobarse con este script sin
# escribir un chequeo distinto para cada uno.
#
# Uso:
#   ./check_tcp_port.sh <host> <puerto> [timeout_segundos]
#
# Salida (una sola línea, formato "clave=valor" para fácil parseo):
#   status=up;latency_ms=<n>      si conecta
#   status=down;latency_ms=-1     si no conecta o hay timeout
#
# Ejemplos:
#   ./check_tcp_port.sh zabbix-web 8080
#   ./check_tcp_port.sh mysql-server 3306 2
#
# Integración como UserParameter (en el contenedor del agente, ver
# scripts/checks/README.md para el procedimiento completo):
#   UserParameter=lab.tcp.check[*],/etc/zabbix/scripts/check_tcp_port.sh $1 $2 $3
#
# Desde Zabbix, los items resultantes podrían ser:
#   lab.tcp.check[zabbix-web,8080,2]   -> "status=up;latency_ms=12"
# y un trigger de ejemplo:
#   find(/Host/lab.tcp.check[zabbix-web,8080,2],,"like","status=down")=1

set -eu

HOST="${1:?Uso: check_tcp_port.sh <host> <puerto> [timeout_segundos]}"
PORT="${2:?Uso: check_tcp_port.sh <host> <puerto> [timeout_segundos]}"
TIMEOUT="${3:-3}"

START_MS=$(($(date +%s%N) / 1000000))

# /dev/tcp es una extensión de bash; en sh (dash/busybox) usamos `nc` si
# está disponible, con fallback a /dev/tcp si la shell lo soporta.
if command -v nc >/dev/null 2>&1; then
  if nc -z -w "$TIMEOUT" "$HOST" "$PORT" >/dev/null 2>&1; then
    CONNECTED=1
  else
    CONNECTED=0
  fi
else
  if (exec 3<>"/dev/tcp/${HOST}/${PORT}") 2>/dev/null; then
    exec 3>&- 3<&-
    CONNECTED=1
  else
    CONNECTED=0
  fi
fi

END_MS=$(($(date +%s%N) / 1000000))
LATENCY=$((END_MS - START_MS))

if [ "$CONNECTED" -eq 1 ]; then
  echo "status=up;latency_ms=${LATENCY}"
else
  echo "status=down;latency_ms=-1"
fi
