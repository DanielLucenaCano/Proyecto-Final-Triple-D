# Validacion

## Objetivo del documento

Este documento centraliza las validaciones realizadas sobre la solucion final. Se separan claramente tres niveles:

- validacion estatica de artefactos
- validacion operativa local
- validacion pendiente por limitacion del entorno

## Estado inicial del entorno

### Herramientas observadas durante la auditoria

- `docker`: instalado, pero daemon no disponible en el momento de la auditoria.
- `kubectl`: instalado.
- `minikube`: instalado.
- `git`: no disponible en `PATH`.
- `gh`: no disponible en `PATH`.
- `helm`: no disponible en `PATH`.

### Impacto inicial

- No fue posible validar de inmediato despliegues Docker o Kubernetes.
- No fue posible de inmediato crear commits locales ni sincronizar con GitHub.

## Matriz de validacion

| Ambito | Validacion prevista | Estado |
|---|---|---|
| Aplicacion | Endpoints `health`, `ready`, `metrics` | Validado |
| Docker Compose | Arranque y comprobacion funcional | Validado |
| Docker Swarm | Revision declarativa y validacion si hay cluster | Parcial |
| Kubernetes | `kubectl apply --dry-run`, despliegue y comprobacion | Parcial |
| Helm | `helm lint` y render del chart | Validado |
| Git | Inicializacion, commits y estado limpio | Validado |
| GitHub | Creacion de remoto, push y sincronizacion | Bloqueado por autenticacion |

## Evidencias y bloqueos

### Bloqueos iniciales registrados

- Falta de `git` local para trazabilidad de commits.
- Falta de `helm` local para validacion del chart.
- Docker Desktop no activo al inicio.
- API de Kubernetes inaccesible al inicio.

### Actualizacion esperada

- Este documento se ira completando por hito con comandos ejecutados, resultado y accion correctiva cuando aplique.

## Validaciones ejecutadas

### Hito 2. Sintaxis Python

- `py_compile` correcto sobre:
  - `product-service/app.py`
  - `order-service/app.py`
  - `user-service/app.py`
  - `notification-service/app.py`
- Resultado: sin errores de sintaxis tras introducir observabilidad y probes avanzadas.

### Hito 3. Helm

- `helm lint` sobre `helm/shopmicro`: correcto.
- `helm template` sobre `helm/shopmicro`: renderizado correcto.
- Incidencia menor: `helm` no quedo en `PATH` tras la instalacion por `winget`; la validacion se ejecuto con ruta absoluta al binario instalado.

### Hito 4. Kubernetes declarativo

- `kubectl apply --dry-run=client --validate=false -f k8s/infra`: correcto.
- `kubectl apply --dry-run=client --validate=false -f k8s/base`: correcto.
- `kubectl apply --dry-run=client --validate=false -f k8s/addons`: correcto para `HPA` e `Ingress`; bloqueo esperado en recursos `ServiceMonitor`, `PrometheusRule`, `VirtualService` y `DestinationRule` por ausencia de CRDs.

### Hito 5. Kubernetes en Minikube

- Minikube arrancado correctamente sobre Docker.
- `k8s/infra` aplicado en cluster: correcto.
- `k8s/base` aplicado en cluster: correcto.
- `StatefulSet` `db-products` y `db-orders`: creados y en ejecucion.
- PVC observados en estado `Bound`:
  - `cache-data`
  - `message-queue-data`
  - `data-db-products-0`
  - `data-db-orders-0`
- Intento de ampliar Minikube a tres nodos: ejecutado.
- Resultado del multinodo: los nodos adicionales quedaron `NotReady`; Minikube advirtio que el cluster original se habia creado sin CNI, por lo que la validacion completa de `podAntiAffinity` multinodo quedo condicionada por esa limitacion de red del entorno local.

### Hito 6. Docker Compose funcional

- `docker compose up -d --build`: correcto tras corregir el `healthcheck` de Nginx.
- `docker compose ps`: servicios principales en estado `healthy`.
- `GET http://127.0.0.1:8081/health`: correcto.
- `GET http://127.0.0.1:8081/api/products`: correcto; devuelve `version: 2.0.0` en `product-service`.
- `POST http://127.0.0.1:8081/api/orders`: correcto.
- `notification-service` registra `Notification sent for order 1`.
- Validacion interna de probes y metricas:
  - `product-service /ready`: correcto.
  - `order-service /ready`: correcto.
  - `notification-service /ready`: correcto.
  - `product-service /metrics`: expone `shopmicro_http_requests_total` y `shopmicro_http_request_duration_seconds`.

### Hito 7. Git y GitHub

- Repositorio Git local inicializado correctamente.
- Historial local generado con commits atomicos.
- `git status --short --branch`: limpio tras los commits.
- `gh auth status`: fallo por ausencia de login en GitHub CLI.
- Bloqueo exacto para sincronizacion remota:
  - no existe sesion autenticada en `gh`
  - el conector GitHub disponible no ofrece creacion de repositorio nuevo
  - en consecuencia no fue posible crear remoto, hacer `push` ni vincular el proyecto automaticamente
