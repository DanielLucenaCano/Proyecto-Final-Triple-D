# Memoria del Proyecto ShopMicro

## Portada

- Título: `PROJECTE DOCKER - Orquestradors: Docker Swarm i Kubernetes`
- Subtítulo: `Cas d'ús: Plataforma e-Commerce Microserveis - ShopMicro`
- Alumno: `Daniel Lucena Cano`
- Curso: `ASIX / DAW 2025-2026`
- Centro: `Institut Sa Palomera`
- Fecha: `Completar el día de entrega`

## Índice

Este documento está preparado para exportarse después a Word o LibreOffice Writer y generar allí el índice automático.

## 1. Introducción del proyecto

El objetivo del proyecto ShopMicro es diseñar, contenerizar y orquestar una plataforma e-Commerce basada en microservicios, siguiendo una evolución progresiva desde Docker Compose hasta Docker Swarm y Kubernetes. El caso de uso propuesto reproduce una arquitectura realista en la que los servicios están desacoplados, utilizan componentes especializados y deben comunicarse entre sí de forma fiable.

La finalidad principal no es desarrollar una lógica de negocio compleja, sino demostrar una arquitectura multicontenedor correcta, una orquestación coherente y una documentación técnica clara. Por este motivo, los microservicios desarrollados en este proyecto implementan únicamente la lógica mínima necesaria para validar los flujos funcionales exigidos.

## 2. Objetivo general y alcance

El objetivo general ha sido construir una base funcional de la plataforma ShopMicro que permita:

- Ejecutar todos los servicios localmente con Docker Compose.
- Preparar el despliegue a Docker Swarm mediante un `docker-stack.yml`.
- Preparar la capa de seguridad de Swarm mediante secretos y segmentación de red.
- Preparar la migración futura a Kubernetes con manifiestos YAML separados por recurso.

Hasta el momento, el trabajo realizado cubre de forma práctica la fase 1 y deja preparada la base técnica de las fases 2, 3 y 4. Las partes no ejecutadas todavía se indican explícitamente en esta memoria para no atribuir como realizadas acciones que aún están pendientes.

## 3. Caso de uso: ShopMicro

ShopMicro es una tienda online ficticia especializada en productos tecnológicos. La aplicación se ha planteado como un conjunto de microservicios independientes para mejorar la escalabilidad, la separación de responsabilidades y la facilidad de despliegue.

Los servicios definidos en el proyecto son los siguientes:

| Servicio | Tecnología | Función |
|---|---|---|
| `frontend` | Nginx + HTML/CSS/JS | Interfaz web de la tienda |
| `api-gateway` | Nginx | Punto de entrada único a la API |
| `product-service` | Python Flask | Consulta y gestión de productos |
| `order-service` | Python Flask | Creación y consulta de pedidos |
| `user-service` | Python Flask | Gestión de usuarios y autenticación JWT |
| `notification-service` | Python Flask | Consumidor de eventos desde RabbitMQ |
| `db-products` | MySQL 8 | Base de datos de catálogo |
| `db-orders` | MySQL 8 | Base de datos de pedidos y usuarios |
| `cache` | Redis 7 | Caché temporal de consultas frecuentes |
| `message-queue` | RabbitMQ 3 | Cola de mensajería interna |

## 4. Arquitectura de la solución

La arquitectura se ha diseñado en tres niveles de red para reforzar el aislamiento lógico entre servicios:

- `public-net`: conecta únicamente `frontend` y `api-gateway`.
- `service-net`: conecta `api-gateway` con los microservicios de aplicación.
- `data-net`: conecta microservicios con MySQL, Redis y RabbitMQ.

Esta segmentación evita que todos los contenedores compartan la misma red y se alinea con el criterio del enunciado de separar servicios por función y exposición.

### 4.1. Flujo de comunicación

1. El usuario accede al `frontend`.
2. El `frontend` envía las peticiones de API al `api-gateway`.
3. El `api-gateway` enruta cada petición al microservicio correspondiente.
4. `product-service` consulta Redis y, si no encuentra caché, consulta MySQL.
5. `order-service` descuenta stock, registra el pedido y publica un evento en RabbitMQ.
6. `notification-service` consume el evento y registra la notificación.

### 4.2. Diagrama de arquitectura

