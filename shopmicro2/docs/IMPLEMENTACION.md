# Implementacion

## Objetivo del documento

Este documento registra la ejecucion real del trabajo sobre el repositorio. Su funcion es dejar trazabilidad de decisiones, cambios aplicados y limitaciones encontradas durante la conversion de la base actual en la solucion final del proyecto avanzado.

## Decision 1. Directorio raiz de trabajo

- Se adopta `shopmicro2/` como raiz efectiva del proyecto.
- El directorio superior solo contiene el repositorio de trabajo y el requisito funcional extraido a texto.

## Decision 2. Prioridad de cierre

- Primero se corrige la base tecnica para satisfacer el PDF avanzado.
- Despues se refuerza la validacion y se consolida la documentacion.
- La publicacion en GitHub se intentara al final de cada hito siempre que las herramientas del entorno lo permitan.

## Bitacora de ejecucion

### Auditoria inicial

- Se identifico `pdf_extract_advanced.txt` como fuente de verdad funcional.
- Se detecto ausencia de repositorio Git inicializado en `shopmicro2/`.
- Se detecto ausencia de `git`, `gh` y `helm` en `PATH`.
- Se detecto Docker Desktop no operativo durante la auditoria.
- Se detecto contexto `kubectl` apuntando a `minikube`, pero sin API accesible en ese momento.

### Brechas funcionales registradas

- Swarm avanzado incompleto: monitorizacion, configuracion de rollback y evidencias operativas.
- Kubernetes avanzado incompleto: `StatefulSet`, PVC, `anti-affinity`, `resources`, `HPA`, `Ingress`, monitorizacion y alertas.
- Helm e Istio ausentes.
- Documentacion heredada desalineada con una entrega final.

## Registro de cambios

### Hito 1. Base documental

- Creado `docs/PLAN.md`.
- Creado este fichero `docs/IMPLEMENTACION.md`.
- Creado `docs/VALIDACION.md`.

### Hito 2. Observabilidad y probes en microservicios

- Se añadieron endpoints `GET /ready` y `GET /metrics` a `product-service`, `order-service`, `user-service` y `notification-service`.
- Se normalizo `GET /health` para soportar simulacion controlada de fallo mediante variables `SIMULATE_HEALTH_FAILURE` y `SIMULATE_READY_FAILURE`.
- Se incorporo instrumentacion Prometheus con contador de peticiones y latencia HTTP.
- Se homogenearon versiones de aplicacion por variable de entorno para facilitar rolling updates y validaciones de despliegue.
- Decision: la simulacion de fallo se resuelve por variables de entorno porque permite demostrar probes en Kubernetes sin bifurcar codigo ni mantener ramas de prueba.

### Hito 3. Kubernetes avanzado

- Se introdujo `shopmicro-config` como `ConfigMap` comun de entorno.
- `db-products` y `db-orders` se migraron a `StatefulSet` con `Headless Service` y `volumeClaimTemplates`.
- Redis y RabbitMQ pasaron a persistencia declarativa con PVC.
- Se añadieron `resources.requests` y `resources.limits` a todos los workloads.
- Se convirtieron `frontend` y `api-gateway` a `ClusterIP` para trabajar con `Ingress`.
- Se incorporaron `podAntiAffinity` obligatorias en `product-service`, `order-service` y `user-service`.
- Se añadieron `HPA`, `Ingress`, `ServiceMonitor`, `PrometheusRule`, `VirtualService` y `DestinationRule`.
- Decision: se separaron los recursos dependientes de CRDs en `k8s/addons` para poder desplegar la base aun cuando Prometheus Operator o Istio no esten instalados.

### Hito 4. Swarm avanzado

- `docker-stack.yml` se reescribio para incluir `cAdvisor`, `Prometheus`, `monitoring-net` y configuracion de `rollback`.
- `product-service` quedo promovido a version `2.0.0` en Swarm para cubrir el requisito de actualizacion avanzada.
- Se añadió `monitoring/prometheus-swarm.yml` para centralizar scraping de `cAdvisor` y microservicios.
- Decision: la monitorizacion de Swarm se mantuvo ligera y declarativa para que pueda desplegarse sin introducir dependencias ajenas al enunciado.

### Hito 5. Helm chart

- Se creo `helm/shopmicro` como chart propio del proyecto.
- Se parametrizaron replicas, imagenes, secretos, recursos, `HPA`, `Ingress`, monitorizacion e Istio.
- Decision: el chart se fragmento en plantillas pequeñas para priorizar mantenibilidad y trazabilidad frente a un template monolitico.

### Hito 6. Correcciones de validacion

- Se corrigio el `healthcheck` de Nginx en `docker-compose.yml` para evitar falsos negativos por binarios no presentes en `nginx:alpine`.
- Se normalizo el SQL de ejemplo de `db/products-init/01-schema.sql` para eliminar textos mal codificados en nuevos despliegues.

### Hito 7. Intento de sincronizacion GitHub

- Se inicializo el repositorio Git local y se ordeno el historial en commits atomicos.
- Se instalo `gh` localmente.
- Se verifico que `gh auth status` falla por ausencia de sesion autenticada.
- Se verifico que el conector GitHub disponible en la sesion permite lectura y operaciones sobre repositorios existentes, pero no expone creacion de repositorio remoto nuevo.
- Decision: se cierra la entrega con historial local completo y se documenta el bloqueo de autenticacion como causa de no sincronizacion remota.

### Hitos siguientes

- Pendiente de actualizacion durante la ejecucion.
