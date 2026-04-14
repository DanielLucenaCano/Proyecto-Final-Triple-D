# Fase 1. Docker Swarm Avanzado en Maquinas Virtuales

## Objetivo

Este documento describe, de principio a fin, como ejecutar la Fase 1 de la practica avanzada de Docker Swarm en tres maquinas virtuales:

- `swarm-manager`
- `swarm-worker1`
- `swarm-worker2`

El documento asume que la configuracion del proyecto ya esta preparada en el repositorio y que el archivo de despliegue a utilizar es `docker-stack.yml`.

## Alcance de esta fase

La fase cubre estos bloques:

- creacion del cluster Swarm
- despliegue de ShopMicro en modo stack
- escalado dinamico por servicio
- despliegue global de `cAdvisor`
- rolling update y rollback de `product-service`
- monitorizacion con `Prometheus + cAdvisor`
- validacion de routing mesh y balanceo interno
- comprobacion de alta disponibilidad y limitacion de un solo manager

## Topologia recomendada

### Maquinas virtuales

- `swarm-manager`: nodo manager del cluster
- `swarm-worker1`: nodo worker
- `swarm-worker2`: nodo worker

### Requisitos minimos por VM

- sistema Linux reciente
- Docker Engine instalado y operativo
- conectividad IP entre las tres VMs
- puertos de Swarm abiertos entre nodos:
  - `2377/tcp`
  - `7946/tcp`
  - `7946/udp`
  - `4789/udp`

## 1. Preparacion inicial en las tres VMs

### 1.1. Definir nombres de host

En cada VM:

```bash
hostnamectl set-hostname swarm-manager
hostnamectl set-hostname swarm-worker1
hostnamectl set-hostname swarm-worker2
```

Ejecuta el comando correspondiente en cada maquina.

### 1.2. Registrar resolucion de nombres

En las tres VMs, edita `/etc/hosts` y añade las IPs reales:

```text
192.168.56.10 swarm-manager
192.168.56.11 swarm-worker1
192.168.56.12 swarm-worker2
```

Validar conectividad:

```bash
ping -c 3 swarm-manager
ping -c 3 swarm-worker1
ping -c 3 swarm-worker2
```

### 1.3. Verificar Docker

En las tres VMs:

```bash
docker version
docker info
```

## 2. Copiar el proyecto al manager

La carpeta del proyecto debe existir en `swarm-manager`. Ejemplo:

```bash
mkdir -p ~/shopmicro2
cd ~/shopmicro2
```

Copia el contenido del repositorio al manager por el metodo que prefieras:

- `git clone`
- `scp`
- carpeta compartida

Valida que existen estos elementos:

```bash
cd ~/shopmicro2
ls -la
ls -la monitoring
ls -la secrets
```

## 3. Inicializar Docker Swarm

### 3.1. Crear el cluster en `swarm-manager`

En `swarm-manager`:

```bash
docker swarm init --advertise-addr <IP_MANAGER>
```

Ejemplo:

```bash
docker swarm init --advertise-addr 192.168.56.10
```

El comando devolvera un `docker swarm join ...` para workers.

### 3.2. Unir `swarm-worker1` y `swarm-worker2`

En cada worker, ejecuta el comando entregado por el manager. Ejemplo:

```bash
docker swarm join --token <TOKEN_WORKER> 192.168.56.10:2377
```

### 3.3. Validar el cluster

En `swarm-manager`:

```bash
docker node ls
```

Resultado esperado:

- `swarm-manager` como `Leader`
- `swarm-worker1` como `Ready`
- `swarm-worker2` como `Ready`

## 4. Preparar secretos y precondiciones del stack

El `docker-stack.yml` del proyecto usa secretos desde ficheros locales.

### 4.1. Verificar secretos en el manager

En `swarm-manager`:

```bash
cd ~/shopmicro2
ls -la secrets
cat secrets/db_root_password.txt
cat secrets/products_db_password.txt
cat secrets/orders_db_password.txt
cat secrets/rabbitmq_password.txt
cat secrets/jwt_secret.txt
```

