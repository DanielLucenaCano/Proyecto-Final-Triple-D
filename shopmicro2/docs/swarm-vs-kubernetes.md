# Comparativa Docker Swarm vs Kubernetes

| Aspecto | Docker Swarm | Kubernetes | Aplicación a ShopMicro |
|---|---|---|---|
| Escalado | Muy simple con `docker service scale` | Más flexible con Deployments y HPA | Swarm es ideal para preproducción rápida; Kubernetes gana si el proyecto crece |
| Self-healing | Reprograma tareas si cae un nodo o contenedor | Reconciliación continua con controladores | Kubernetes da más control fino sobre recuperación |
| Rolling updates | `update_config` sencillo | Estrategias declarativas más completas | Kubernetes documenta mejor cambios graduales |
| Secrets | Docker Secrets integrados en Swarm | Secrets nativos, integrables con gestores externos | Ambos cubren el caso, Kubernetes escala mejor |
| Networking | Overlay simple y directo | Más potente, pero más complejo | Swarm es más fácil de explicar; Kubernetes es más completo |
| Operación | Curva de entrada baja | Mayor complejidad operativa | Para clase, Swarm permite entender HA; para producción, Kubernetes encaja mejor |

