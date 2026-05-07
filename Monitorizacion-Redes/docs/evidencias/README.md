# Gestión de Evidencias

## Política

Toda evidencia debe poder trazarse a una fase, un comando o una validación concreta. El objetivo no es acumular capturas; el objetivo es sostener una auditoría técnica coherente.

## Tipos de evidencia aceptados

- Capturas de pantalla del frontend.
- Salidas de comandos ejecutados.
- Logs exportados o copiados desde el sistema.
- Referencias a eventos y problemas detectados.

## Convención recomendada

| Fase | Nombre sugerido |
|---|---|
| Instalación | `fase3-instalacion-01-login.png` |
| Integración de hosts | `fase4-host-01-agent-ok.txt` |
| Triggers | `fase5-trigger-cpu-warning.png` |
| Pruebas | `fase8-test-servicio-caido.log` |

## Nota operativa

Las imágenes no se incrustarán en la documentación principal. Se referenciarán por nombre de fichero y contexto.
