import json
import os
from decimal import Decimal
from flask import Flask, jsonify, request
import pymysql
import redis


app = Flask(__name__)
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")


def env_value(name: str, default: str = "") -> str:
    file_name = f"{name}_FILE"
    if os.getenv(file_name):
        with open(os.getenv(file_name), "r", encoding="utf-8") as file:
            return file.read().strip()
    return os.getenv(name, default)


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


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "product-service",
        "version": APP_VERSION,
    }, 200


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
