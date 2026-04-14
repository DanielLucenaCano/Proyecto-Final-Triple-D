# Plan de Ejecucion

## Fuente de verdad y criterio rector

- El archivo `pdf_extract_advanced.txt` se adopta como fuente de verdad funcional.
- El repositorio actual se adopta como fuente de verdad tecnica de partida.
- La prioridad de ejecucion es cerrar requisitos funcionales del enunciado antes de optimizaciones cosmeticas.
- Toda decision relevante debe quedar documentada dentro de `docs/`.

## Diagnostico inicial

### Capacidades ya presentes

- Base funcional de ShopMicro con los 10 servicios exigidos.
- `docker-compose.yml` operativo como entorno local de referencia.
- `docker-stack.yml` base para Swarm con secretos y redes segregadas.
- Manifiestos Kubernetes iniciales para namespace, servicios de negocio e infraestructura.
- Documentacion heredada de fases anteriores que sirve como contexto tecnico.

### Brechas detectadas contra el PDF avanzado

#### Fase 1. Docker Swarm avanzado

- Falta el stack de monitorizacion `Prometheus + cAdvisor`.
- Falta una red de monitorizacion dedicada.
- Falta una politica de rolling update y rollback conforme al enunciado para `product-service`.
- Falta una configuracion operativa y documental para demostrar escalado por servicio, escalado global, routing mesh y VIP.

#### Fase 2. Kubernetes HA y monitorizacion

- `db-products` y `db-orders` siguen desplegados como `Deployment`; deben migrarse a `StatefulSet`.
- Redis y RabbitMQ no tienen persistencia declarativa mediante PVC.
- No existe un `ConfigMap` comun de entorno ni una estructura consistente de configuracion compartida.
- No existe `podAntiAffinity` obligatorio en `product-service`, `order-service` y `user-service`.
- No existe integracion declarativa con `kube-prometheus-stack`, `ServiceMonitor` ni reglas de alerta.

#### Fase 3. Recursos, autoscaling y balanceo

- Faltan `resources.requests` y `resources.limits` en todos los workloads.
- Falta `HPA` para `product-service`.
- Las probes no estan alineadas con el requisito de `liveness` y `readiness` diferenciadas.
- Los microservicios no exponen aun un `path /ready` para readiness avanzada.
- No existe recurso `Ingress` para acceso centralizado.

#### Fase 4. Helm e Istio

- No existe Helm chart propio del proyecto.
- No existen manifiestos de Istio (`VirtualService`, `DestinationRule`) ni guia operativa asociada.

#### Documentacion y trazabilidad

- Falta documentacion de proyecto final en formato operativo y de auditoria.
- La documentacion existente contiene afirmaciones historicas que ya no sirven como entrega final.
- No hay trazabilidad Git inicializada dentro del directorio de trabajo actual.
- `git`, `gh` y `helm` no estan actualmente disponibles en `PATH`.
- Docker Desktop no estaba operativo durante la auditoria inicial y el contexto `kubectl` apuntaba a un clúster no accesible.

## Estrategia de ejecucion

### Hito 1. Normalizacion documental y de arquitectura

- Crear `docs/PLAN.md`, `docs/IMPLEMENTACION.md` y `docs/VALIDACION.md`.
- Actualizar `README.md` con una guia operativa unica.
- Registrar decisiones tecnicas, limitaciones del entorno y criterios de validacion.

### Hito 2. Adecuacion de la aplicacion

- Añadir endpoints y controles necesarios para `health`, `ready` y `metrics`.
- Preparar el `product-service` para identificacion de version y pruebas de degradacion controlada.
- Homogeneizar dependencias de los microservicios para observabilidad y probes avanzadas.

### Hito 3. Cierre de Docker Swarm avanzado

- Extender `docker-stack.yml` con `cAdvisor`, `Prometheus`, `monitoring-net`, `configs` y politica completa de rollout/rollback.
- Añadir configuracion de Prometheus y documentar el procedimiento de validacion Swarm.

### Hito 4. Cierre de Kubernetes avanzado

- Migrar BDs a `StatefulSet` con `Headless Service` y PVC.
- Añadir PVC a Redis y RabbitMQ.
- Aplicar `ConfigMap`, `Secret`, anti-affinity, probes, `resources` y `HPA`.
- Incorporar `Ingress`, `ServiceMonitor` y reglas de alerta.

### Hito 5. Packaging y service mesh

- Crear un Helm chart `shopmicro` parametrizable.
- Añadir manifiestos base de Istio y documentacion de despliegue.

### Hito 6. Validacion y entrega

- Ejecutar validaciones locales sobre los artefactos disponibles.
- Intentar restaurar herramientas faltantes (`git`, `helm`, acceso GitHub) sin bloquear el avance funcional.
- Si la sincronizacion remota no es viable, documentar con precision el bloqueo operativo.

## Principios de implementacion

- Las configuraciones deben ser reproducibles desde repositorio, no dependientes de acciones manuales no documentadas.
- Toda configuracion nueva debe ir acompañada de instrucciones de despliegue y validacion.
- Los ejemplos de secretos en el repositorio se mantendran como valores academicos de laboratorio; el README y la documentacion dejaran claro que deben sustituirse en entornos reales.
- Cuando el entorno local no permita demostrar un requisito de infraestructura, se dejara preparado el artefacto, el procedimiento exacto y la evidencia del bloqueo.

## Riesgos y mitigaciones

- Riesgo: ausencia de `git` local. Mitigacion: intentar localizar o instalar `git`; si no es viable, documentar bloqueo de trazabilidad remota.
- Riesgo: ausencia de `helm`. Mitigacion: generar Helm chart igualmente y validar al menos estructura y render si la herramienta puede instalarse.
- Riesgo: Docker Desktop parado y contexto Kubernetes caido. Mitigacion: reactivar el entorno mas adelante para la fase de validacion; no bloquear la implementacion por ello.
- Riesgo: cluster local mononodo. Mitigacion: dejar anti-affinity y escalado preparados para cluster multinodo y documentar la condicion necesaria para validarlos completamente.
