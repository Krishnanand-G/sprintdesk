import pytest
from app.models import TicketStatus


@pytest.mark.parametrize("status", list(TicketStatus))
def test_board_counts_status(client, auth_header, status):
    sprint = client.post(
        "/projects/1/sprints",
        headers=auth_header,
        json={"name": "Board", "start_date": "2025-07-01", "end_date": "2025-07-14", "status": "active"},
    ).json()
    sid = sprint["id"]
    client.post(
        "/projects/1/tickets",
        headers=auth_header,
        json={"title": f"Item {status.value}", "body": "x", "ticket_type": "task", "status": status.value, "sprint_id": sid},
    )
    board = client.get(f"/projects/1/sprints/{sid}/board-summary", headers=auth_header).json()
    assert board[status.value] >= 1


@pytest.mark.parametrize(
    "title,expect",
    [("ab", 422), ("valid title", 200)],
)
def test_ticket_title_length(client, auth_header, title, expect):
    r = client.post(
        "/projects/1/tickets",
        headers=auth_header,
        json={"title": title, "body": "long enough body", "ticket_type": "task"},
    )
    assert r.status_code == expect
