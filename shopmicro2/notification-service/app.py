import json
import logging
import os
import threading
import time
from flask import Flask, Response, g, request
import pika
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest


app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
SERVICE_NAME = "notification-service"
APP_VERSION = os.getenv("APP_VERSION", "1.1.0")
REQUEST_COUNT = Counter(
    "shopmicro_http_requests_total",
    "Total HTTP requests handled by ShopMicro services.",
    ["service", "method", "endpoint", "status"],
)
REQUEST_LATENCY = Histogram(
    "shopmicro_http_request_duration_seconds",
    "Request latency in seconds.",
    ["service", "endpoint"],
)
NOTIFICATIONS_PROCESSED = Counter(
    "shopmicro_notifications_processed_total",
    "Processed order notification events.",
)
consumer_state = {
    "connected": False,
    "last_error": "",
}


def env_value(name: str, default: str = "") -> str:
    file_name = f"{name}_FILE"
    if os.getenv(file_name):
        with open(os.getenv(file_name), "r", encoding="utf-8") as file:
            return file.read().strip()
    return os.getenv(name, default)


def flag_enabled(name: str) -> bool:
    return os.getenv(name, "false").strip().lower() in {"1", "true", "yes", "on"}


def rabbitmq_connection():
    credentials = pika.PlainCredentials(
        env_value("RABBITMQ_USER", "shopmicro"),
        env_value("RABBITMQ_PASSWORD", "shopmicro-pass"),
    )
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.getenv("RABBITMQ_HOST", "message-queue"),
            credentials=credentials,
        )
    )


def check_rabbitmq() -> None:
    connection = rabbitmq_connection()
    connection.close()


@app.before_request
def before_request() -> None:
    g.request_started_at = time.perf_counter()


@app.after_request
def after_request(response):
    endpoint = request.endpoint or request.path
    REQUEST_COUNT.labels(
        SERVICE_NAME,
        request.method,
        endpoint,
        str(response.status_code),
    ).inc()
    if hasattr(g, "request_started_at"):
        REQUEST_LATENCY.labels(SERVICE_NAME, endpoint).observe(
            time.perf_counter() - g.request_started_at
        )
    return response


def consume_messages():
    while True:
        try:
            connection = rabbitmq_connection()
            channel = connection.channel()
            channel.queue_declare(queue="order_events", durable=True)
            consumer_state["connected"] = True
            consumer_state["last_error"] = ""

            def callback(ch, method, properties, body):
                event = json.loads(body.decode("utf-8"))
                logging.info("Notification sent for order %s", event["order_id"])
                NOTIFICATIONS_PROCESSED.inc()
                ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue="order_events", on_message_callback=callback)
            logging.info("Waiting for order events...")
            channel.start_consuming()
        except Exception as exc:
            consumer_state["connected"] = False
            consumer_state["last_error"] = str(exc)
            logging.warning("RabbitMQ not ready yet: %s", exc)
            time.sleep(5)


@app.get("/health")
def health():
    if flag_enabled("SIMULATE_HEALTH_FAILURE"):
        return {"status": "error", "service": SERVICE_NAME, "version": APP_VERSION}, 503
    return {"status": "ok", "service": SERVICE_NAME, "version": APP_VERSION}, 200


@app.get("/ready")
def ready():
    if flag_enabled("SIMULATE_READY_FAILURE"):
        return {"status": "not_ready", "service": SERVICE_NAME, "version": APP_VERSION}, 503

    try:
        check_rabbitmq()
    except Exception as exc:
        return {
            "status": "not_ready",
            "service": SERVICE_NAME,
            "version": APP_VERSION,
            "details": str(exc),
        }, 503

    return {
        "status": "ready",
        "service": SERVICE_NAME,
        "version": APP_VERSION,
        "consumer_connected": consumer_state["connected"],
        "last_error": consumer_state["last_error"],
    }, 200


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    worker = threading.Thread(target=consume_messages, daemon=True)
    worker.start()
    app.run(host="0.0.0.0", port=5000)
