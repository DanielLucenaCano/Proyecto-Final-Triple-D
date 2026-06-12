# Utilidades

Scripts de soporte para la generación de carga controlada y la validación
del laboratorio (ver [`docs/validacion-pruebas.md`](../../docs/validacion-pruebas.md)).

## Inventario

| Script | Función | Caso de prueba asociado |
|---|---|---|
| [`generar-carga-cpu.sh`](./generar-carga-cpu.sh) | Genera carga artificial de CPU sostenida durante N segundos con M procesos en paralelo, para disparar los triggers `CPU load alto/critico en {HOST.NAME}` de la plantilla `Laboratorio - Umbrales Base`. | Sobrecarga de CPU |

## Cómo ejecutarlos

Estos scripts están pensados para ejecutarse **dentro del contenedor** que
actúa como host monitorizado (`zabbix-agent`, host `Zabbix server` en el
frontend), no en la máquina anfitriona:

```bash
# Copia el script al contenedor y entra en una shell
docker compose cp scripts/utils/generar-carga-cpu.sh zabbix-agent:/tmp/generar-carga-cpu.sh
docker compose exec zabbix-agent sh /tmp/generar-carga-cpu.sh 360 2
```

Detalle paso a paso de cada caso de prueba (qué esperar, qué capturar como
evidencia) en [`docs/validacion-pruebas.md`](../../docs/validacion-pruebas.md).
