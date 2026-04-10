import os
from datetime import datetime, timedelta, timezone
from flask import Flask, jsonify, request
import jwt
import pymysql


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


@app.get("/health")
def health():
    return {"status": "ok", "service": "user-service"}, 200


@app.post("/users/register")
def register():
    payload = request.get_json(force=True)
    with mysql_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (email, password, full_name)
                VALUES (%s, %s, %s)
                """,
                (
                    payload["email"],
                    payload["password"],
                    payload.get("full_name", "ShopMicro User"),
                ),
            )
            user_id = cursor.lastrowid
    return jsonify({"id": user_id, "status": "registered"}), 201


@app.post("/users/login")
def login():
    payload = request.get_json(force=True)
    with mysql_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, email, full_name
                FROM users
                WHERE email = %s AND password = %s
                """,
                (payload["email"], payload["password"]),
            )
            user = cursor.fetchone()
    if not user:
        return jsonify({"error": "invalid_credentials"}), 401

    token = jwt.encode(
        {
            "sub": user["id"],
            "email": user["email"],
            "exp": datetime.now(timezone.utc) + timedelta(hours=4),
        },
        env_value("JWT_SECRET", "change-me-in-real-env"),
        algorithm="HS256",
    )
    return jsonify({"token": token, "user": user})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

