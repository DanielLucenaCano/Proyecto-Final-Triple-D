# Introducción a Docker Compose

Docker Compose permite definir y ejecutar aplicaciones multicontenedor con un único fichero YAML. En ShopMicro se usa para levantar rápidamente toda la plataforma en un entorno local con redes, volúmenes, variables de entorno, dependencias y comprobaciones de salud.

## Ideas clave

- Centraliza la definición de servicios en `docker-compose.yml`.
- Facilita dependencias declarativas con `depends_on`.
- Permite crear redes aisladas para separar frontend, microservicios y datos.
- Gestiona volúmenes persistentes para MySQL y RabbitMQ.

## Diferencias frente a `docker run`

- `docker run` crea un contenedor cada vez con una línea de comandos larga y difícil de mantener.
- Compose describe todo el stack como código y se puede versionar.
- Compose simplifica el arranque y parada conjunta de todos los servicios.

