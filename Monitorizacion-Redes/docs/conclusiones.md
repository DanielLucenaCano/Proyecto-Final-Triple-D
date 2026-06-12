# Conclusiones

## Estado

Redactadas a partir del trabajo realizado y documentado en este
repositorio. Las afirmaciones marcadas como **(a confirmar tras pruebas)**
dependen de la ejecución de `docs/validacion-pruebas.md` con resultados
reales — actualízalas (y, si procede, los apartados de "líneas de mejora")
una vez completada esa matriz, para que esta página refleje el cierre
real del proyecto y no solo el diseño.

## Grado de cumplimiento de objetivos

| Fase del guion | Objetivo | Cumplimiento |
|---|---|---|
| 1. Introducción | Comprender conceptos y tipos de monitorización | Completo — `docs/introduccion.md` |
| 2. Selección de herramienta | Comparar y justificar Zabbix/Nagios/Cacti | Completo — `docs/comparativa-herramientas.md`, decisión razonada por Zabbix |
| 3. Instalación | Desplegar y validar el stack con datos reales | Completo — stack en Docker Compose desplegado, host monitorizado y datos fluyendo (`docs/instalacion.md`, `docs/arquitectura.md`); integración de varios dispositivos simulados queda como ampliación (ver limitaciones) |
| 4. Políticas de monitorización | Definir parámetros, umbrales y severidades | Completo en diseño — `docs/politicas-monitorizacion.md` y plantilla `Laboratorio - Umbrales Base`; ajuste fino pendiente de validación con datos reales |
| 5. Personalización y scripts | Desarrollar chequeos propios | Completo en diseño e implementación — `scripts/checks/` (`check_tcp_port.sh`, `check_log_errors.sh`) y guía de integración como UserParameters; integración final en el frontend **(a confirmar tras pruebas)** |
| 6. Dashboard e informes | Visualizar el estado del laboratorio | Diseño y guía de creación completos — `docs/dashboards.md`; construcción interactiva en el frontend **(a confirmar tras pruebas)** |
| 7. Pruebas y validación | Provocar incidencias controladas y validar la respuesta | Procedimiento detallado listo — `docs/validacion-pruebas.md`; ejecución y resultados **(a confirmar tras pruebas)** |
| 8. Documentación y presentación | Documentar y presentar resultados | Completo — memoria, arquitectura, instalación, políticas, dashboards, validación, conclusiones y presentación (`docs/presentacion.pptx`) |

En conjunto, **las ocho fases tienen entregable documental completo**; las
fases que requieren interacción en vivo con el frontend (6 y 7,
parcialmente la 5) tienen el diseño, los scripts y el procedimiento
listos para ejecutarse — su cierre depende de una sesión de trabajo sobre
el stack desplegado, no de trabajo de diseño pendiente.

## Lecciones aprendidas

- **Migrar de "VM + systemd" a Docker Compose simplificó radicalmente el
  despliegue.** El cambio de enfoque (documentado en `docs/arquitectura.md`)
  eliminó la gestión manual de paquetes, el orden de arranque de servicios
  y la configuración de red por IP fija, sustituyéndolos por
  `depends_on` + `healthcheck` declarativos y resolución por nombre de
  servicio. La lección es general: en laboratorios de aprendizaje, reducir
  la fricción de "puesta en marcha" deja más tiempo para el objetivo real
  (entender la herramienta de monitorización), no para pelear con la
  infraestructura que la sostiene.
- **Los valores por defecto de las imágenes oficiales no siempre encajan
  con un despliegue multi-contenedor.** El host `Zabbix server` precargado
  por la imagen apunta su interfaz de agente a `127.0.0.1`, lo cual solo
  tiene sentido si servidor y agente comparten máquina. Detectarlo y
  resolverlo con un *init container* idempotente (`zabbix-init` /
  `scripts/fix-agent-interface.sh`) en lugar de un ajuste manual cada vez
  que se recrean los volúmenes fue clave para que el laboratorio sea
  reproducible sin pasos ocultos.
- **Diseñar las políticas de alerta antes de tener datos reales obliga a
  declarar umbrales como "provisionales" — y eso es correcto, no un
  defecto.** La separación entre "diseño razonado" (`docs/politicas-monitorizacion.md`)
  y "validación con datos reales" (`docs/validacion-pruebas.md`, con su
  sección de histórico de ajustes) permite avanzar en paralelo sin fingir
  una certeza que todavía no existe, y dejar trazabilidad de por qué un
  umbral cambió.
- **Un chequeo personalizado genérico y parametrizable vale más que varios
  específicos.** En lugar de un script por servicio, `check_tcp_port.sh`
  cubre cualquier servicio TCP mediante parámetros — coherente con el
  principio de extender la plantilla estándar (no sustituirla) que también
  se aplicó al diseño de triggers.

## Limitaciones del laboratorio

- **Host único monitorizado.** El guion menciona "integración con
  dispositivos de xarxa simulats"; esta iteración monitoriza solo el
  contenedor `zabbix-agent` (host `Zabbix server`). El procedimiento para
  ampliar a más hosts/dispositivos está documentado y probado en su
  diseño (`config/agents/README.md`), pero no ejecutado — es la ampliación
  más directa para una siguiente iteración.
- **Sin servidor SMTP en el laboratorio.** Los informes periódicos
  (`docs/dashboards.md`, sección "Informes periódicos") están diseñados y
  configurables, pero su envío real no puede demostrarse sin un *media
  type* de correo operativo — limitación de entorno, no de la herramienta
  ni del diseño.
- **Entorno de laboratorio aislado, no producción.** Los umbrales,
  severidades (solo `Warning`/`High`) y el alcance de las pruebas están
  calibrados para demostrar el mecanismo con un host de bajo consumo
  basal, no para representar cargas ni topologías de producción real.
- **Validación dependiente de ejecución manual interactiva.** Las pruebas
  de la Fase 7 requieren intervenir sobre el stack en marcha (parar
  contenedores, generar carga, desconectar redes) y observar la respuesta
  en tiempo real en el frontend — no son automatizables sin un entorno de
  CI con acceso a Docker y al navegador, lo cual queda fuera del alcance
  de esta iteración documental.

## Líneas de mejora futura

1. **Ampliar a varios hosts/dispositivos simulados** siguiendo
   `config/agents/README.md`, para ejercitar plantillas SNMP o de
   aplicación distintas a `Linux by Zabbix agent` y enriquecer el
   dashboard con una vista comparativa entre hosts.
2. **Cerrar el ciclo de validación** (`docs/validacion-pruebas.md`):
   ejecutar los tres casos, capturar evidencias, ajustar umbrales según lo
   observado y registrar los cambios en el histórico de
   `docs/politicas-monitorizacion.md`.
3. **Añadir severidad `Disaster`** y acciones de notificación (correo,
   webhook a un canal de chat) si se incorpora algún servicio que se
   considere crítico para el laboratorio, cerrando así también el diseño
   de informes periódicos con un *media type* real.
4. **Incorporar HTTPS** en el frontend mediante un proxy inverso con TLS,
   tal y como se apunta como mejora futura en `docs/arquitectura.md`.
5. **Versionar la plantilla de umbrales como definitiva** una vez ajustada
   con datos reales, retirando la marca "PROVISIONAL" de
   `config/templates/plantilla-laboratorio-base.yaml.example`.
