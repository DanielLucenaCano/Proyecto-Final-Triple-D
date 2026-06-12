# Políticas de Monitorización

## Estado

Definidas y aplicadas mediante la plantilla
[`config/templates/plantilla-laboratorio-base.yaml.example`](../config/templates/plantilla-laboratorio-base.yaml.example),
vinculada al host `Zabbix server`. Los umbrales se marcan **provisionales**
hasta completar la validación con datos reales descrita en
`docs/validacion-pruebas.md`; cualquier ajuste derivado de esa fase debe
reflejarse aquí (sección "Histórico de ajustes").

## Alcance y enfoque

Esta política cubre, para cada host monitorizado del laboratorio, cuatro
dimensiones operativas que se corresponden con los "tipos de
monitorización" descritos en `docs/introduccion.md`:

1. **Disponibilidad** — ¿está vivo el host/agente?
2. **Capacidad/recursos** — CPU, memoria, disco.
3. **Rendimiento** — tendencias que anticipan saturación antes de que
   se conviertan en incidente.
4. **Servicios** — procesos o puertos críticos del laboratorio (ampliable
   según los hosts que se den de alta, ver `config/agents/README.md`).

El principio rector es **alertar lo justo**: cada trigger debe representar
una condición que requiera atención humana. Umbrales demasiado sensibles
generan fatiga de alertas (se acaban ignorando); umbrales demasiado laxos
dejan pasar incidencias reales. Por eso cada regla usa una **ventana
temporal** (`5m`) en lugar de valores instantáneos — exige que la
condición se sostenga, filtrando picos puntuales sin significado operativo.

## Matriz de parámetros y umbrales

| Métrica | Item de origen | Umbral Warning | Umbral Critical | Ventana | Racional |
|---|---|---|---|---|---|
| Carga de CPU | `system.cpu.load[percpu,avg1]` | `> 1.5` | `> 3` | media 5 min | En un host de 1 vCPU (caso típico de laboratorio en contenedor), una carga media sostenida > 1.5 indica cola de procesos esperando CPU; > 3 indica saturación clara. La media de 5 min evita falsas alarmas por picos de arranque de procesos puntuales. |
| Memoria disponible | `vm.memory.size[pavailable]` | `< 20%` | `< 10%` | media 5 min | Por debajo del 20% el sistema empieza a depender de swap/caché bajo presión, con riesgo de degradación; por debajo del 10% el riesgo de OOM (out-of-memory) es alto. La ventana de 5 min filtra picos transitorios de procesos que liberan memoria rápidamente. |
| Espacio en disco (`/`) | `vfs.fs.size[/,pfree]` | `< 20%` | `< 10%` | valor actual (`last`) | El espacio en disco no fluctúa en segundos como CPU/memoria — un valor puntual ya es representativo, no necesita ventana de promedio. El umbral del 20% da margen para planificar limpieza/ampliación antes de llegar al 10%, donde servicios como bases de datos o el propio Zabbix pueden empezar a fallar al escribir. |
| Disponibilidad del agente | Estado de la interfaz del host (`zabbix[host.maintenance]` / availability icon) | — | Host no disponible | tras varios sondeos fallidos consecutivos | Cubierta de forma nativa por Zabbix (no requiere trigger explícito): el servidor marca el host como "no disponible" tras N fallos de sondeo seguidos, y genera el evento "Zabbix agent is not available". Es la primera señal de un caso de "caída de servicio" u "host inaccesible" (ver `docs/validacion-pruebas.md`). |

> Los cuatro primeros triggers (CPU/memoria/disco en sus dos niveles) están
> implementados en la plantilla `Laboratorio - Umbrales Base`; la
> disponibilidad del agente la proporciona Zabbix de forma nativa para
> cualquier host con interfaz de agente — no requiere configuración
> adicional más allá de tener el host dado de alta.

## Severidades y criterio de escalado

| Severidad Zabbix | Uso en esta política | Expectativa de respuesta |
|---|---|---|
| `Warning` | Primer nivel de aviso: la métrica ha cruzado el umbral "hay que vigilar esto" | Revisar en la siguiente sesión de operación; no requiere intervención inmediata si es puntual |
| `High` (etiquetado como "critical" en los nombres de los triggers, por legibilidad) | La métrica ha cruzado el umbral "esto puede degradar el servicio pronto" | Revisar y actuar en el mismo día; si se repite, revisar dimensionamiento del recurso |

No se usan las severidades `Disaster` ni `Average`/`Information` en esta
iteración: el laboratorio tiene un único host y un alcance de prueba de
concepto, por lo que dos niveles (`Warning`/`High`) son suficientes para
demostrar el mecanismo de escalado sin sobrecargar la matriz de pruebas.
Si se amplía el laboratorio con servicios críticos de producción simulada,
se recomienda incorporar `Disaster` para condiciones de pérdida total de
servicio.

## Racional técnico común a todos los triggers

- **Funciones de agregación (`min`, `last`)**: `min(...,5m)` para CPU y
  memoria garantiza que *todo* el intervalo estuvo por encima/debajo del
  umbral (no solo el promedio), lo cual es una condición más estricta y
  reduce falsos positivos. Para disco se usa `last` porque la métrica es
  prácticamente constante a esa escala temporal — promediarla no aporta
  valor y solo retrasaría la detección.
- **Nomenclatura**: todos los nombres de trigger incluyen `{HOST.NAME}`
  para que, al añadir más hosts y vincular la misma plantilla, cada
  problema se identifique sin ambigüedad en **Monitoring → Problems**.
- **Dependencia de la plantilla base**: los triggers se definen como
  *extensión* de `Linux by Zabbix agent` (no la sustituyen) para
  aprovechar sus items ya probados y mantenidos por Zabbix, manteniendo
  el esfuerzo de personalización centrado en las reglas de negocio
  (umbrales y severidades), no en la recolección de datos.

## Aplicación por tipo de dispositivo

En esta iteración el laboratorio monitoriza un único tipo de dispositivo
(host Linux vía agente, contenedor `zabbix-agent`), por lo que la matriz
anterior se aplica de forma uniforme. Si se incorporan dispositivos de
otra naturaleza (ver crecimiento previsto en `docs/arquitectura.md` y
procedimiento en `config/agents/README.md`), esta sección debe ampliarse
con una sub-matriz por tipo, por ejemplo:

- **Dispositivos de red (switches/routers simulados, vía SNMP)**:
  disponibilidad (ICMP/SNMP), uso de interfaces (`ifInOctets`/`ifOutOctets`),
  errores de interfaz — umbrales a definir según ancho de banda simulado.
- **Servicios de aplicación (HTTP, bases de datos)**: tiempo de respuesta,
  códigos de error, disponibilidad del puerto — umbrales a definir según
  el SLA simulado del laboratorio.

## Histórico de ajustes

| Fecha | Cambio | Motivo | Evidencia |
|---|---|---|---|
| — | (sin ajustes todavía; los umbrales actuales son los provisionales iniciales) | — | — |

> Al completar `docs/validacion-pruebas.md`, registra aquí cualquier
> cambio de umbral derivado de la observación de datos reales (por
> ejemplo, "se sube CPU Warning de 1.5 a 2.0 porque la carga base del
> contenedor en reposo ya rondaba 1.3, generando falsos positivos").
