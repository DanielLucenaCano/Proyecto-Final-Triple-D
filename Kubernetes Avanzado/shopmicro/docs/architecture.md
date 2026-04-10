# Arquitectura ShopMicro

## Resumen

La solución separa la plataforma en tres dominios de red:

- `public-net`: solo para `frontend` y `api-gateway`.
- `service-net`: comunicación entre gateway y microservicios.
- `data-net`: acceso restringido a bases de datos, Redis y RabbitMQ.

## Puertos expuestos

- `8080`: frontend web.
- `8081`: api-gateway.
- `6379`: Redis para pruebas locales.
- `15672`: panel de RabbitMQ.

## Servicios

- `frontend`: interfaz estática para listar productos y crear pedidos.
- `api-gateway`: reverse proxy único para enrutar llamadas `/api/*`.
- `product-service`: CRUD básico de productos con cache TTL en Redis.
- `order-service`: crea pedidos, descuenta stock y publica eventos.
- `user-service`: registro y login con JWT.
- `notification-service`: consumidor de RabbitMQ con registro en log.
- `db-products`: MySQL para catálogo.
- `db-orders`: MySQL para pedidos y usuarios.
- `cache`: Redis.
- `message-queue`: RabbitMQ.

