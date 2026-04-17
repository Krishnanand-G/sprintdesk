def test_list_projects(client, auth_header):
    r = client.get("/projects", headers=auth_header)
    assert r.status_code == 200
    assert len(r.json()) >= 1


def test_create_project(client, auth_header):
    r = client.post("/projects", headers=auth_header, json={"name": "Mobile", "key": "MOB"})
    assert r.status_code == 200
    assert r.json()["key"] == "MOB"

def test_get_project(client, auth_header):
    r = client.get("/projects/1", headers=auth_header)
    assert r.status_code == 200
    assert r.json()["key"] == "DESK"