### 4.2. Verificar configuracion de Prometheus

```bash
cat monitoring/prometheus-swarm.yml
```

### 4.3. Verificar imagenes

Si las imagenes `shopmicro/...` ya estan en un registro accesible, no hace falta reconstruir.

Si las vais a construir en el manager:

```bash
docker build -t shopmicro/frontend:1.0.0 frontend
docker build -t shopmicro/api-gateway:1.0.0 api-gateway
docker build -t shopmicro/product-service:2.0.0 product-service
docker build -t shopmicro/order-service:1.1.0 order-service
docker build -t shopmicro/user-service:1.1.0 user-service
docker build -t shopmicro/notification-service:1.1.0 notification-service
```

Si el cluster usa varias VMs reales, la opcion profesional es subir esas imagenes a Docker Hub o a un registro privado y asegurarse de que los tres nodos pueden hacer `pull`.

## 5. Desplegar el stack ShopMicro

En `swarm-manager`:

```bash
cd ~/shopmicro2
docker stack deploy -c docker-stack.yml shopmicro
```

### 5.1. Validar servicios

```bash
docker stack services shopmicro
docker stack ps shopmicro
```

### 5.2. Ver detalle por servicio

```bash
docker service ls
docker service ps shopmicro_frontend
docker service ps shopmicro_api-gateway
docker service ps shopmicro_product-service
docker service ps shopmicro_order-service
docker service ps shopmicro_user-service
docker service ps shopmicro_notification-service
docker service ps shopmicro_cadvisor
docker service ps shopmicro_prometheus
```

## 6. Validacion funcional inicial

Accede al frontend desde cualquier nodo:

```bash
curl http://<IP_MANAGER>:8080
curl http://<IP_WORKER1>:8080
curl http://<IP_WORKER2>:8080
```

Valida el gateway:

```bash
curl http://<IP_MANAGER>:8081/health
curl http://<IP_MANAGER>:8081/api/products
```

Valida Prometheus:

```bash
curl http://<IP_MANAGER>:9090/-/ready
```

Accesos web esperados:

- frontend: `http://<IP_NODO>:8080`
- api-gateway: `http://<IP_NODO>:8081`
- Prometheus: `http://<IP_MANAGER>:9090`
- RabbitMQ UI: `http://<IP_MANAGER>:15672`

## 7. Escalado dinamico por servicio

Segun el enunciado, hay que demostrar escalado en caliente sobre `product-service` y `order-service`.

### 7.1. Escalar servicios

En `swarm-manager`:

```bash
docker service scale shopmicro_product-service=4 shopmicro_order-service=3
```

### 7.2. Validar distribucion de replicas

```bash
docker service ps shopmicro_product-service
docker service ps shopmicro_order-service
docker stack ps shopmicro
```

Punto de control:

- `product-service` debe quedar con `4` replicas
- `order-service` debe quedar con `3` replicas
- las replicas deben repartirse entre nodos

## 8. Escalado global de cAdvisor

El `docker-stack.yml` ya define `cAdvisor` en modo `global`.

### 8.1. Verificar despliegue global

```bash
docker service inspect shopmicro_cadvisor --format '{{json .Spec.Mode}}'
docker service ps shopmicro_cadvisor
```

Resultado esperado:

- una tarea de `cAdvisor` por nodo
- total esperado: `3` tareas, una en `swarm-manager`, una en `swarm-worker1` y una en `swarm-worker2`

## 9. Rolling update de `product-service`

El stack ya define politica de update y rollback para `product-service`.

### 9.1. Comprobar la configuracion aplicada

```bash
docker service inspect shopmicro_product-service --pretty
```

Debes confirmar:

- `parallelism: 1`
- `delay: 10s`
- `failure_action: rollback`
- `monitor: 30s`
- `rollback_config` activo

### 9.2. Lanzar actualizacion controlada

Si ya has subido una nueva imagen con la misma etiqueta esperada, puedes forzar redeploy:

