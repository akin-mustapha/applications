def test_variable_form_renders_on_template_select(client):
    resp = client.post(
        "/templates",
        json={
            "name": "Form Template",
            "content": "Hello {{name}}, your role is {{role}}.",
            "variables": [
                {"name": "name", "description": "Recipient name"},
                {"name": "role", "description": "Recipient role"},
            ],
        },
    )
    template_id = resp.json()["id"]

    get_resp = client.get(f"/templates/{template_id}")
    assert get_resp.status_code == 200
    variables = get_resp.json()["variables"]
    assert len(variables) == 2
    assert variables[0]["name"] == "name"
    assert variables[0]["description"] == "Recipient name"
    assert variables[1]["name"] == "role"
    assert variables[1]["description"] == "Recipient role"


def test_instantiation_callback_success(client):
    create = client.post(
        "/templates",
        json={
            "name": "Greeting",
            "content": "Hello {{name}}, you are a {{role}}.",
            "variables": [
                {"name": "name", "description": "Name"},
                {"name": "role", "description": "Role"},
            ],
        },
    )
    template_id = create.json()["id"]

    resp = client.post(
        f"/templates/{template_id}/instantiate",
        json={"variable_values": {"name": "Alice", "role": "engineer"}},
    )
    assert resp.status_code == 201
    assert resp.json()["content"] == "Hello Alice, you are a engineer."


def test_instantiation_callback_missing_template(client):
    resp = client.post(
        "/templates/nonexistent-id/instantiate",
        json={"variable_values": {"name": "Alice"}},
    )
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"].lower()


def test_form_resets_after_instantiation(client):
    create = client.post(
        "/templates",
        json={
            "name": "Reset Test",
            "content": "Task: {{task}}",
            "variables": [{"name": "task", "description": "The task"}],
        },
    )
    template_id = create.json()["id"]

    resp = client.post(
        f"/templates/{template_id}/instantiate",
        json={"variable_values": {"task": "write tests"}},
    )
    assert resp.status_code == 201
    body = resp.json()
    # Prompt has template_id recorded (used by Dash to clear template store)
    assert body["template_id"] == template_id
    # Returned object is a Prompt — no variables field (template form hides on reset)
    assert "variables" not in body
    # Prompt is persisted and retrievable
    prompt_id = body["id"]
    get_resp = client.get(f"/prompts/{prompt_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["content"] == "Task: write tests"
