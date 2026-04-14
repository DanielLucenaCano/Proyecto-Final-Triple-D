# Kubernetes ShopMicro

## Estructura

- `infra/`: namespace, configuracion compartida, BDs, Redis y RabbitMQ
- `base/`: frontend, gateway y microservicios de negocio
- `addons/`: `HPA`, `Ingress`, monitorizacion e Istio

## Orden de despliegue

```powershell
kubectl apply -f k8s/infra
kubectl apply -f k8s/base
kubectl apply -f k8s/addons/hpa.yaml
kubectl apply -f k8s/addons/ingress.yaml
```

Aplicar solo cuando los componentes externos existan:

```powershell
kubectl apply -f k8s/addons/monitoring.yaml
kubectl apply -f k8s/addons/istio.yaml
```

## Requisitos externos

- `monitoring.yaml` requiere CRDs de `kube-prometheus-stack`
- `istio.yaml` requiere Istio instalado e inyeccion de sidecar habilitada si se quiere validar el mesh

## Comprobaciones

```powershell
kubectl get pods -n shopmicro -o wide
kubectl get pvc -n shopmicro
kubectl get deployments,statefulsets,svc -n shopmicro
kubectl get hpa -n shopmicro
kubectl get ingress -n shopmicro
```
