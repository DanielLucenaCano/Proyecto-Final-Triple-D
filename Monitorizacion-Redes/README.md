# Proyecto de Monitorización de Red

Repositorio base para la implantación académica de una plataforma de monitorización en laboratorio aislado. La estrategia aprobada para esta iteración es implantar **Zabbix** como herramienta principal, con trazabilidad documental, evidencias y automatización de soporte.

## Alcance de la iteración actual

- Comparativa técnica entre Zabbix, Nagios y Cacti.
- Selección formal de la herramienta objetivo.
- Estructura inicial del repositorio y base documental.
- Preparación de scripts, configuración y directorios de evidencias.

## Decisión ejecutiva

La herramienta seleccionada es **Zabbix**. El racional es directo: mejor equilibrio entre escalabilidad, dashboards nativos, alertado, descubrimiento, plantillas y rapidez de implantación en laboratorio. Nagios exige más ensamblaje operativo y Cacti queda por detrás en gestión integral de alertas y automatización.

## Estructura

```text
project-monitoring/
├── docs/
├── scripts/
├── config/
├── logs/
└── README.md
```

## Estado por fases

- Fase 1. Introducción: base documental creada.
- Fase 2. Selección de herramienta: completada y documentada.
- Fase 3. Instalación: pendiente de validación.
- Fase 4 en adelante: pendientes.

## Siguiente hito propuesto

Tras validación de esta iteración, se ejecutará la instalación de Zabbix Server, base de datos, frontend web y agente local, documentando comandos, validaciones y evidencias.
