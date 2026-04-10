# Comandos guía para Docker Swarm

## Inicialización

```bash
docker swarm init --advertise-addr <IP_MANAGER>
docker swarm join-token worker
docker swarm join --token <TOKEN> <IP_MANAGER>:2377
docker node ls
```

## Despliegue del stack

```bash
docker build -t shopmicro/frontend:1.0.0 ./frontend
docker build -t shopmicro/api-gateway:1.0.0 ./api-gateway
docker build -t shopmicro/product-service:1.0.0 ./product-service
docker build -t shopmicro/order-service:1.0.0 ./order-service
docker build -t shopmicro/user-service:1.0.0 ./user-service
docker build -t shopmicro/notification-service:1.0.0 ./notification-service

docker stack deploy -c docker-stack.yml shopmicro
docker stack services shopmicro
docker stack ps shopmicro
```

## Tolerancia a fallos

```bash
systemctl stop docker
docker node ls
docker stack ps shopmicro
systemctl start docker
docker node ls
```

## Escalado en caliente

```bash
docker service scale shopmicro_product-service=4
docker service ps shopmicro_product-service
```

