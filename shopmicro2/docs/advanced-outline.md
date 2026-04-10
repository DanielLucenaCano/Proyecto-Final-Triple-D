# Guion de la práctica avanzada

## Proyecto

- Título: `PROJECTE DOCKER - Orquestradors: Docker Swarm i Kubernetes Avançat`
- Caso de uso: `Continuació del cas d'ús ShopMicro eCommerce`
- Alumno: `Daniel Lucena Cano`
- Curso: `ASIX / DAW 2025-2026`

## Estructura del documento final

1. Portada
2. Índice automático
3. Introducción del proyecto avanzado
4. Situación de partida: herencia del proyecto básico
5. Fase 1. Docker Swarm avanzado
6. Fase 2. Kubernetes: alta disponibilidad y monitorización
7. Fase 3. Kubernetes: recursos, autoescalado y balanceo
8. Fase 4. Kubernetes: herramientas complementarias
9. Conclusiones
10. Anexos de código y manifiestos

## Fase 1. Docker Swarm avanzado

- Escalado dinámico por servicio
- Escalado global con `cadvisor`
- Rolling update y rollback
- Monitorización con Prometheus + cAdvisor
- Routing mesh, VIP y alta disponibilidad teórica del plano de control

## Fase 2. Kubernetes: alta disponibilidad y monitorización

- Migración de bases de datos a StatefulSets
- Headless Services
- PVC, ConfigMaps y Secrets por entorno
- Pod anti-affinity
- Monitorización con Prometheus + Grafana vía Helm

## Fase 3. Kubernetes: recursos, escalado y balanceo

- Requests y Limits
- OOMKilled controlado
- Escalado manual y HPA
- Liveness y Readiness probes avanzadas
- Ingress Controller con `shopmicro.local`

## Fase 4. Herramientas complementarias

- Helm chart propio de ShopMicro
- Upgrade del chart
- Istio sidecar injection
- VirtualService con timeout y retries

