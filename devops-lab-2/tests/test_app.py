from app.app import app


def test_index():
    app.config["TESTING"] = True
    with app.test_client() as c:
        res = c.get("/")
        assert res.status_code == 200
        assert res.json["version"] == "2.0.0"


def test_health():
    app.config["TESTING"] = True
    with app.test_client() as c:
        res = c.get("/health")
        assert res.status_code == 200
        assert res.json["status"] == "UP"