```bash
docker service update --force shopmicro_product-service
```

Si quieres cambiar la imagen explicitamente:

```bash
docker service update --image shopmicro/product-service:2.0.0 shopmicro_product-service
```

### 9.3. Observar la sustitucion de replicas

```bash
watch -n 2 docker service ps shopmicro_product-service
```

Sin `watch`:

```bash
docker service ps shopmicro_product-service
```

Debes documentar que:

- se actualiza una replica cada vez
- el servicio sigue disponible
- las tareas antiguas se sustituyen progresivamente

## 10. Prueba de rollback automatico

El objetivo es demostrar que Swarm revierte automaticamente si la nueva version falla.

### 10.1. Simular version defectuosa

Usa una imagen inexistente:

```bash
docker service update --image shopmicro/product-service:broken shopmicro_product-service
```

### 10.2. Observar fallo y rollback

```bash
docker service ps shopmicro_product-service
docker service inspect shopmicro_product-service --pretty
```

Debes comprobar:

- la nueva tarea no llega a `Running`
- Swarm detecta el fallo
- se ejecuta rollback automatico por `failure_action: rollback`

### 10.3. Restaurar si fuese necesario

Si quieres forzar manualmente la vuelta atras:

```bash
docker service rollback shopmicro_product-service
```

## 11. Monitorizacion con Prometheus y cAdvisor

### 11.1. Validar estado de Prometheus

```bash
docker service ps shopmicro_prometheus
curl http://<IP_MANAGER>:9090/-/ready
```

### 11.2. Acceder a Prometheus

Abre en navegador:

```text
http://<IP_MANAGER>:9090
```

### 11.3. Consultas recomendadas

En la interfaz de Prometheus, ejecuta:

```text
container_cpu_usage_seconds_total
```

```text
container_memory_usage_bytes
```

Filtra si quieres por servicio o contenedor.

### 11.4. Verificar targets

En Prometheus, abre:

```text
Status > Targets
```

Debes ver:

- `cadvisor`
- `product-service`
- `order-service`
- `user-service`

## 12. Demostracion de routing mesh

Docker Swarm permite entrar por cualquier nodo aunque la replica concreta no viva en ese nodo.

### 12.1. Probar acceso por cualquier IP

Ejecuta desde tu maquina anfitriona o desde otra VM:

```bash
curl http://<IP_MANAGER>:8080
curl http://<IP_WORKER1>:8080
curl http://<IP_WORKER2>:8080
```

Haz lo mismo con el gateway:

```bash
curl http://<IP_MANAGER>:8081/health
curl http://<IP_WORKER1>:8081/health
curl http://<IP_WORKER2>:8081/health
```

Conclusion esperada:

- cualquier nodo recibe la peticion
- el routing mesh la redirige a una replica valida del servicio

## 13. Demostracion del balanceo interno VIP

El objetivo es demostrar que, desde dentro del cluster, las peticiones se balancean entre replicas.

### 13.1. Entrar en una tarea de `product-service`

Primero identifica un contenedor:

```bash
docker ps --format 'table {{.ID}}\t{{.Image}}\t{{.Names}}'
```

Luego entra en uno de los contenedores de `product-service`:

```bash
docker exec -it <CONTAINER_ID_PRODUCT_SERVICE> sh
```

### 13.2. Lanzar varias peticiones al gateway

Dentro del contenedor:

```sh
for i in 1 2 3 4 5; do wget -qO- http://api-gateway/api/products; echo; done
```

Alternativa si existe `curl`:

```sh
for i in 1 2 3 4 5; do curl -s http://api-gateway/api/products; echo; done
```

### 13.3. Revisar logs del gateway

En el manager:

```bash
docker service logs shopmicro_api-gateway --tail 100
```

El objetivo es documentar que:

- las peticiones entran siempre por el VIP del servicio
- el backend atiende desde replicas distintas

## 14. Alta disponibilidad y caida de nodos

### 14.1. Simular caida de un worker

Apaga `swarm-worker1` o para Docker en ese nodo:

