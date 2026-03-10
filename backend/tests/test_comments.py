def test_comment_flow(client, auth_header):
    t = client.post(
        "/projects/1/tickets",
        headers=auth_header,
        json={"title": "Discuss", "body": "context", "ticket_type": "task"},
    ).json()
    post = client.post(f"/tickets/{t['id']}/comments", headers=auth_header, json={"body": "LGTM"})
    assert post.status_code == 200
    listed = client.get(f"/tickets/{t['id']}/comments", headers=auth_header)
    assert len(listed.json()) == 1
