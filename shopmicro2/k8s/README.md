# Kubernetes

Aplicación recomendada:

```bash
kubectl apply -f k8s/infra/namespace.yaml
kubectl apply -f k8s/infra/
kubectl apply -f k8s/base/
kubectl get pods -n shopmicro
kubectl get services -n shopmicro
```

Todos los recursos usan el namespace `shopmicro`.

