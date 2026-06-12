#!/bin/sh
# Chequeo personalizado: cuenta líneas que coinciden con un patrón de error
# en un fichero de log durante los últimos N segundos. Pensado para
# integrarse como UserParameter de Zabbix agent2 (Fase 5 — personalización
# de chequeos no cubiertos por la plantilla estándar de items de sistema).
#
# A diferencia de los items de la plantilla "Linux by Zabbix agent" (que
# miden recursos del sistema operativo), este chequeo mira el contenido de
# los logs de aplicación — útil para detectar problemas funcionales que no
# se reflejan en CPU/memoria/disco (p. ej. errores de conexión a la base
# de datos, fallos de autenticación repetidos, etc.).
#
# Uso:
#   ./check_log_errors.sh <fichero_log> <patron_regex> <ventana_segundos>
#
# Salida: un único entero (nº de líneas que matchean dentro de la ventana),
# en el formato que Zabbix espera para un item numérico simple.
#
# Ejemplos:
#   ./check_log_errors.sh /var/log/zabbix/zabbix_server.log "ERROR|CRITICAL" 300
#   ./check_log_errors.sh /var/log/app/access.log " 5[0-9]{2} " 60   # errores HTTP 5xx
#
# Integración como UserParameter:
#   UserParameter=lab.log.errors[*],/etc/zabbix/scripts/check_log_errors.sh $1 "$2" $3
#
# Item resultante, p. ej.: lab.log.errors[/var/log/zabbix/zabbix_server.log,ERROR|CRITICAL,300]
# Trigger de ejemplo (más de 5 errores en la ventana → warning):
#   last(/Host/lab.log.errors[...])>5
#
# Nota: el filtrado por ventana temporal se basa en la fecha de
# modificación del fichero combinada con un conteo de líneas nuevas desde
# la última ejecución sería más preciso con estado persistente; esta
# versión usa una aproximación simple y suficiente para el laboratorio:
# cuenta coincidencias en las líneas escritas en los últimos N segundos
# usando la marca de tiempo del propio log si está en formato ISO-8601 al
# inicio de línea, y si no, recurre a `tail` sobre las últimas líneas como
# aproximación basada en volumen.

set -eu

LOGFILE="${1:?Uso: check_log_errors.sh <fichero_log> <patron_regex> <ventana_segundos>}"
PATTERN="${2:?Uso: check_log_errors.sh <fichero_log> <patron_regex> <ventana_segundos>}"
WINDOW="${3:?Uso: check_log_errors.sh <fichero_log> <patron_regex> <ventana_segundos>}"

if [ ! -r "$LOGFILE" ]; then
  # Zabbix interpreta un valor no numérico como error de recolección;
  # devolvemos 0 y dejamos constancia por stderr para depuración manual.
  echo "0"
  echo "[check_log_errors] aviso: no se puede leer ${LOGFILE}" >&2
  exit 0
fi

NOW=$(date +%s)
CUTOFF=$((NOW - WINDOW))

# Intento 1: líneas con timestamp ISO-8601 al inicio (YYYY-MM-DD[ T]HH:MM:SS)
COUNT=$(awk -v cutoff="$CUTOFF" -v pattern="$PATTERN" '
  match($0, /^[0-9]{4}-[0-9]{2}-[0-9]{2}[ T][0-9]{2}:[0-9]{2}:[0-9]{2}/) {
    ts_str = substr($0, RSTART, 19)
    gsub(/T/, " ", ts_str)
    cmd = "date -d \"" ts_str "\" +%s 2>/dev/null"
    cmd | getline ts
    close(cmd)
    if (ts >= cutoff && $0 ~ pattern) count++
    next
  }
  { fallback_total++; if ($0 ~ pattern) fallback_match++ }
  END {
    if (count > 0 || (fallback_total == 0)) { print count + 0 }
    else { print fallback_match + 0 }
  }
' "$LOGFILE" 2>/dev/null || echo 0)

echo "${COUNT:-0}"
