PNG = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]) + b"rest"


def test_upload_png(client, auth_header):
    t = client.post(
        "/projects/1/tickets",
        headers=auth_header,
        json={"title": "Shot", "body": "see attach", "ticket_type": "task"},
    ).json()
    files = {"file": ("shot.png", PNG, "image/png")}
    r = client.post(f"/tickets/{t['id']}/attachments", headers=auth_header, files=files)
    assert r.status_code == 200


def test_reject_bad_mime(client, auth_header):
    t = client.post(
        "/projects/1/tickets",
        headers=auth_header,
        json={"title": "Bin", "body": "nope", "ticket_type": "task"},
    ).json()
    files = {"file": ("x.exe", b"MZ", "application/octet-stream")}
    r = client.post(f"/tickets/{t['id']}/attachments", headers=auth_header, files=files)
    assert r.status_code == 400