El diagrama Mermaid del proyecto se encuentra en el archivo [architecture.mmd](/C:/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex/shopmicro/docs/architecture.mmd). En el documento final debe insertarse como figura numerada.

Texto de pie de figura recomendado:

`Figura 1. Arquitectura lógica de ShopMicro con separación por redes y servicios.`

## 5. Introducción teórica de las tecnologías utilizadas

### 5.1. Docker Compose

Docker Compose permite definir aplicaciones multicontenedor en un único fichero YAML. Cada servicio se declara con su imagen o contexto de build, variables de entorno, puertos, redes, volúmenes y dependencias. Su principal ventaja frente a `docker run` es que la infraestructura queda descrita como código, lo que facilita la repetibilidad, la lectura del despliegue y el mantenimiento del proyecto.

En este proyecto se ha utilizado Docker Compose como entorno de desarrollo local, permitiendo levantar toda la plataforma con un único comando y verificando que todos los servicios son capaces de comunicarse entre sí.

### 5.2. Docker Swarm

Docker Swarm es la solución de orquestación nativa de Docker. Organiza los nodos en managers y workers, distribuye servicios replicados y permite actualizaciones progresivas, restart policies y placement constraints. Su integración con Docker lo hace adecuado para entornos de laboratorio o preproducción, donde se valora especialmente la simplicidad operativa.

En ShopMicro se ha preparado un `docker-stack.yml` con réplicas, restricciones de ubicación y soporte para secrets, con el objetivo de migrar la solución de Compose a un clúster Swarm de al menos tres nodos.

### 5.3. Kubernetes

Kubernetes es una plataforma de orquestación más avanzada y flexible que Docker Swarm. Trabaja con objetos declarativos como Pods, Deployments, Services, ConfigMaps, Secrets y Namespaces. Entre sus principales capacidades se encuentran el self-healing, el rolling update controlado y la posibilidad de desacoplar configuración y credenciales.

En este proyecto se ha dejado preparada la base de migración a Kubernetes mediante manifiestos YAML separados por infraestructura y servicios, aunque la ejecución real del clúster queda pendiente.

## 6. Estructura del proyecto

La estructura principal generada es la siguiente:

```text
shopmicro/
|-- api-gateway/
|-- frontend/
|-- product-service/
|-- order-service/
|-- user-service/
|-- notification-service/
|-- db/
|-- docs/
|-- k8s/
|-- scripts/
|-- .env.example
|-- .gitignore
|-- docker-compose.yml
`-- docker-stack.yml
```

## 7. Fase 1: Docker Compose - Entorno de desarrollo

### 7.1. Objetivo de la fase

El objetivo de esta fase ha sido disponer de un entorno local completamente funcional con todos los servicios del caso de uso ShopMicro ejecutándose en contenedores independientes.

### 7.2. Decisiones de diseño adoptadas

Para esta fase se tomaron las siguientes decisiones:

- Usar Flask en los microservicios por su sencillez y rapidez de desarrollo.
- Usar Nginx en el `frontend` y en `api-gateway` para separar claramente capa visual y reverse proxy.
- Mantener dos bases de datos diferenciadas:
  `db-products` para catálogo y `db-orders` para pedidos y usuarios.
- Usar Redis exclusivamente como caché temporal para el listado de productos.
- Usar RabbitMQ para desacoplar la notificación del flujo principal del pedido.
- Separar redes internas para evitar una topología plana.

### 7.3. Archivo `docker-compose.yml`

El despliegue local se ha definido en el archivo [docker-compose.yml](/C:/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex/shopmicro/docker-compose.yml). Este fichero incluye:

- Los diez servicios exigidos en el enunciado.
- `build` para los servicios propios y `image` para servicios de infraestructura.
- Variables de entorno para bases de datos, JWT y mensajería.
- Volúmenes persistentes para MySQL y RabbitMQ.
- `depends_on` con `condition: service_healthy`.
- `healthcheck` para servicios críticos.
- Redes separadas para frontend, microservicios y datos.

Fragmento representativo:

```yaml
services:
  frontend:
    build:
      context: ./frontend
    ports:
      - "8080:80"
    depends_on:
      api-gateway:
        condition: service_healthy
    networks:
      - public-net

  product-service:
    build:
      context: ./product-service
    environment:
      DB_HOST: db-products
      DB_NAME: ${PRODUCTS_DB}
      DB_USER: ${PRODUCTS_DB_USER}
      REDIS_HOST: cache
    depends_on:
      db-products:
        condition: service_healthy
      cache:
        condition: service_healthy
    networks:
      - service-net
      - data-net
