# ShopMicro

ShopMicro is a sample microservices e-commerce platform prepared for the project "Docker Orquestradors: Docker Swarm i Kubernetes".

The repository includes a working base for the four requested phases:

- Docker Compose for local development
- Docker Swarm for high availability and scaling
- Docker Swarm security with secrets and network isolation
- Kubernetes manifests for production-style deployment

## Stack

- `frontend`: Nginx + static HTML/CSS/JS
- `api-gateway`: Nginx reverse proxy
- `product-service`: Flask + Redis + MySQL
- `order-service`: Flask + MySQL + RabbitMQ
- `user-service`: Flask + JWT + MySQL
- `notification-service`: Flask consumer for RabbitMQ
- `db-products`: MySQL 8
- `db-orders`: MySQL 8
- `cache`: Redis 7
- `message-queue`: RabbitMQ 3

## Repository structure

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

## Main flows

1. Product listing: `frontend -> api-gateway -> product-service -> Redis/MySQL`
2. Order creation: `frontend -> api-gateway -> order-service -> product-service -> db-orders -> RabbitMQ -> notification-service`
3. Swarm failover base: services are defined with replicas and placement rules

## Local run with Docker

From the project root:

```bash
cp .env.example .env
docker compose up -d --build
```

Open:

- Frontend: `http://localhost:8080`
- API Gateway health: `http://localhost:8081/health`
- RabbitMQ UI: `http://localhost:15672`

RabbitMQ default credentials:

- User: `shopmicro`
- Password: `shopmicro-pass`

## Useful files

- [docker-compose.yml](./docker-compose.yml): local environment
- [docker-stack.yml](./docker-stack.yml): Swarm deployment
- [docs/report-outline.md](./docs/report-outline.md): report guide for the PDF delivery
- [docs/architecture.mmd](./docs/architecture.mmd): Mermaid architecture diagram
- [k8s/](./k8s/): Kubernetes manifests

## Important notes before publishing

- Real secrets should never be committed
- The `secrets/` folder is ignored on purpose
- The `.env` file is ignored on purpose
- If you need example secrets, keep them only as documentation, not as active credentials

## Suggested first commit

```bash
git init
git branch -M main
git add .
git commit -m "Initial ShopMicro project"
```

