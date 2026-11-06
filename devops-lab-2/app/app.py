"""Flask app for ENSP461 Lab 2 - containerization and Kubernetes."""
import os
from flask import Flask, jsonify

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "2.0.0")
APP_MESSAGE = os.getenv("APP_MESSAGE", "DevOps Lab 2 containerized app is working")


@app.route("/")
def index():
    return jsonify(message=APP_MESSAGE, version=APP_VERSION)


@app.route("/health")
def health():
    return jsonify(status="UP", version=APP_VERSION), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
