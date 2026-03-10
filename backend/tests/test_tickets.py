import pytest
from app.models import Severity


@pytest.mark.parametrize("severity", list(Severity))
def test_bug_auto_assign(client, auth_header, severity):
    r = client.post(
        "/projects/1/tickets",
        headers=auth_header,
        json={
            "title": f"Bug {severity.value}",
            "body": "steps to repro",
            "ticket_type": "bug",
            "severity": severity.value,
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["sla_hours"] is not None
    if severity.value in ("high", "critical"):
        assert data["assignee_id"] == 1
    else:
        assert data["assignee_id"] is None


def test_story_rejects_severity(client, auth_header):
    r = client.post(
        "/projects/1/tickets",
        headers=auth_header,
        json={"title": "Story one", "body": "", "ticket_type": "story", "severity": "low"},
    )
    assert r.status_code == 400


def test_patch_status(client, auth_header):
    created = client.post(
        "/projects/1/tickets",
        headers=auth_header,
        json={"title": "Task move", "body": "work", "ticket_type": "task"},
    ).json()
    tid = created["id"]
    r = client.patch(f"/tickets/{tid}", headers=auth_header, json={"status": "doing"})
    assert r.status_code == 200
    assert r.json()["status"] == "doing"
