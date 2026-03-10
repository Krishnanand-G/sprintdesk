from datetime import date


def test_create_sprint_and_board(client, auth_header):
    sprint = client.post(
        "/projects/1/sprints",
        headers=auth_header,
        json={"name": "S1", "start_date": "2025-07-01", "end_date": "2025-07-14", "status": "active"},
    )
    assert sprint.status_code == 200
    sid = sprint.json()["id"]
    board = client.get(f"/projects/1/sprints/{sid}/board-summary", headers=auth_header)
    assert board.status_code == 200
    data = board.json()
    assert data["backlog"] == 0
    assert data["done"] == 0
