#!/bin/sh
# Genera carga artificial de CPU durante un tiempo determinado, para
# provocar de forma controlada los triggers de "CPU load alto/critico"
# definidos en config/templates/plantilla-laboratorio-base.yaml.example
# y validar el caso "Sobrecarga de CPU" de docs/validacion-pruebas.md.
#
# Uso:
#   ./generar-carga-cpu.sh [segundos] [procesos_paralelos]
#
# Ejemplos:
#   ./generar-carga-cpu.sh            # 360s (6 min) con 2 procesos (valores por defecto)
#   ./generar-carga-cpu.sh 600 4      # 10 min con 4 procesos en paralelo (carga mayor)
#
# Dónde ejecutarlo: DENTRO del contenedor que se quiere sobrecargar
# (normalmente "zabbix-agent", que es el host monitorizado "Zabbix server"):
#
#   docker compose exec zabbix-agent sh
#   # (copia este script al contenedor o pégalo y ejecútalo, ver docs/validacion-pruebas.md)
#
# El trigger evalúa la carga media en ventanas de 5 minutos
# (system.cpu.load[percpu,avg1] con min(...,5m)), así que para que se
# dispare hace falta sostener la carga varios minutos seguidos —
# de ahí el valor por defecto de 360s.

set -eu

DURACION="${1:-360}"
PROCESOS="${2:-2}"

echo "[carga-cpu] Generando carga durante ${DURACION}s con ${PROCESOS} proceso(s) en paralelo..."
echo "[carga-cpu] Cada proceso calcula en bucle para mantener la CPU ocupada."
echo "[carga-cpu] Pulsa Ctrl+C para abortar antes de tiempo."

i=0
while [ "$i" -lt "$PROCESOS" ]; do
  (
    END=$(($(date +%s) + DURACION))
    while [ "$(date +%s)" -lt "$END" ]; do
      : $((1 + 1))
      awk 'BEGIN { x = 0; for (i = 0; i < 200000; i++) { x += i * i } }' >/dev/null
    done
  ) &
  i=$((i + 1))
done

wait
echo "[carga-cpu] Hecho. Comprueba en Zabbix (Monitoring -> Latest data / Problems)"
echo "[carga-cpu] si se ha generado el problema 'CPU load alto/critico en Zabbix server'."
echo "[carga-cpu] Recuerda: el trigger usa una media de 5 minutos, así que el evento"
echo "[carga-cpu] puede tardar unos minutos en aparecer (y otros tantos en resolverse)."
