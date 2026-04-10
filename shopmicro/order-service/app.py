import json
import os
from flask import Flask, jsonify, request
import pika
import pymysql
import requests


app = Flask(__name__)


def env_value(name: str, default: str = "") -> str:
    file_name = f"{name}_FILE"
    if os.getenv(file_name):
        with open(os.getenv(file_name), "r", encoding="utf-8") as file:
            return file.read().strip()
    return os.getenv(name, default)


def mysql_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "db-orders"),
        user=env_value("DB_USER", "orders_user"),
        password=env_value("DB_PASSWORD", "orders_pass123"),
        database=os.getenv("DB_NAME", "orders_db"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


def publish_order_event(message: dict):
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
    channel.basic_publish(
        exchange="",
        routing_key="order_events",
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    connection.close()


@app.get("/health")
def health():
    return {"status": "ok", "service": "order-service"}, 200


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