```

En el documento final debe insertarse el fichero completo en bloque monoespaciado.

### 7.4. Microservicios implementados

#### `frontend`

El frontend se ha desarrollado como una aplicación estática servida por Nginx. Permite:

- Consultar el catálogo.
- Visualizar nombre, descripción, precio y stock.
- Crear pedidos desde un formulario.
- Seleccionar el producto por nombre en un desplegable.
- Generar automáticamente el `user_id` en el navegador mediante `localStorage`.

#### `api-gateway`

El gateway implementa el punto de entrada único a la API y enruta:

- `/api/products` hacia `product-service`
- `/api/orders` hacia `order-service`
- `/api/users/register` y `/api/users/login` hacia `user-service`

#### `product-service`

Este servicio permite listar, crear, modificar y eliminar productos. El flujo de consulta implementado es:

1. Comprobar si la clave `products:all` existe en Redis.
2. Si existe, devolver los datos desde caché.
3. Si no existe, consultar MySQL.
4. Convertir el precio a formato serializable.
5. Guardar el resultado en Redis con TTL de 60 segundos.

#### `order-service`

Este servicio crea pedidos y ejecuta el siguiente flujo:

1. Recibe el producto y la cantidad.
2. Llama internamente a `product-service` para descontar stock.
3. Inserta el pedido en `db-orders`.
4. Publica un evento en la cola `order_events`.

#### `user-service`

Este servicio permite registrar usuarios y generar tokens JWT para autenticación.

#### `notification-service`

Este servicio escucha eventos en RabbitMQ y registra por log la notificación simulada de pedido creado.

### 7.5. Inicialización de bases de datos

Se han definido scripts SQL iniciales:

- [db/products-init/01-schema.sql](/C:/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex/shopmicro/db/products-init/01-schema.sql)
- [db/orders-init/01-schema.sql](/C:/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex/shopmicro/db/orders-init/01-schema.sql)

Estos scripts crean las tablas necesarias y cargan datos de ejemplo para facilitar las pruebas.

### 7.6. Comandos de despliegue utilizados

En WSL se utilizó el siguiente flujo:

```bash
cd ~/Codex/shopmicro
cp .env.example .env
docker compose up -d --build
docker compose ps
docker compose logs -f
```

### 7.7. Incidencias detectadas y correcciones realizadas

Durante la puesta en marcha de la fase 1 se detectaron varias incidencias reales, que fueron resueltas:

#### Incidencia 1. Error de serialización JSON en `product-service`

Al consultar productos, MySQL devolvía el campo `price` como tipo `Decimal`, y Python no podía serializarlo directamente al almacenar la respuesta en Redis.

Solución aplicada:

- Se añadió una función de normalización para convertir `Decimal` a `float`.

#### Incidencia 2. Error de autenticación PyMySQL con MySQL 8

El contenedor de `product-service` devolvía el error:

```text
RuntimeError: 'cryptography' package is required for sha256_password or caching_sha2_password auth methods
```

Solución aplicada:

- Se añadió la dependencia `cryptography` a:
  - `product-service/requirements.txt`
  - `order-service/requirements.txt`
  - `user-service/requirements.txt`

#### Incidencia 3. Mejora de la experiencia de usuario del frontend

El formulario original exigía introducir manualmente el ID de producto y el ID de usuario.

Mejora aplicada:

- Sustitución del campo `product_id` por un selector basado en nombre de producto.
- Generación automática del `user_id` en el navegador.

### 7.8. Verificación funcional realizada

A nivel funcional, se ha verificado lo siguiente:

- El `frontend` se sirve correctamente en `http://localhost:8080`.
- El `api-gateway` responde correctamente en `http://localhost:8081/health`.
- RabbitMQ es accesible en `http://localhost:15672`.
- La consulta de productos funciona y puede devolver datos desde caché.
- El formulario del frontend permite crear pedidos de manera más usable.

Capturas pendientes de insertar en el documento final:

