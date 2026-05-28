import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers.users import _reset_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_slate():
    _reset_db()
    yield
    _reset_db()


def test_create_user():
    resp = client.post(
        "/api/v1/users/",
        json={
            "username": "testuser01",
            "email": "user01@example.com",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == "testuser01"
    assert data["email"] == "user01@example.com"
    assert data["id"] == 1


def test_bad_email_gets_422():
    resp = client.post(
        "/api/v1/users/",
        json={
            "username": "someone",
            "email": "this-is-not-email",
        },
    )
    assert resp.status_code == 422


def test_duplicate_username_blocked():
    client.post("/api/v1/users/", json={"username": "taken", "email": "a@b.com"})
    resp = client.post("/api/v1/users/", json={"username": "taken", "email": "c@d.com"})
    assert resp.status_code == 409


def test_empty_list():
    resp = client.get("/api/v1/users/")
    assert resp.status_code == 200
    assert resp.json() == []


def test_nonexistent_user_404():
    resp = client.get("/api/v1/users/42")
    assert resp.status_code == 404


def test_delete_works():
    create = client.post(
        "/api/v1/users/",
        json={
            "username": "byebye",
            "email": "bye@example.com",
        },
    )
    uid = create.json()["id"]
    resp = client.delete(f"/api/v1/users/{uid}")
    assert resp.status_code == 204
