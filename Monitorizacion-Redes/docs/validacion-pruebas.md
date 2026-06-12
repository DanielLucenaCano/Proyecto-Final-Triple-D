# Validación y Pruebas

## Estado

Procedimiento detallado listo para ejecutar. Las herramientas necesarias
(script de carga) están en `scripts/utils/`. La columna **Resultado real**
y **Evidencia** quedan a completar por quien ejecute las pruebas contra el
stack en marcha — anota hora de inicio/fin, capturas y, si procede,
ajustes de umbral derivados de lo observado.

## Matriz de casos

| Caso | Acción | Resultado esperado | Resultado real | Evidencia |
|---|---|---|---|---|
| Caída de servicio | Detener el contenedor del agente (`docker compose stop zabbix-agent`) | El host `Zabbix server` pasa a "no disponible"; problema de disponibilidad del agente en Monitoring → Problems | Pendiente de ejecutar | Pendiente |
| Sobrecarga de CPU | Ejecutar `scripts/utils/generar-carga-cpu.sh` dentro del contenedor del agente durante ≥6 minutos | Se dispara el trigger `CPU load alto en Zabbix server (warning)` (y, con más procesos/duración, el `critico`); aparece en Problems con severidad Warning/High | Pendiente de ejecutar | Pendiente |
| Host inaccesible | Desconectar el contenedor del agente de la red (`docker network disconnect zabbix-net zabbix-agent`) | Zabbix detecta el host como inalcanzable (ICMP/agente no disponible) y genera el problema correspondiente | Pendiente de ejecutar | Pendiente |

## Procedimiento detallado por caso

### 1. Caída de servicio

**Objetivo**: comprobar que detener el agente monitorizado genera un
problema visible y, si hay acciones configuradas, una alerta.

1. Antes de empezar, anota la hora exacta (servirá para correlar con el
   timestamp del evento en Zabbix).
2. Detén el contenedor del agente:
   ```bash
   docker compose stop zabbix-agent
   ```
3. Espera 1–3 minutos (el servidor necesita varios fallos de sondeo
   consecutivos antes de marcar el host como no disponible — controlado
   por los parámetros del icono de disponibilidad del host).
4. En el frontend: **Monitoring → Problems** — debe aparecer un problema
   del tipo "Zabbix agent is not available" (o equivalente) sobre el host
   `Zabbix server`. El icono de disponibilidad del host (en
   **Data collection → Hosts**) debe pasar de verde a rojo.
5. Captura: pantalla de **Problems** con el evento, y de **Hosts** con el
   icono en rojo. Anota la hora de detección que muestra Zabbix y compárala
   con la hora real de la parada (para documentar la latencia de detección).
6. Restaura el servicio:
   ```bash
   docker compose start zabbix-agent
   ```
   Comprueba que el problema se resuelve solo (pasa a "RESOLVED") en
   **Monitoring → Problems** (incluyendo los ya resueltos con el filtro
   correspondiente). Captura también esta resolución — demuestra el ciclo
   completo detección → alerta → recuperación.

### 2. Sobrecarga de CPU

**Objetivo**: comprobar que una carga sostenida dispara los triggers de
umbral de CPU definidos en `config/templates/plantilla-laboratorio-base.yaml.example`.

1. Copia y ejecuta el script dentro del contenedor del agente:
   ```bash
   docker compose cp scripts/utils/generar-carga-cpu.sh zabbix-agent:/tmp/generar-carga-cpu.sh
   docker compose exec zabbix-agent sh /tmp/generar-carga-cpu.sh 360 2
   ```
   Ajusta los parámetros si el umbral de `1.5` no llega a superarse con
   2 procesos (prueba `4` o `6` procesos, o una duración mayor — recuerda
   que el trigger evalúa la **media de 5 minutos**, así que picos breves
   no son suficientes).
2. Mientras se ejecuta, observa en tiempo real:
   - **Monitoring → Latest data** → host `Zabbix server` → item
     `CPU load` — el valor debe subir y mantenerse por encima de `1.5`.
   - **Monitoring → Problems** — en cuanto la media de 5 minutos supere
     el umbral, debe aparecer "CPU load alto en Zabbix server (warning)".
3. Si la carga es suficientemente alta y sostenida, debería escalar
   también a "CPU load critico en Zabbix server (critical)" (umbral `>3`).
4. Captura: gráfica del item `CPU load` mostrando el pico (con el umbral
   de referencia si la vista lo permite), y el problema en **Problems**
   con su severidad y duración.
5. Al terminar el script, deja pasar el tiempo necesario para que la
   media de 5 minutos vuelva a bajar del umbral y comprueba que el
   problema se resuelve solo. Documenta el tiempo total entre disparo y
   resolución.
6. **Si los umbrales provisionales (1.5 / 3) resultan poco realistas**
   para la carga de base del contenedor (por ejemplo, se disparan sin
   generar carga, o no se disparan ni con el script al máximo), ajústalos
   en la plantilla y registra el cambio — con su justificación — tanto en
   `docs/politicas-monitorizacion.md` como en el changelog de la plantilla.

### 3. Host inaccesible

**Objetivo**: comprobar la detección de pérdida de conectividad de red
(distinto del caso 1: aquí el proceso del agente sigue vivo, pero pierde
la red).

1. Anota la hora de inicio.
2. Desconecta el contenedor del agente de la red del laboratorio:
   ```bash
   docker network disconnect zabbix-net zabbix-agent
   ```
3. Espera 1–3 minutos y revisa **Monitoring → Problems**: debe aparecer
   un problema de inaccesibilidad sobre el host `Zabbix server`
   (mismo tipo de evento que en el caso 1 desde el punto de vista del
   servidor — la diferencia relevante a documentar es la **causa real**:
   aquí es de red, no de proceso parado).
4. Captura: pantalla de **Problems** y, si se dispone de acceso a logs del
   `zabbix-server` (`docker compose logs zabbix-server`), un fragmento que
   muestre el error de conexión al agente (timeout / "no route to host").
5. Reconecta para restaurar el laboratorio:
   ```bash
   docker network connect zabbix-net zabbix-agent
   ```
   Verifica que el problema se resuelve y el host vuelve a "disponible".
   Si no se resuelve solo en unos minutos, reinicia el agente
   (`docker compose restart zabbix-agent`).

## Qué documentar al rellenar la matriz

Para cada caso, sustituye "Pendiente de ejecutar" por una frase breve que
indique si el resultado coincidió con lo esperado (y si no, qué pasó
realmente — esto también es validación útil: un umbral que no se dispara
cuando debería es un hallazgo, no un fallo del informe). En "Evidencia",
referencia el fichero de captura guardado en `docs/evidencias/`
(convención en `docs/evidencias/README.md`), por ejemplo
`evidencias/caso-cpu-problema.png`.

## Conclusión de esta fase

Una vez completada la matriz con resultados reales, traslada el resumen
(qué funcionó, qué umbrales se ajustaron y por qué, qué limitaciones de
laboratorio se observaron) a `docs/conclusiones.md`.