- `Figura 2. docker compose ps con todos los servicios levantados.`
- `Figura 3. Pantalla principal del frontend con productos cargados.`
- `Figura 4. Respuesta correcta de /api/products.`
- `Figura 5. Logs de notification-service tras crear un pedido.`

### 7.9. Estado actual de la Fase 1

La fase 1 puede considerarse funcional a nivel de arquitectura y de flujo local. Quedan pendientes únicamente las capturas finales y, si se desea, una validación más exhaustiva del flujo completo de pedido con evidencia visual paso a paso.

## 8. Fase 2: Docker Swarm - Clúster de alta disponibilidad

### 8.1. Trabajo realizado

La fase 2 no se ha ejecutado todavía sobre un clúster real de tres nodos, pero sí se ha preparado técnicamente:

- Se creó el archivo [docker-stack.yml](/C:/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex/shopmicro/docker-stack.yml).
- Se definieron réplicas para los microservicios.
- Se añadieron `placement.constraints` para ubicar bases de datos y servicios críticos en el manager.
- Se añadieron `restart_policy` y `update_config`.
- Se preparó una guía de comandos en [scripts/swarm-commands.md](/C:/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex/shopmicro/scripts/swarm-commands.md).

### 8.2. Decisiones de diseño en Swarm

Se decidió que:

- Los servicios de API tengan como mínimo 2 réplicas.
- Las bases de datos y RabbitMQ residan en el manager para simplificar persistencia y consistencia en un entorno académico.
- La actualización se realice con paralelismo 1.

### 8.3. Estado actual de la Fase 2

La fase 2 está preparada a nivel de configuración, pero no documentada todavía con:

- `docker node ls`
- `docker stack services shopmicro`
- `docker stack ps shopmicro`
- caída y recuperación de un worker
- escalado en caliente de `product-service`

Por tanto, en el documento final esta fase debe presentarse como `preparada, pero pendiente de ejecución real`.

## 9. Fase 3: Seguridad en Docker Swarm

### 9.1. Trabajo realizado

Se ha preparado la base de seguridad en Swarm:

- Se definieron secretos en `docker-stack.yml`.
- Se usaron rutas `_FILE` para leer credenciales desde `/run/secrets`.
- Se segmentaron las redes `public-net`, `service-net` y `data-net`.
- Se redactaron notas de seguridad en [security-notes.md](/C:/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex/shopmicro/docs/security-notes.md).

### 9.2. Vulnerabilidades identificadas

Antes de aplicar el modelo de Swarm con secrets, los principales riesgos eran:

- Contraseñas visibles en variables de entorno locales.
- Posible exposición de servicios de datos si se publicaban puertos innecesarios.
- Ausencia de aislamiento si toda la arquitectura compartiera una sola red.

### 9.3. Estado actual de la Fase 3

Esta fase está preparada a nivel de diseño, pero todavía no se ha ejecutado en un clúster Swarm real. También quedan pendientes:

- la demostración de Docker Secrets en funcionamiento real
- la verificación de TLS interno con `docker info`
- el escaneo de imágenes con Docker Scout o Trivy

## 10. Fase 4: Kubernetes - Migración y gestión avanzada

### 10.1. Trabajo realizado

La fase 4 ya ha empezado a ejecutarse sobre un clúster local Minikube con Kubernetes `v1.30.0`. Además de la preparación previa de manifiestos, se ha realizado ya un primer despliegue funcional.

Se había dejado inicialmente una base completa de manifiestos Kubernetes en la carpeta [k8s](/C:/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex/shopmicro/k8s):

- `Namespace`
- `Deployments`
- `Services`
- `ConfigMaps`
- `Secrets`

La estructura está separada entre:

- [k8s/infra](/C:/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex/shopmicro/k8s/infra)
- [k8s/base](/C:/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex/shopmicro/k8s/base)

Además, ya existe una comparativa inicial entre Swarm y Kubernetes en [swarm-vs-kubernetes.md](/C:/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex/shopmicro/docs/swarm-vs-kubernetes.md).

Ejecución real ya realizada:

- instalación de Minikube
- arranque de un clúster local con Docker como driver
- construcción de imágenes propias y carga en Minikube
- `kubectl apply` de infraestructura y servicios
- verificación de `kubectl get pods -n shopmicro`
- verificación de `kubectl get services -n shopmicro`
- comprobación de `kubectl describe deployment product-service -n shopmicro`
- prueba funcional de consulta de productos
- prueba funcional de creación de pedido
- validación del consumo en `notification-service`

