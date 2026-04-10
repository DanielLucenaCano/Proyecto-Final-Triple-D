import json
import logging
import os
import threading
import time
from flask import Flask
import pika


app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def env_value(name: str, default: str = "") -> str:
    file_name = f"{name}_FILE"
    if os.getenv(file_name):
        with open(os.getenv(file_name), "r", encoding="utf-8") as file:
            return file.read().strip()
    return os.getenv(name, default)


def consume_messages():
    while True:
        try:
            credentials = pika.PlainCredentials(
                env_value("RABBITMQ_USER", "shopmicro"),
                env_value("RABBITMQ_PASSWORD", "shopmicro-pass"),
            )
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=os.getenv("RABBITMQ_HOST", "message-queue"),
                    credentials=credentials,
                )
            )
            channel = connection.channel()
            channel.queue_declare(queue="order_events", durable=True)

            def callback(ch, method, properties, body):
                event = json.loads(body.decode("utf-8"))
                logging.info("Notification sent for order %s", event["order_id"])
                ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue="order_events", on_message_callback=callback)
            logging.info("Waiting for order events...")
            channel.start_consuming()
        except Exception as exc:
            logging.warning("RabbitMQ not ready yet: %s", exc)
            time.sleep(5)


@app.get("/health")
def health():
    return {"status": "ok", "service": "notification-service"}, 200


if __name__ == "__main__":
    worker = threading.Thread(target=consume_messages, daemon=True)
    worker.start()
    app.run(host="0.0.0.0", port=5000)

