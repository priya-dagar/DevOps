"""Flask app for ENSP461 Lab 3 - monitoring, logging and DevSecOps."""
import logging
import os

from flask import Flask, jsonify, request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

APP_VERSION = os.getenv("APP_VERSION", "3.0.0")
FEATURE_BETA = os.getenv("FEATURE_BETA", "false").lower() == "true"
LOG_DIR = os.getenv("LOG_DIR", "logs")

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "lab3_app_requests_total", "Total HTTP requests", ["endpoint", "status"]
)

os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(os.path.join(LOG_DIR, "app.log")), logging.StreamHandler()],
)
log = logging.getLogger("lab3")


@app.after_request
def count_request(response):
    REQUEST_COUNT.labels(request.path, str(response.status_code)).inc()
    return response


@app.route("/")
def index():
    log.info("GET / served")
    return jsonify(message="DevOps Lab 3 app is working", version=APP_VERSION)


@app.route("/health")
def health():
    log.info("GET /health served")
    return jsonify(status="UP", version=APP_VERSION), 200


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


@app.route("/beta")
def beta():
    if not FEATURE_BETA:
        log.info("GET /beta rejected - feature flag disabled")
        return jsonify(feature="beta", enabled=False), 404
    log.info("GET /beta served - feature flag enabled")
    return jsonify(feature="beta", enabled=True, message="Welcome to the beta feature")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
