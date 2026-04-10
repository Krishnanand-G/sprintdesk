import pytest


@pytest.mark.parametrize("ticket_type", ["story", "bug", "task"])
def test_create_types(client, auth_header, ticket_type):
    body = {"title": f"Type {ticket_type}", "body": "desc", "ticket_type": ticket_type}
    if ticket_type == "bug":
        body["severity"] = "medium"
    r = client.post("/projects/1/tickets", headers=auth_header, json=body)
    assert r.status_code == 200
    assert r.json()["ticket_type"] == ticket_type


@pytest.mark.parametrize("status", ["backlog", "todo", "doing", "done"])
def test_list_after_status_set(client, auth_header, status):
    r = client.post(
        "/projects/1/tickets",
        headers=auth_header,
        json={"title": f"Move {status}", "body": "x", "ticket_type": "task", "status": status},
    )
    assert r.status_code == 200
    listed = client.get("/projects/1/tickets", headers=auth_header)
    assert any(t["status"] == status for t in listed.json())
