# Memoria Operativa del Proyecto Avanzado ShopMicro

## 0. Control documental

- Proyecto: `PROJECTE DOCKER - Orquestradors: Docker Swarm i Kubernetes Avançat`
- Caso de uso: `ShopMicro e-Commerce`
- Alumno: `Daniel Lucena Cano`
- Curso: `ASIX / DAW 2025-2026`
- Fecha de apertura de esta memoria: `2026-04-10`
- Estado del documento: `Activo`

## 1. Propósito de esta memoria

Esta memoria se crea como documento independiente para registrar la ejecución del proyecto avanzado a partir del baseline ya existente del proyecto básico. Su objetivo es consolidar, con trazabilidad técnica y criterio de entrega, todo lo que se vaya implementando a partir de este punto.

Esta memoria no sustituye a la documentación previa. La complementa y se orienta específicamente a:

- registrar decisiones técnicas del proyecto avanzado;
- documentar evidencias por ejercicio y por fase;
- dejar constancia de incidencias, validaciones y resultados;
- servir de base para el PDF final y para la presentación.

## 2. Punto de partida auditado

Tras la revisión inicial del repositorio y del enunciado avanzado, el estado del proyecto se resume así:

- Existe una base funcional heredada del proyecto básico.
- El repositorio incluye `docker-compose.yml`, `docker-stack.yml`, manifiestos Kubernetes y documentación previa.
- El enunciado avanzado ya ha sido extraído a texto para trabajo operativo en `docs/enunciado-extraido.txt`.
- La base actual es válida como plataforma de arranque, pero no cubre todavía de forma íntegra los requisitos avanzados.

## 3. Diagnóstico ejecutivo inicial

### 3.1. Capacidades ya disponibles

- Arquitectura ShopMicro definida con 10 servicios.
- Base Docker Compose operativa a nivel de diseño.
- Base Docker Swarm preparada mediante `docker-stack.yml`.
- Base Kubernetes ya modelada en YAML y parcialmente documentada.
- Documentación previa reutilizable para memoria final.

### 3.2. Brechas detectadas frente al enunciado avanzado

- No consta cerrada la fase avanzada de Swarm con evidencia completa de escalado dinámico, `rolling update`, `rollback`, `cAdvisor`, `Prometheus`, `routing mesh` y validación de alta disponibilidad.
- En Kubernetes, `db-products` y `db-orders` siguen planteadas como `Deployment` en lugar de `StatefulSet`.
- No se ha consolidado persistencia real con `PersistentVolumeClaim` para todos los servicios con estado.
- No están implementadas todavía las reglas de `pod anti-affinity` exigidas para servicios críticos.
- No están formalizados `resources.requests`, `resources.limits`, `HPA`, `Ingress`, `Helm` ni `Istio`.
- Los microservicios actuales no exponen todavía todas las rutas necesarias para la fase avanzada, especialmente `/ready` y un endpoint formal de métricas.

## 4. Estado operativo a fecha 2026-04-10

### 4.1. Infraestructura del usuario

- El usuario confirma que dispone ya del clúster Docker Swarm con las máquinas virtuales requeridas para la parte avanzada.
- La ejecución real de las pruebas de Swarm se realizará sobre dichas máquinas virtuales.

### 4.2. Estado de esta estación de trabajo

- En esta sesión no hay binario `git` disponible en el `PATH`.
- En esta sesión tampoco había runtime Docker/Kubernetes activo en local durante la auditoría inicial.

Conclusión operativa:

- Podemos preparar documentación, estructura, cambios de código y estrategia de publicación.
- Para publicar en GitHub desde esta estación necesitaremos habilitar `git` o, alternativamente, trabajar contra un repositorio remoto ya provisionado por otra vía.

## 5. Estrategia de ejecución acordada

La ejecución del proyecto seguirá esta línea:

1. Consolidar la base documental y de repositorio.
2. Publicar el proyecto en GitHub con una estructura limpia y trazable.
3. Ejecutar el proyecto avanzado por ejercicios, uno a uno.
4. Documentar cada bloque según se complete, sin diferir la memoria al cierre.

## 6. Plan maestro de implementación

### Fase 1. Docker Swarm Avanzado

Objetivo:

- cerrar escalado dinámico;
- desplegar `cAdvisor` y `Prometheus`;
- demostrar `rolling update`, `rollback`, `routing mesh` y alta disponibilidad.

Entregables internos:

- actualización de `docker-stack.yml`;
- configuración de Prometheus;
- evidencias de comandos y capturas;
- validación funcional de `product-service` y `order-service`.

### Fase 2. Kubernetes: Alta Disponibilidad y Monitorización

Objetivo:

- migrar bases de datos a `StatefulSet`;
- introducir `PVC`;
- separar `ConfigMaps` y `Secrets`;
- aplicar `anti-affinity`;
- desplegar `kube-prometheus-stack` y `Grafana`.

Entregables internos:

- nuevos manifiestos Kubernetes;
- evidencia de persistencia y naming estable;
- dashboards y métricas del namespace `shopmicro`.

### Fase 3. Kubernetes: Recursos, Escalado y Balanceo

Objetivo:

- fijar `requests/limits`;
- activar `HPA`;
- refinar `liveness/readiness`;
- desplegar `Ingress`.

Entregables internos:

- manifiestos actualizados;
- pruebas de `OOMKilled`, `scale-out`, `scale-in` y retirada del balanceo;
- exposición funcional por `Ingress`.

### Fase 4. Kubernetes: Helm e Istio

Objetivo:

- empaquetar la solución en Helm;
- activar `Istio`;
- aplicar `VirtualService` y `DestinationRule`;
- validar observabilidad y control de tráfico.

Entregables internos:

- chart Helm reutilizable;
- configuración Istio documentada;
- evidencias en Kiali.

## 7. Criterio de trabajo a partir de ahora

Regla operativa:

- no se cerrará ningún ejercicio sin evidencia mínima, validación técnica y actualización documental.

Cada ejercicio deberá dejar:

- cambio técnico implementado;
- comando o procedimiento ejecutado;
- resultado observado;
- incidencia, si aplica;
- conclusión breve.

## 8. Próximo hito

El siguiente hito es dejar resuelta la capa de repositorio:

- verificar disponibilidad real de Git o definir mecanismo alternativo de publicación;
- vincular el proyecto a GitHub;
- iniciar la trazabilidad de cambios antes de comenzar la ejecución técnica del primer ejercicio.