```bash
sudo systemctl stop docker
```

### 14.2. Revisar reaccion del cluster

En `swarm-manager`:

```bash
docker node ls
docker stack ps shopmicro
docker service ps shopmicro_product-service
```

Debes comprobar:

- el nodo pasa a `Down` o `Unavailable`
- Swarm reprograma replicas en nodos sanos cuando aplica

### 14.3. Restaurar el worker

En `swarm-worker1`:

```bash
sudo systemctl start docker
```

Valida de nuevo:

```bash
docker node ls
```

## 15. Prueba especifica de caida del manager

### 15.1. Comprobar limitacion real

Con un solo manager, si cae `swarm-manager`, el plano de control deja de tener quorum.

Esto significa:

- los contenedores que ya esten corriendo pueden seguir un tiempo
- pero no podras gestionar el cluster correctamente
- no hay alta disponibilidad real del control plane

### 15.2. Demostracion conceptual

En `swarm-manager`, antes de apagarlo:

```bash
docker node ls
docker service ls
```

Luego apaga el manager o para Docker:

```bash
sudo systemctl stop docker
```

Conclusion que debes documentar:

- con `1 manager + 2 workers` no hay HA real del plano de control
- para HA real se necesitan `3 managers` con consenso Raft

## 16. Explicacion de HA real con 3 managers

La configuracion correcta para alta disponibilidad del plano de control seria:

- `3 managers`
- `2 workers` o mas

Ejemplo teorico para añadir managers adicionales:

En el manager actual:

```bash
docker swarm join-token manager
```

En los nuevos managers:

```bash
docker swarm join --token <TOKEN_MANAGER> 192.168.56.10:2377
```

Validacion:

```bash
docker node ls
```

Con `3 managers`, el cluster tolera la caida de `1 manager` sin perder quorum.

## 17. Comandos de cierre y limpieza

### 17.1. Eliminar el stack

En `swarm-manager`:

```bash
docker stack rm shopmicro
```

### 17.2. Esperar limpieza

```bash
docker service ls
docker network ls
```

### 17.3. Salir del modo Swarm en workers

En cada worker:

```bash
docker swarm leave
```

### 17.4. Salir del modo Swarm en manager

En `swarm-manager`:

```bash
docker swarm leave --force
```

## 18. Checklist de evidencias recomendadas

Para documentar la fase en la memoria, conviene capturar:

- `docker node ls`
- `docker stack services shopmicro`
- `docker stack ps shopmicro`
- `docker service ps shopmicro_product-service`
- `docker service ps shopmicro_order-service`
- `docker service ps shopmicro_cadvisor`
- interfaz de Prometheus con targets en `UP`
- consulta de `container_cpu_usage_seconds_total`
- consulta de `container_memory_usage_bytes`
- acceso al frontend desde las tres IPs de nodo
- prueba de rollback de `product-service`
- prueba de caida de un worker
- explicacion de por que `1 manager` no da HA real

## 19. Resumen ejecutivo de comandos clave

### Crear cluster

```bash
docker swarm init --advertise-addr <IP_MANAGER>
docker swarm join --token <TOKEN_WORKER> <IP_MANAGER>:2377
docker node ls
```

### Desplegar stack

```bash
cd ~/shopmicro2
docker stack deploy -c docker-stack.yml shopmicro
docker stack services shopmicro
docker stack ps shopmicro
```

### Escalar

```bash
docker service scale shopmicro_product-service=4 shopmicro_order-service=3
docker service ps shopmicro_product-service
docker service ps shopmicro_order-service
```

### Rolling update y rollback

```bash
docker service update --force shopmicro_product-service
docker service update --image shopmicro/product-service:broken shopmicro_product-service
docker service rollback shopmicro_product-service
```

### Monitorizacion

```bash
docker service ps shopmicro_cadvisor
docker service ps shopmicro_prometheus
curl http://<IP_MANAGER>:9090/-/ready
```

### Limpieza

```bash
docker stack rm shopmicro
docker swarm leave
docker swarm leave --force
```
