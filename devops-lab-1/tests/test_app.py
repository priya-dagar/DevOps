"""Unit tests for the Flask app routes."""
import pytest
from app.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_returns_message(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json["message"] == "DevOps Lab 1 CI/CD pipeline is working"


def test_health_returns_up(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json["status"] == "UP"
