from app.app import app


def test_health():
    app.config["TESTING"] = True
    with app.test_client() as c:
        res = c.get("/health")
        assert res.status_code == 200
        assert res.json["status"] == "UP"


def test_beta_disabled_by_default():
    app.config["TESTING"] = True
    with app.test_client() as c:
        res = c.get("/beta")
        assert res.status_code == 404


def test_metrics_exposed():
    app.config["TESTING"] = True
    with app.test_client() as c:
        res = c.get("/metrics")
        assert res.status_code == 200
        assert b"lab3_app_requests_total" in res.data
