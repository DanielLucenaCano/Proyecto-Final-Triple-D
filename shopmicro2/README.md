# ShopMicro Avanzado

Solucion finalizada de la plataforma `ShopMicro` para el proyecto avanzado de Docker Swarm y Kubernetes. El repositorio queda alineado con `pdf_extract_advanced.txt` como fuente de verdad funcional y con la base heredada como punto de partida tecnico.

## Alcance cubierto

- Aplicacion con probes `health` y `ready`, mas endpoint `metrics` en microservicios Python.
- `docker-stack.yml` preparado para Swarm avanzado con `rolling update`, `rollback`, `cAdvisor` y `Prometheus`.
- Manifiestos Kubernetes avanzados con `StatefulSet`, PVC, `podAntiAffinity`, `resources`, `HPA`, `Ingress`, `ServiceMonitor`, `PrometheusRule` e Istio.
- Helm chart propio en `helm/shopmicro`.
- Documentacion operativa y de trazabilidad en `docs/`.

## Estructura relevante

```text
.
|-- api-gateway/
|-- db/
|-- docker-compose.yml
|-- docker-stack.yml
|-- docs/
|-- frontend/
|-- helm/shopmicro/
|-- k8s/
|-- monitoring/
|-- notification-service/
|-- order-service/
|-- product-service/
|-- scripts/
`-- user-service/
```

## Requisitos locales

- Docker Desktop operativo
- `kubectl`
- Minikube si se va a validar Kubernetes localmente
- Helm v3 o v4 para `lint` y `template`

## Ejecucion local con Docker Compose

1. Crear entorno:

```powershell
Copy-Item .env.example .env
```

2. Levantar la plataforma:

```powershell
docker compose up -d --build
```

3. Verificaciones basicas:

```powershell
docker compose ps
Invoke-RestMethod http://127.0.0.1:8081/health
Invoke-RestMethod http://127.0.0.1:8081/api/products | ConvertTo-Json -Depth 6
```

Accesos esperados:

- Frontend: `http://127.0.0.1:8080`
- API Gateway: `http://127.0.0.1:8081`
- RabbitMQ UI: `http://127.0.0.1:15672`

Nota operativa:

- Si se quiere regenerar el catalogo de ejemplo con el SQL corregido, eliminar antes los volumenes de Compose asociados a MySQL.

## Docker Swarm avanzado

El `docker-stack.yml` deja preparada la fase avanzada:

- `product-service` en `4` replicas con politica de `rolling update` y `failure_action: rollback`
- `order-service` y `user-service` escalados a `3` replicas
- `cAdvisor` en modo `global`
- `Prometheus` en red `monitoring-net`
- configuracion de scraping en `monitoring/prometheus-swarm.yml`

Despliegue orientativo:

```powershell
docker swarm init
docker stack deploy -c docker-stack.yml shopmicro
docker service ls
docker service ps shopmicro_product-service
```

## Kubernetes avanzado

Orden recomendado:

```powershell
kubectl apply -f k8s/infra
kubectl apply -f k8s/base
kubectl apply -f k8s/addons/hpa.yaml
kubectl apply -f k8s/addons/ingress.yaml
```

Puntos clave ya modelados:

- `db-products` y `db-orders` migrados a `StatefulSet`
- PVC para BDs, Redis y RabbitMQ
- `shopmicro-config` para configuracion no sensible
- secretos separados de la configuracion
- `podAntiAffinity` obligatoria en `product-service`, `order-service` y `user-service`
- `requests` y `limits` en todos los workloads
- `HPA` para `product-service`
- `Ingress` por host `shopmicro.local`

Recursos que requieren CRDs o componentes previos:

- `k8s/addons/monitoring.yaml` requiere `kube-prometheus-stack`
- `k8s/addons/istio.yaml` requiere Istio instalado

## Helm

Chart disponible en `helm/shopmicro`.

Validacion:

```powershell
helm lint .\helm\shopmicro
helm template shopmicro .\helm\shopmicro --namespace shopmicro
```

Instalacion:

```powershell
helm install shopmicro .\helm\shopmicro -n shopmicro --create-namespace
helm upgrade shopmicro .\helm\shopmicro -n shopmicro --set productService.replicas=4
```

## Monitorizacion e Istio

- `k8s/addons/monitoring.yaml` contiene `ServiceMonitor` y `PrometheusRule`
- `k8s/addons/istio.yaml` contiene `VirtualService` y `DestinationRule`

Instalaciones de referencia:

```powershell
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
```

## Documentacion de entrega

- `docs/PLAN.md`
- `docs/IMPLEMENTACION.md`
- `docs/VALIDACION.md`

## Estado de validacion

Resumen ejecutivo:

- Compose: validado funcionalmente
- Helm: `lint` correcto y `template` renderizado
- Kubernetes: `infra` y `base` aplicados en Minikube; `addons` parcialmente validados
- Bloqueos reales: CRDs de Prometheus Operator e Istio no instalados en el cluster local; intento de multinodo en Minikube condicionado por la red del cluster existente
