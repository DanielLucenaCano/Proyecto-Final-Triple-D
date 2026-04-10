# Memoria del Proyecto Avanzado ShopMicro

## Portada

- Título: `PROJECTE DOCKER - Orquestradors: Docker Swarm i Kubernetes Avançat`
- Subtítulo: `Continuació del cas d'ús ShopMicro eCommerce`
- Alumno: `Daniel Lucena Cano`
- Curso: `ASIX / DAW 2025-2026`
- Centro: `Institut Sa Palomera`
- Fecha: `Completar el día de entrega`

## Índice

Este documento está preparado para pasarse a Word o LibreOffice Writer y generar allí el índice automático.

## 1. Introducción del proyecto avanzado

El proyecto avanzado de ShopMicro parte directamente del trabajo realizado en la parte básica. La plataforma ya no se considera un prototipo inicial, sino una base funcional sobre la que deben aplicarse técnicas más cercanas a un entorno productivo real: alta disponibilidad, tolerancia a fallos, escalado automático, gestión de recursos, monitorización centralizada y herramientas de packaging y service mesh.

El objetivo de esta segunda parte no es rehacer el proyecto básico, sino evolucionarlo. Por eso se reaprovecha la arquitectura existente y se amplía con mecanismos avanzados tanto en Docker Swarm como en Kubernetes.

## 2. Situación de partida

La base heredada del proyecto básico incluye:

- Plataforma ShopMicro ya dividida en 10 servicios.
- `docker-compose.yml` funcional para entorno local.
- `docker-stack.yml` preparado para Swarm.
- Despliegue Kubernetes funcional con Deployments, Services, ConfigMaps y Secrets.
- Documentación previa del proyecto básico.

La nueva práctica se desarrolla en una carpeta independiente para no mezclar entregas:

- Ruta de trabajo: [shopmicro2](/C:/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex/shopmicro2/shopmicro2)

## 3. Diferencias clave respecto a la práctica básica

La parte avanzada introduce varios bloques nuevos:

- Docker Swarm avanzado con escalado dinámico, `mode: global`, zero-downtime y rollback.
- Monitorización real con Prometheus, cAdvisor y Grafana.
- Kubernetes con StatefulSets, PVC, anti-affinity y HPA.
- Ingress Controller para centralizar el tráfico.
- Helm como empaquetado estándar de la plataforma.
- Istio como service mesh para controlar tráfico y resiliencia.

## 4. Estrategia de trabajo y documentación

Se mantiene la misma estrategia utilizada en la práctica básica:

- ejecutar el trabajo técnico por fases
- documentar al mismo tiempo los pasos reales realizados
- dejar memorias vivas que se van actualizando
- no atribuir como completado nada que no se haya ejecutado de verdad

Por tanto, esta memoria se irá ampliando conforme se completen las fases del proyecto avanzado.

## 5. Fase 1. Docker Swarm avanzado

### Objetivos de la fase

- Escalado dinámico de servicios críticos
- Despliegue de servicios globales
- Rolling update sin parada
- Rollback automático
- Monitorización con Prometheus y cAdvisor
- Demostración de routing mesh y balanceig intern

### Estado actual

Pendiente de ejecución.

## 6. Fase 2. Kubernetes: alta disponibilidad y monitorización

### Objetivos de la fase

- Migrar bases de datos a StatefulSets
- Añadir Headless Services
- Consolidar PVC, ConfigMaps y Secrets
- Aplicar pod anti-affinity
- Instalar Prometheus + Grafana con Helm

### Estado actual

Pendiente de ejecución.

## 7. Fase 3. Kubernetes: recursos, HPA y balanceo

### Objetivos de la fase

- Añadir requests y limits a todos los contenedores
- Probar OOMKilled controlado
- Configurar escalado manual y automático
- Refinar probes
- Instalar Ingress Controller y crear Ingress para ShopMicro

### Estado actual

Pendiente de ejecución.

## 8. Fase 4. Helm e Istio

### Objetivos de la fase

- Crear un chart Helm propio de ShopMicro
- Validar `helm lint`, `helm template`, `helm install` y `helm upgrade`
- Instalar Istio
- Habilitar sidecar injection
- Configurar `VirtualService` con timeout y retries

### Estado actual

Pendiente de ejecución.

## 9. Conclusión provisional

La práctica avanzada se apoyará en una base ya funcional, lo que permite dedicar el esfuerzo a requisitos realmente avanzados. El siguiente paso consiste en decidir si se empieza por la fase de Swarm avanzado o por la parte de Kubernetes avanzada, en función del estado real de los entornos disponibles.