La trazabilidad completa del procedimiento se ha documentado en [memoria-kubernetes-procedimiento.md](/C:/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex/shopmicro/docs/memoria-kubernetes-procedimiento.md).

### 10.2. Estado actual de la Fase 4

En este momento la fase 4 se encuentra en estado `parcialmente ejecutada y validada`.

Ya realizado:

- despliegue funcional sobre Minikube
- verificación básica del entorno Kubernetes
- validación de servicios y pods
- demostración del flujo de productos y del flujo de pedido con notificación
- rolling update real de `product-service` desde `1.0.0` a `1.1.0`
- prueba de self-healing eliminando manualmente un pod y verificando su recreación automática

Pendiente:

- documentación final con capturas numeradas
- repetición documentada y completa de todos los flujos desde frontend con evidencia visual
- cierre comparativo final entre Swarm y Kubernetes

## 11. Archivos principales generados

Los archivos más importantes creados durante el proyecto son:

- [docker-compose.yml](/C:/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex/shopmicro/docker-compose.yml)
- [docker-stack.yml](/C:/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex/shopmicro/docker-stack.yml)
- [frontend/index.html](/C:/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex/shopmicro/frontend/index.html)
- [frontend/assets/app.js](/C:/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex/shopmicro/frontend/assets/app.js)
- [api-gateway/nginx.conf](/C:/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex/shopmicro/api-gateway/nginx.conf)
- [product-service/app.py](/C:/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex/shopmicro/product-service/app.py)
- [order-service/app.py](/C:/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex/shopmicro/order-service/app.py)
- [user-service/app.py](/C:/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex/shopmicro/user-service/app.py)
- [notification-service/app.py](/C:/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex/shopmicro/notification-service/app.py)
- [k8s/README.md](/C:/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex/shopmicro/k8s/README.md)

## 12. Conclusiones provisionales

El trabajo realizado hasta el momento demuestra que la base de ShopMicro está correctamente diseñada como arquitectura multicontenedor y que la fase local con Docker Compose ya es utilizable. La solución presenta separación de responsabilidades, persistencia, caché, mensajería y un punto de entrada único mediante gateway.

También se ha avanzado más allá de la fase 1 al dejar preparadas las siguientes fases en forma de configuración reproducible, aunque sin validación real todavía. Esta preparación anticipada acelera el desarrollo posterior y permitirá pasar a Swarm y Kubernetes reutilizando una arquitectura ya coherente.

Desde el punto de vista técnico, Docker Compose ha sido suficiente para validar el comportamiento funcional local. Docker Swarm parece una opción adecuada para preproducción por su sencillez y por su integración nativa con Docker. Kubernetes, en cambio, apunta a ser la opción más sólida para producción cuando se requiera escalado avanzado, mayor observabilidad, mejor separación declarativa de recursos y una orquestación más madura.

## 13. Trabajo pendiente para completar la memoria final

Antes de convertir este documento en PDF final, todavía conviene completar:

- Capturas reales numeradas de la fase 1.
- Ejecución y documentación real de la fase 2.
- Ejecución y documentación real de la fase 3.
- Despliegue real y capturas de la fase 4.
- Inserción íntegra de todos los YAML y Dockerfiles en anexos o secciones de código.
- Generación del índice automático en Word o Writer.

## 14. Anexos recomendados

Para cumplir exactamente el formato del enunciado, se recomienda añadir al documento final los siguientes anexos con bloques de código completos:

1. `docker-compose.yml`
2. `docker-stack.yml`
3. `frontend/Dockerfile`
4. `frontend/nginx.conf`
5. `api-gateway/Dockerfile`
6. `api-gateway/nginx.conf`
7. `product-service/Dockerfile`
8. `product-service/app.py`
9. `order-service/Dockerfile`
10. `order-service/app.py`
11. `user-service/Dockerfile`
12. `user-service/app.py`
13. `notification-service/Dockerfile`
14. `notification-service/app.py`
15. Manifiestos Kubernetes de `k8s/infra`
16. Manifiestos Kubernetes de `k8s/base`
