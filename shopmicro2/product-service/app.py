import json
import os
import time
from decimal import Decimal
from flask import Flask, Response, g, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
import pymysql
import redis


app = Flask(__name__)
SERVICE_NAME = "product-service"
APP_VERSION = os.getenv("APP_VERSION", "2.0.0")
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
        host=os.getenv("DB_HOST", "db-products"),
        user=env_value("DB_USER", "products_user"),
        password=env_value("DB_PASSWORD", "products_pass123"),
        database=os.getenv("DB_NAME", "products_db"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


cache_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "cache"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
)
CACHE_TTL = int(os.getenv("REDIS_TTL", "60"))


def normalize_product(row: dict) -> dict:
    normalized = dict(row)
    if isinstance(normalized.get("price"), Decimal):
        normalized["price"] = float(normalized["price"])
    return normalized


def check_mysql() -> None:
    with mysql_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")


def check_redis() -> None:
    cache_client.ping()


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


@app.get("/health")
def health():
    if flag_enabled("SIMULATE_HEALTH_FAILURE"):
        return {
            "status": "error",
            "service": SERVICE_NAME,
            "version": APP_VERSION,
        }, 503
    return {
        "status": "ok",
        "service": SERVICE_NAME,
        "version": APP_VERSION,
    }, 200


@app.get("/ready")
def ready():
    if flag_enabled("SIMULATE_READY_FAILURE"):
        return {
            "status": "not_ready",
            "service": SERVICE_NAME,
            "version": APP_VERSION,
        }, 503

    try:
        check_mysql()
        check_redis()
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
    }, 200


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.get("/products")
def list_products():
    cached = cache_client.get("products:all")
    if cached:
        return jsonify(
            {
                "source": "cache",
                "service": "product-service",
                "version": APP_VERSION,
                "items": json.loads(cached),
            }
        )

    with mysql_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, description, price, stock
                FROM products
                ORDER BY id
                """
            )
            items = [normalize_product(item) for item in cursor.fetchall()]

    cache_client.setex("products:all", CACHE_TTL, json.dumps(items))
    return jsonify(
        {
            "source": "database",
            "service": "product-service",
            "version": APP_VERSION,
            "items": items,
        }
    )


@app.post("/products")
def create_product():
    payload = request.get_json(force=True)
    with mysql_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO products (name, description, price, stock)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    payload["name"],
                    payload.get("description", ""),
                    payload["price"],
                    payload.get("stock", 0),
                ),
            )
            product_id = cursor.lastrowid
    cache_client.delete("products:all")
    return jsonify({"id": product_id, "status": "created"}), 201


@app.put("/products/<int:product_id>")
def update_product(product_id: int):
    payload = request.get_json(force=True)
    with mysql_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE products
                SET name = %s, description = %s, price = %s, stock = %s
                WHERE id = %s
                """,
                (
                    payload["name"],
                    payload.get("description", ""),
                    payload["price"],
                    payload.get("stock", 0),
                    product_id,
                ),
            )
    cache_client.delete("products:all")
    return jsonify({"id": product_id, "status": "updated"})


@app.delete("/products/<int:product_id>")
def delete_product(product_id: int):
    with mysql_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    cache_client.delete("products:all")
    return jsonify({"id": product_id, "status": "deleted"})


@app.post("/internal/stock/decrease")
def decrease_stock():
    payload = request.get_json(force=True)
    product_id = payload["product_id"]
    quantity = int(payload.get("quantity", 1))

    with mysql_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT stock FROM products WHERE id = %s",
                (product_id,),
            )
            product = cursor.fetchone()
            if not product:
                return jsonify({"error": "product_not_found"}), 404
            if product["stock"] < quantity:
                return jsonify({"error": "insufficient_stock"}), 409
            cursor.execute(
                "UPDATE products SET stock = stock - %s WHERE id = %s",
                (quantity, product_id),
            )

    cache_client.delete("products:all")
    return jsonify({"status": "stock_updated", "product_id": product_id})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
