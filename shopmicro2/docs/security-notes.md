# Notas de seguridad

## Vulnerabilidades iniciales detectadas

- Contraseñas de MySQL, RabbitMQ y JWT expuestas en variables de entorno si se usa solo `.env`.
- Riesgo de publicar servicios de datos si se conectan a una red pública.
- Ausencia de separación estricta entre capas si todos los servicios comparten una sola red.

## Medidas aplicadas en esta plantilla

- `docker-stack.yml` migra credenciales a Docker Secrets.
- Las bases de datos y RabbitMQ quedan en `data-net`.
- `frontend` solo habla con `api-gateway`.
- Los microservicios usan credenciales distintas para productos y pedidos.

