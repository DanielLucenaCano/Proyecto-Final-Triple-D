# Dashboards e Informes

## Estado

Diseño completado y guía de creación lista para ejecutar en el frontend
(`http://localhost:${WEB_PORT}`, por defecto `:8080`). La creación final
del dashboard se hace de forma interactiva en la interfaz web — sigue la
guía de esta página y, al terminar, captura las evidencias indicadas al
final del documento.

## Criterios de diseño

- **Una vista, un propósito**: el dashboard "Laboratorio - Estado General"
  responde a la pregunta "¿está todo bien ahora mismo?" de un vistazo,
  sin necesitar navegar a otras secciones.
- **De lo general a lo concreto**: arriba los indicadores de estado global
  (problemas activos, disponibilidad), abajo el detalle de rendimiento
  (gráficas históricas de CPU/memoria/disco).
- **Coherencia con las políticas**: los widgets de problemas filtran por
  los triggers definidos en `config/templates/plantilla-laboratorio-base.yaml.example`
  y documentados en `docs/politicas-monitorizacion.md`, para que las
  severidades mostradas (`Warning`/`High`) sean las mismas que disparan
  las alertas.
- **Refresco acorde al intervalo de recolección**: los widgets se
  configuran con un refresco de 30s–1min, en línea con el intervalo de
  los items de la plantilla `Linux by Zabbix agent` (1 min por defecto),
  para evitar dar la falsa sensación de "tiempo real" cuando el dato
  subyacente no se actualiza tan rápido.

## Vista 1 — "Laboratorio - Estado General"

### Guía de creación paso a paso (Zabbix 7.4)

1. Inicia sesión en el frontend (`Admin` / contraseña ya cambiada según
   `docs/instalacion.md`).
2. Ve a **Dashboards** (menú lateral izquierdo) → botón **Create dashboard**
   (esquina superior derecha).
3. Rellena:
   - **Owner**: `Admin` (o el usuario operador del laboratorio).
   - **Name**: `Laboratorio - Estado General`.
   - **Default page name**: `Resumen`.
4. Pulsa **Add widget** y añade, en este orden (de arriba abajo, dos
   columnas donde se indique):

   | # | Tipo de widget | Configuración clave | Qué muestra |
   |---|---|---|---|
   | 1 | **Problems** | *Show*: `Recent problems`; *Host groups*: `Laboratorio Monitorizacion-Redes`; *Severity*: `Warning` y superiores marcadas; *Show tags*: `1` | Lista en vivo de problemas activos/recientes con su severidad — el "semáforo" del laboratorio. |
   | 2 | **Problems by severity** | *Host groups*: `Laboratorio Monitorizacion-Redes`; *Layout*: `Horizontal` | Recuento de problemas agrupados por severidad (Warning/High), para ver de un vistazo si hay incidencias críticas abiertas. |
   | 3 | **Host availability** | *Host groups*: `Laboratorio Monitorizacion-Redes`; *Interface type*: `Agent` | Disponibilidad del host `Zabbix server` (verde = disponible, rojo = inalcanzable) — cubre la dimensión "disponibilidad" de `docs/introduccion.md`. |
   | 4 | **Graph (classic)** o **Graph (SVG)** | *Data set* → *Host*: `Zabbix server`; *Item pattern*: `CPU load` (`system.cpu.load[percpu,avg1]`); *Time period*: `Last 1 hour` | Evolución de la carga de CPU — referencia visual directa de los umbrales 1.5/3 definidos en la plantilla. |
   | 5 | **Graph (SVG)** | *Data set* → *Host*: `Zabbix server`; *Item pattern*: `Available memory` (`vm.memory.size[available]`) | Evolución de la memoria disponible — referencia de los umbrales 20%/10%. |
   | 6 | **Graph (SVG)** | *Data set* → *Host*: `Zabbix server`; *Item pattern*: `Free disk space on /` (`vfs.fs.size[/,pfree]`) | Evolución del espacio libre en disco — referencia de los umbrales 20%/10%. |

5. Ajusta el **Refresh interval** del dashboard (icono de engranaje, arriba
   a la derecha) a `30 seconds` o `1 minute`.
6. Pulsa **Save changes**. El dashboard queda accesible desde
   **Dashboards → Laboratorio - Estado General** para cualquier usuario con
   permisos sobre el grupo de hosts.

> **Nota sobre nombres de items**: si al buscar el patrón no aparece el
> item esperado, comprueba el nombre exacto en
> **Data collection → Hosts → Zabbix server → Items** y filtra por la
> plantilla `Linux by Zabbix agent` — los nombres pueden variar
> ligeramente entre versiones de la plantilla oficial.

## Informes periódicos

Zabbix 7.x permite programar el envío periódico de capturas de un
dashboard por correo (**Reports → Scheduled reports**). Para este
laboratorio:

1. Ve a **Reports → Scheduled reports** → **Create report**.
2. Configura:
   - **Name**: `Informe semanal - Estado del laboratorio`.
   - **Dashboard**: `Laboratorio - Estado General`.
   - **Period**: `Weekly`.
   - **Recipients**: el usuario `Admin` (o un grupo de usuarios del
     laboratorio); requiere tener configurado un *Media type* de correo
     en **Alerts → Media types** y asociado al usuario en
     **Users → Users → \<usuario\> → Media**.
3. Guarda. El informe generará y enviará una captura del dashboard con la
   periodicidad indicada — útil para revisar tendencias sin entrar al
   frontend cada día.

> Si no se dispone de un servidor SMTP en el laboratorio, este paso queda
> documentado como **diseño validado pero no ejecutado** (limitación de
> entorno, no de la herramienta) — anótalo así en `docs/conclusiones.md`.

## Evidencias a capturar

Una vez creado el dashboard con datos reales fluyendo:

- Captura de pantalla del dashboard completo (`Laboratorio - Estado General`)
  con los seis widgets visibles y datos reales (no "No data").
- Captura del widget **Problems** mostrando al menos un problema activo
  (puede generarse a propósito siguiendo `docs/validacion-pruebas.md`,
  por ejemplo el caso "Sobrecarga de CPU").
- Captura de la configuración de **Scheduled reports** (aunque el envío no
  llegue a ejecutarse por falta de SMTP, la configuración en sí es
  evidencia del diseño).

Guarda las capturas en `docs/evidencias/` siguiendo la convención descrita
en `docs/evidencias/README.md`.
