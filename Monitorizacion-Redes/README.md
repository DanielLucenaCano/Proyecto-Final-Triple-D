# Proyecto de Monitorización de Red

Repositorio base para la implantación académica de una plataforma de monitorización en laboratorio aislado. La estrategia aprobada para esta iteración es implantar **Zabbix** como herramienta principal, con trazabilidad documental, evidencias y automatización de soporte.

## Alcance de la iteración actual

- Comparativa técnica entre Zabbix, Nagios y Cacti.
- Selección formal de la herramienta objetivo.
- Estructura inicial del repositorio y base documental.
- Preparación de scripts, configuración y directorios de evidencias.

## Decisión ejecutiva

La herramienta seleccionada es **Zabbix**. El racional es directo: mejor equilibrio entre escalabilidad, dashboards nativos, alertado, descubrimiento, plantillas y rapidez de implantación en laboratorio. Nagios exige más ensamblaje operativo y Cacti queda por detrás en gestión integral de alertas y automatización.

## Despliegue: Docker Compose (sin VM)

El stack se despliega íntegramente con **Docker Compose** y las imágenes
oficiales de Zabbix — no depende de una máquina virtual ni de instalación
manual de paquetes/servicios. Arranque rápido:

```bash
cp .env.example .env   # ajusta credenciales y variables
docker compose up -d
```

Detalle completo en [`docs/instalacion.md`](./docs/instalacion.md) y
[`docs/arquitectura.md`](./docs/arquitectura.md). Definición del stack en
[`docker-compose.yml`](./docker-compose.yml) y variables en
[`.env.example`](./.env.example).

## Estructura

```text
project-monitoring/
├── docker-compose.yml
├── .env.example
├── docs/
├── scripts/
├── config/
└── README.md
```

## Estado por fases

- Fase 1. Introducción: base documental creada.
- Fase 2. Selección de herramienta: completada y documentada.
- Fase 3. Instalación: stack Docker Compose definido (`docker-compose.yml`,
  `.env.example`); despliegue real pendiente de validación con evidencias.
- Fase 4 en adelante: pendientes.

## Siguiente hito propuesto

Levantar el stack con `docker compose up -d`, completar el asistente web,
dar de alta el host local y documentar comandos, validaciones y evidencias
conforme a `docs/instalacion.md`.
