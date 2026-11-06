"""Flask app for ENSP461 Lab 1 - CI/CD pipeline demo."""
from flask import Flask, jsonify

app = Flask(__name__)

APP_VERSION = "1.0.1"


@app.route("/")
def index():
    return jsonify(message="DevOps Lab 1 CI/CD pipeline is working", version=APP_VERSION)


@app.route("/health")
def health():
    return jsonify(status="UP", version=APP_VERSION), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
