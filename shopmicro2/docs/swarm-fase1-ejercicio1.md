# Fase 1 - Ejercicio 1 - Escalado dinámico por servicio en Docker Swarm

## Objetivo

Demostrar el escalado en caliente de los servicios `product-service` y `order-service` dentro del stack `shopmicro`, sin detener el despliegue ni recrear el stack completo.

## Alcance del ejercicio

El enunciado exige:

- escalar `product-service` a 4 réplicas;
- escalar `order-service` a 3 réplicas;
- documentar la distribución resultante con `docker service ps`;
- verificar con `docker stack ps shopmicro` que las tareas se reparten entre los nodos del clúster.

## Baseline del proyecto

Estado actual declarado en [docker-stack.yml](/C:/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex%20Projects/Kubernetes%20Avanzado/shopmicro/docker-stack.yml):

- `product-service`: 2 réplicas
- `order-service`: 2 réplicas

Conclusión:

- el stack ya parte de una configuración replicada;
- para este ejercicio no es imprescindible modificar el YAML base;
- el cambio se demuestra operativamente con `docker service scale`.

## Procedimiento operativo

Ejecutar en el nodo manager:

```bash
docker node ls
docker stack services shopmicro
docker service scale shopmicro_product-service=4 shopmicro_order-service=3
docker service ps shopmicro_product-service
docker service ps shopmicro_order-service
docker stack ps shopmicro
docker stack services shopmicro
```

## Evidencias a guardar

Capturas o salidas de:

- `docker node ls`
- `docker stack services shopmicro` antes del escalado
- `docker service scale shopmicro_product-service=4 shopmicro_order-service=3`
- `docker service ps shopmicro_product-service`
- `docker service ps shopmicro_order-service`
- `docker stack ps shopmicro`

## Criterio de validación

El ejercicio se considerará correctamente ejecutado si se verifica lo siguiente:

- `product-service` queda con 4 tareas deseadas y en ejecución;
- `order-service` queda con 3 tareas deseadas y en ejecución;
- el stack sigue disponible tras el escalado;
- las tareas aparecen distribuidas entre los nodos del clúster y no concentradas de forma anómala en un único nodo, salvo restricción explícita del scheduler.

## Lectura técnica esperada

Este ejercicio demuestra que Docker Swarm permite ajustar capacidad de servicio en tiempo real sin necesidad de redeploy completo del stack. A nivel de negocio, esto encaja con escenarios de pico de carga sobre catálogo y pedidos.

## Resultado a documentar en la memoria principal

Al cerrar el ejercicio, conviene registrar:

- fecha de ejecución;
- nodo manager utilizado;
- estado inicial de réplicas;
- estado final de réplicas;
- reparto por nodos;
- incidencia observada, si la hubiera.

## Ejecución real realizada

Fecha de validación: `2026-04-10`

Resultado observado:

- `shopmicro_product-service` quedó en `4/4` réplicas.
- `shopmicro_order-service` quedó en `3/3` réplicas.
- La distribución quedó repartida entre `swarm-worker-1`, `swarm-manager` y `swarm-worker-2`.

Distribución observada en `product-service`:

- réplica `1` en `swarm-worker-1`
- réplica `2` en `swarm-manager`
- réplicas `3` y `4` en `swarm-worker-2`

Distribución observada en `order-service`:

- réplica `1` en `swarm-worker-1`
- réplica `2` en `swarm-manager`
- réplica `3` en `swarm-worker-2`

Conclusión técnica:

- el escalado en caliente se ha ejecutado correctamente;
- Swarm ha mantenido el servicio operativo;
- el scheduler ha distribuido las tareas entre los nodos disponibles del clúster.

## Incidencias detectadas durante la validación

Se ha observado una incidencia ajena al objetivo directo del ejercicio:

- `shopmicro_message-queue` figura en `0/1` en `docker stack services shopmicro`.

Impacto:

- no invalida la demostración del escalado dinámico de `product-service` y `order-service`;
- sí constituye una desviación operativa que conviene resolver antes de abordar ejercicios que dependan de mensajería o monitorización más avanzada.
