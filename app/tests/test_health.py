from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_200():
    resp = client.get("/health")
    assert resp.status_code == 200


def test_health_body_has_status():
    resp = client.get("/health")
    body = resp.json()
    assert body["status"] == "healthy"
    assert "version" in body


def test_ready_endpoint():
    resp = client.get("/ready")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ready"
