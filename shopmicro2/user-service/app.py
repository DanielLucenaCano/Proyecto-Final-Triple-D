import os
import time
from datetime import datetime, timedelta, timezone
from flask import Flask, Response, g, jsonify, request
import jwt
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
import pymysql


app = Flask(__name__)
SERVICE_NAME = "user-service"
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


def check_mysql() -> None:
    with mysql_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")


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
        return {"status": "error", "service": SERVICE_NAME, "version": APP_VERSION}, 503
    return {"status": "ok", "service": SERVICE_NAME, "version": APP_VERSION}, 200


@app.get("/ready")
def ready():
    if flag_enabled("SIMULATE_READY_FAILURE"):
        return {"status": "not_ready", "service": SERVICE_NAME, "version": APP_VERSION}, 503

    try:
        check_mysql()
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
