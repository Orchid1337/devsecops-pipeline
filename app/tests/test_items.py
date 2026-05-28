import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers.items import _reset_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_slate():
    _reset_db()
    yield
    _reset_db()


def test_create_item():
    resp = client.post("/api/v1/items/", json={
        "name": "Mechanical Keyboard",
        "description": "Cherry MX Brown switches",
        "price": 149.99,
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Mechanical Keyboard"
    assert data["price"] == 149.99
    assert data["id"] == 1


def test_xss_gets_stripped():
    resp = client.post("/api/v1/items/", json={
        "name": "<script>alert('xss')</script>Keyboard",
        "price": 50.0,
    })
    assert resp.status_code == 201
    # angle brackets and quotes should be gone
    assert "<script>" not in resp.json()["name"]
    assert "alert" in resp.json()["name"]


def test_negative_price_rejected():
    resp = client.post("/api/v1/items/", json={"name": "Free stuff", "price": -1.0})
    assert resp.status_code == 422


def test_missing_item_404():
    resp = client.get("/api/v1/items/999")
    assert resp.status_code == 404


def test_update_item():
    client.post("/api/v1/items/", json={"name": "Old Name", "price": 10.0})
    resp = client.put("/api/v1/items/1", json={"name": "New Name", "price": 25.0})
    assert resp.status_code == 200
    assert resp.json()["name"] == "New Name"
    assert resp.json()["price"] == 25.0


def test_delete_then_gone():
    client.post("/api/v1/items/", json={"name": "Temp", "price": 1.0})
    resp = client.delete("/api/v1/items/1")
    assert resp.status_code == 204
    # confirm it's actually gone
    assert client.get("/api/v1/items/1").status_code == 404


def test_list_multiple():
    client.post("/api/v1/items/", json={"name": "A", "price": 1.0})
    client.post("/api/v1/items/", json={"name": "B", "price": 2.0})
    resp = client.get("/api/v1/items/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2
