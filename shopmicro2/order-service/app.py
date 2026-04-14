import json
import os
import time
from flask import Flask, Response, g, jsonify, request
import pika
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
import pymysql
import requests


app = Flask(__name__)
SERVICE_NAME = "order-service"
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


def env_value(name: str, default: str = "") -> str:
    file_name = f"{name}_FILE"
    if os.getenv(file_name):
        with open(os.getenv(file_name), "r", encoding="utf-8") as file:
            return file.read().strip()
    return os.getenv(name, default)


def flag_enabled(name: str) -> bool:
    return os.getenv(name, "false").strip().lower() in {"1", "true", "yes", "on"}


def mysql_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "db-orders"),
        user=env_value("DB_USER", "orders_user"),
        password=env_value("DB_PASSWORD", "orders_pass123"),
        database=os.getenv("DB_NAME", "orders_db"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


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


def check_mysql() -> None:
    with mysql_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")


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


def publish_order_event(message: dict):
    connection = rabbitmq_connection()
    channel = connection.channel()
    channel.queue_declare(queue="order_events", durable=True)
    channel.basic_publish(
        exchange="",
        routing_key="order_events",
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    connection.close()


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
        check_mysql()
        check_rabbitmq()
    except Exception as exc:
        return {
            "status": "not_ready",
            "service": SERVICE_NAME,
            "version": APP_VERSION,
            "details": str(exc),
        }, 503

    return {"status": "ready", "service": SERVICE_NAME, "version": APP_VERSION}, 200


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.get("/orders")
def list_orders():
    with mysql_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, user_id, product_id, quantity, status, created_at
                FROM orders
                ORDER BY id DESC
                """
            )
            rows = cursor.fetchall()
    return jsonify(rows)


@app.post("/orders")
def create_order():
    payload = request.get_json(force=True)
    product_id = payload["product_id"]
    quantity = int(payload.get("quantity", 1))
    user_id = int(payload.get("user_id", 1))

    stock_response = requests.post(
        f"{os.getenv('PRODUCT_SERVICE_URL', 'http://product-service:5000')}/internal/stock/decrease",
        json={"product_id": product_id, "quantity": quantity},
        timeout=10,
    )
    if stock_response.status_code >= 400:
        return jsonify({"error": "stock_not_available", "details": stock_response.json()}), 409

    with mysql_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO orders (user_id, product_id, quantity, status)
                VALUES (%s, %s, %s, %s)
                """,
                (user_id, product_id, quantity, "CREATED"),
            )
            order_id = cursor.lastrowid

    event = {
        "order_id": order_id,
        "user_id": user_id,
        "product_id": product_id,
        "quantity": quantity,
        "status": "CREATED",
    }
    publish_order_event(event)
    return jsonify({"status": "created", "order": event}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
