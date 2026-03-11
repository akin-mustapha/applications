def test_create_template(client):
    resp = client.post(
        "/templates",
        json={
            "name": "My Template",
            "content": "Hello {{name}}",
            "variables": [{"name": "name", "description": "The recipient"}],
        },
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["name"] == "My Template"
    assert len(body["variables"]) == 1
    assert "id" in body
    assert "created_datetime" in body


def test_get_template(client):
    create = client.post(
        "/templates", json={"name": "Get Test", "content": "body"}
    )
    template_id = create.json()["id"]

    resp = client.get(f"/templates/{template_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == template_id


def test_get_template_not_found(client):
    resp = client.get("/templates/nonexistent-id")
    assert resp.status_code == 404


def test_list_templates(client):
    client.post("/templates", json={"name": "T1", "content": "a"})
    client.post("/templates", json={"name": "T2", "content": "b"})

    resp = client.get("/templates")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_search_templates(client):
    client.post("/templates", json={"name": "Greeting", "content": "hi", "description": "A greeting template"})
    client.post("/templates", json={"name": "Other", "content": "bye", "description": "unrelated"})

    resp = client.get("/templates?q=Greeting")
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) == 1
    assert results[0]["name"] == "Greeting"


def test_update_template(client):
    create = client.post("/templates", json={"name": "Old Name", "content": "old"})
    template_id = create.json()["id"]

    resp = client.put(f"/templates/{template_id}", json={"name": "New Name"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "New Name"
    assert resp.json()["content"] == "old"


def test_delete_template(client):
    create = client.post("/templates", json={"name": "To Delete", "content": "bye"})
    template_id = create.json()["id"]

    resp = client.delete(f"/templates/{template_id}")
    assert resp.status_code == 200
    assert resp.json() == {"deleted": True}

    get_resp = client.get(f"/templates/{template_id}")
    assert get_resp.status_code == 404


def test_instantiate_template(client):
    create = client.post(
        "/templates",
        json={
            "name": "Greeting",
            "content": "Hello {{name}}, you are a {{role}}.",
            "variables": [
                {"name": "name", "description": "Recipient name"},
                {"name": "role", "description": "Recipient role"},
            ],
        },
    )
    template_id = create.json()["id"]

    resp = client.post(
        f"/templates/{template_id}/instantiate",
        json={"variable_values": {"name": "Alice", "role": "engineer"}},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["content"] == "Hello Alice, you are a engineer."
    assert body["template_id"] == template_id
    assert body["variable_values"] == {"name": "Alice", "role": "engineer"}
    assert "id" in body


def test_instantiate_template_not_found(client):
    resp = client.post(
        "/templates/nonexistent-id/instantiate",
        json={"variable_values": {}},
    )
    assert resp.status_code == 404


def test_instantiate_missing_variable(client):
    create = client.post(
        "/templates",
        json={
            "name": "Partial",
            "content": "Hello {{name}}, role: {{role}}.",
            "variables": [
                {"name": "name", "description": "Name"},
                {"name": "role", "description": "Role"},
            ],
        },
    )
    template_id = create.json()["id"]

    # Only one variable provided — missing variable placeholder stays in content
    resp = client.post(
        f"/templates/{template_id}/instantiate",
        json={"variable_values": {"name": "Alice"}},
    )
    assert resp.status_code == 201
    assert resp.json()["content"] == "Hello Alice, role: {{role}}."


def test_instantiate_extra_variable(client):
    create = client.post(
        "/templates",
        json={
            "name": "Simple",
            "content": "Hello {{name}}.",
            "variables": [{"name": "name", "description": "Name"}],
        },
    )
    template_id = create.json()["id"]

    # Extra variable not in template — silently ignored
    resp = client.post(
        f"/templates/{template_id}/instantiate",
        json={"variable_values": {"name": "Bob", "extra": "ignored"}},
    )
    assert resp.status_code == 201
    assert resp.json()["content"] == "Hello Bob."
