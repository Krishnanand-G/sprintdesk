import pytest


def test_login_ok(client):
    r = client.post("/auth/login", data={"username": "triager@local.dev", "password": "triager123"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_bad(client):
    r = client.post("/auth/login", data={"username": "triager@local.dev", "password": "nope"})
    assert r.status_code == 400


def test_register_and_me(client):
    r = client.post("/auth/register", json={"email": "dev@local.dev", "password": "secret1", "display_name": "Dev"})
    assert r.status_code == 200
    login = client.post("/auth/login", data={"username": "dev@local.dev", "password": "secret1"})
    token = login.json()["access_token"]
    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.json()["email"] == "dev@local.dev"


@pytest.mark.parametrize("path", ["/projects", "/projects/1/tickets"])
def test_routes_need_auth(client, path):
    r = client.get(path)
    assert r.status_code == 401
