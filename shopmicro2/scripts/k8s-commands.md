# Comandos guía para Kubernetes

```bash
kubectl apply -f k8s/infra/namespace.yaml
kubectl apply -f k8s/infra/
kubectl apply -f k8s/base/

kubectl get pods -n shopmicro
kubectl get services -n shopmicro
kubectl describe deployment product-service -n shopmicro
kubectl logs deployment/notification-service -n shopmicro
```

## Rolling update de ejemplo

```bash
kubectl set image deployment/product-service product-service=shopmicro/product-service:1.1.0 -n shopmicro
kubectl rollout status deployment/product-service -n shopmicro
kubectl rollout history deployment/product-service -n shopmicro
```

