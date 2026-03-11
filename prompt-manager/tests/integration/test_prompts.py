def test_create_prompt(client):
    resp = client.post("/prompts", json={"name": "My Prompt", "content": "Hello world"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["name"] == "My Prompt"
    assert body["content"] == "Hello world"
    assert "id" in body
    assert "created_datetime" in body


def test_get_prompt(client):
    create = client.post("/prompts", json={"name": "Get Test", "content": "body"})
    prompt_id = create.json()["id"]

    resp = client.get(f"/prompts/{prompt_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == prompt_id


def test_get_prompt_not_found(client):
    resp = client.get("/prompts/nonexistent-id")
    assert resp.status_code == 404


def test_list_prompts(client):
    client.post("/prompts", json={"name": "A", "content": "one"})
    client.post("/prompts", json={"name": "B", "content": "two"})

    resp = client.get("/prompts")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_search_prompts_by_q(client):
    client.post("/prompts", json={"name": "Alpha prompt", "content": "irrelevant"})
    client.post("/prompts", json={"name": "Beta prompt", "content": "irrelevant"})

    resp = client.get("/prompts?q=Alpha")
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) == 1
    assert results[0]["name"] == "Alpha prompt"


def test_filter_prompts_by_tags(client):
    client.post("/prompts", json={"name": "Tagged", "content": "x", "tags": ["gpt"]})
    client.post("/prompts", json={"name": "Untagged", "content": "y", "tags": []})

    resp = client.get("/prompts?tags=gpt")
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) == 1
    assert results[0]["name"] == "Tagged"


def test_filter_prompts_by_multiple_tags(client):
    client.post("/prompts", json={"name": "P1", "content": "x", "tags": ["gpt"]})
    client.post("/prompts", json={"name": "P2", "content": "y", "tags": ["creative"]})
    client.post("/prompts", json={"name": "P3", "content": "z", "tags": ["other"]})

    resp = client.get("/prompts?tags=gpt,creative")
    assert resp.status_code == 200
    names = {p["name"] for p in resp.json()}
    assert names == {"P1", "P2"}


def test_update_prompt(client):
    create = client.post("/prompts", json={"name": "Old Name", "content": "old"})
    prompt_id = create.json()["id"]

    resp = client.put(f"/prompts/{prompt_id}", json={"name": "New Name"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "New Name"
    assert resp.json()["content"] == "old"


def test_delete_prompt(client):
    create = client.post("/prompts", json={"name": "To Delete", "content": "bye"})
    prompt_id = create.json()["id"]

    resp = client.delete(f"/prompts/{prompt_id}")
    assert resp.status_code == 200
    assert resp.json() == {"deleted": True}

    get_resp = client.get(f"/prompts/{prompt_id}")
    assert get_resp.status_code == 404


def test_delete_prompt_not_found(client):
    resp = client.delete("/prompts/nonexistent-id")
    assert resp.status_code == 404
