def test_export_md_triggers_download(client):
    create = client.post("/prompts", json={"name": "My Prompt", "content": "# Hello"})
    prompt_id = create.json()["id"]

    resp = client.get(f"/prompts/{prompt_id}/export?format=md")
    assert resp.status_code == 200
    assert len(resp.content) > 0
    assert resp.headers["content-disposition"].endswith(".md")


def test_export_yaml_triggers_download(client):
    create = client.post("/prompts", json={"name": "My Prompt", "content": "body"})
    prompt_id = create.json()["id"]

    resp = client.get(f"/prompts/{prompt_id}/export?format=yaml")
    assert resp.status_code == 200
    assert len(resp.content) > 0
    assert resp.headers["content-disposition"].endswith(".yaml")


def test_export_json_triggers_download(client):
    create = client.post("/prompts", json={"name": "My Prompt", "content": "body"})
    prompt_id = create.json()["id"]

    resp = client.get(f"/prompts/{prompt_id}/export?format=json")
    assert resp.status_code == 200
    assert len(resp.content) > 0
    assert resp.headers["content-disposition"].endswith(".json")


def test_export_no_prompt_selected(client):
    resp = client.get("/prompts/nonexistent-id/export?format=md")
    assert resp.status_code == 404
