# Comparativa de Herramientas

## Alcance

Se comparan **Zabbix**, **Nagios** y **Cacti** conforme a los criterios operativos relevantes para el proyecto: escalabilidad, visualización, alertado, facilidad de despliegue en laboratorio, mantenimiento y capacidad de personalización.

## Resumen ejecutivo

La selección recomendada es **Zabbix**. Es la opción con mejor cobertura funcional nativa para un proyecto académico que exige despliegue integral, dashboards, alertas, políticas, validación controlada y documentación demostrable.

## Comparativa cualitativa

| Criterio | Zabbix | Nagios | Cacti |
|---|---|---|---|
| Escalabilidad | Alta. Arquitectura madura con proxies, plantillas y auto-descubrimiento. | Media-Alta. Escala, pero con mayor esfuerzo de ensamblaje y gobierno. | Media. Muy válido para gráficas, menos robusto como plataforma integral. |
| Dashboards nativos | Muy buenos. Widgets, mapas, problemas, SLA y vistas operativas. | Limitados en la edición base. Suele depender de complementos. | Buenos para gráficas históricas, flojo para operación en tiempo real. |
| Alertado y triggers | Muy completo. Severidades, dependencias, acciones y escalados. | Sólido, pero más manual y fragmentado. | Limitado comparado con Zabbix y Nagios. |
| Facilidad de implantación en laboratorio | Alta. Instalación directa y experiencia homogénea. | Media. Requiere más trabajo de integración. | Alta para gráficas, media para monitorización integral. |
| Plantillas y automatización | Muy maduras. Reduce tiempo de configuración. | Dependiente de plugins y definición manual. | Menor foco en automatización avanzada. |
| Curva de aprendizaje | Media. Amplia funcionalidad, pero coherente. | Media-Alta. Más conocimiento de componentes y plugins. | Baja-Media. Sencillo para gráficas; menos completo. |
| Ajuste al proyecto | Excelente | Aceptable | Parcial |

## Matriz de decisión ponderada

Escala de 1 a 5. La ponderación refleja impacto real en el proyecto.

| Criterio | Peso | Zabbix | Nagios | Cacti |
|---|---:|---:|---:|---:|
| Escalabilidad | 20 | 5 | 4 | 3 |
| Dashboards | 20 | 5 | 3 | 4 |
| Alertado | 20 | 5 | 4 | 2 |
| Facilidad de implantación en laboratorio | 15 | 5 | 3 | 4 |
| Automatización y plantillas | 15 | 5 | 3 | 2 |
| Adecuación académica y demostrabilidad | 10 | 5 | 4 | 3 |
| **Total ponderado** | **100** | **5.0** | **3.5** | **3.0** |

## Justificación final de la selección

### Zabbix

Zabbix concentra en una sola plataforma lo que el proyecto necesita demostrar: monitorización basada en agente, chequeos ICMP, triggers por umbral, dashboards operativos, gráficas, scripts personalizados y evidencias claras de validación. Reduce fricción técnica y maximiza capacidad de entrega.

### Nagios

Nagios es sólido y ampliamente adoptado, pero su modelo operativo exige más dependencia de plugins, más trabajo manual y mayor dispersión de componentes. Para un laboratorio acotado es viable, pero no es la opción más eficiente.

### Cacti

Cacti destaca en visualización histórica y gráficas, especialmente con SNMP. Sin embargo, queda corto como solución principal cuando el proyecto exige alertado rico, políticas avanzadas y una experiencia integral de operación.

## Decisión

Se aprueba **Zabbix** como herramienta principal del proyecto.

## Evidencias que se deberán capturar en fases posteriores

- Captura de la pantalla de login del frontend.
- Captura del dashboard principal con hosts y problemas.
- Salida de validación del agente y chequeos ICMP.
- Evidencia de triggers `Warning` y `High/Critical`.
- Evidencia de pruebas controladas de fallo.
