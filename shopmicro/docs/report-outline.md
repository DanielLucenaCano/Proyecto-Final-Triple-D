# Guion para el PDF final

## 1. Portada

- Título del proyecto.
- Nombre del alumno o equipo.
- Curso ASIX/DAW 2025-2026.
- Fecha de entrega.

## 2. Índice automático

- Generado desde Word o Writer.

## 3. Introducción teórica

- Docker Compose: arquitectura, sintaxis YAML, diferencias con `docker run`.
- Docker Swarm: manager, worker, consenso Raft, VIP y réplicas.
- Kubernetes: pods, deployments, services, configmaps, secrets, probes.

## 4. Arquitectura diseñada

- Inserta el diagrama Mermaid de `docs/architecture.mmd`.
- Explica redes, volúmenes, servicios y puertos expuestos.

## 5. Fase 1. Docker Compose

- Decisiones de diseño.
- Bloques de código con `docker-compose.yml`, Dockerfiles y configuración Nginx.
- Capturas: `docker compose up -d`, `docker compose ps`, logs y prueba de flujos.

## 6. Fase 2. Docker Swarm

- Creación del clúster de 3 nodos.
- Descripción de `docker-stack.yml`.
- Capturas: `docker node ls`, `docker stack services shopmicro`, `docker stack ps shopmicro`.
- Prueba de caída de `worker-2` y redistribución.
- Escalado en caliente de `product-service`.

## 7. Fase 3. Seguridad

- Vulnerabilidades iniciales detectadas.
- Migración a Docker Secrets.
- Aislamiento de redes overlay.
- Explicación del TLS interno de Swarm.
- Resultado del escaneo con Docker Scout o Trivy.

## 8. Fase 4. Kubernetes

- Comparativa Swarm vs Kubernetes.
- Instalación de Minikube o k3s.
- Aplicación de manifiestos en `k8s/`.
- Capturas: `kubectl get pods`, `kubectl get services`, `kubectl describe deployment product-service`.
- Rolling update documentado.
- Validación de los tres flujos funcionales.

## 9. Conclusiones

- Qué solución encaja mejor en desarrollo, preproducción y producción.
- Problemas encontrados y aprendizajes.

