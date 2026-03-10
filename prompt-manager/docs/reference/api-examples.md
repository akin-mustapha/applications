---
name: API Examples
---

# API Examples

Concrete request and response examples for every Prompt Manager endpoint. The API runs at `http://localhost:8000` by default.

---

## Prompts

### Create a Prompt

**`POST /prompts`**

```bash
curl -X POST http://localhost:8000/prompts \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Code Review Prompt",
    "description": "Asks Claude to review Python code for quality and bugs",
    "content": "Please review the following Python code for quality, bugs, and style issues:\n\n```python\n{{code}}\n```",
    "tags": ["code-review", "python"]
  }'
```

**Response `201 Created`:**

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "name": "Code Review Prompt",
  "description": "Asks Claude to review Python code for quality and bugs",
  "content": "Please review the following Python code for quality, bugs, and style issues:\n\n```python\n{{code}}\n```",
  "tags": ["code-review", "python"],
  "template_id": null,
  "variable_values": null,
  "created_datetime": "2024-01-15T10:30:00Z",
  "updated_datetime": "2024-01-15T10:30:00Z"
}
```

---

### List All Prompts

**`GET /prompts`**

```bash
curl http://localhost:8000/prompts
```

**Response `200 OK`:**

```json
[
  {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "name": "Code Review Prompt",
    "description": "Asks Claude to review Python code for quality and bugs",
    "content": "Please review the following Python code...",
    "tags": ["code-review", "python"],
    "template_id": null,
    "variable_values": null,
    "created_datetime": "2024-01-15T10:30:00Z",
    "updated_datetime": "2024-01-15T10:30:00Z"
  }
]
```

---

### Search Prompts by Text

**`GET /prompts?q={query}`**

Searches across `name`, `description`, and `content`.

```bash
curl "http://localhost:8000/prompts?q=code+review"
```

---

### Filter Prompts by Tags

**`GET /prompts?tags={tag1,tag2}`**

OR logic — returns prompts matching any of the specified tags.

```bash
# Single tag
curl "http://localhost:8000/prompts?tags=python"

# Multiple tags (OR)
curl "http://localhost:8000/prompts?tags=python,code-review"
```

---

### Search + Tag Filter Combined

```bash
curl "http://localhost:8000/prompts?q=review&tags=python"
```

---

### Get a Single Prompt

**`GET /prompts/{id}`**

```bash
curl http://localhost:8000/prompts/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**Response `200 OK`:** Same shape as the create response above.

**Response `404 Not Found`:**

```json
{
  "detail": "Not found"
}
```

---

### Update a Prompt

**`PUT /prompts/{id}`**

Send only the fields you want to update.

```bash
curl -X PUT http://localhost:8000/prompts/a1b2c3d4-e5f6-7890-abcd-ef1234567890 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Code Review Prompt v2",
    "tags": ["code-review", "python", "quality"]
  }'
```

**Response `200 OK`:** Returns the full updated prompt object. `updated_datetime` is refreshed automatically.

---

### Delete a Prompt

**`DELETE /prompts/{id}`**

```bash
curl -X DELETE http://localhost:8000/prompts/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**Response `204 No Content`:** Empty body.

**Response `404 Not Found`:**

```json
{
  "detail": "Not found"
}
```

---

### Export a Prompt

**`GET /prompts/{id}/export?format={md|yaml|json}`**

The response is a file download, not a JSON wrapper.

**Export as Markdown:**

```bash
curl -O http://localhost:8000/prompts/a1b2c3d4-e5f6-7890-abcd-ef1234567890/export?format=md
```

**Export as YAML:**

```bash
curl -O http://localhost:8000/prompts/a1b2c3d4-e5f6-7890-abcd-ef1234567890/export?format=yaml
```

**Export as JSON:**

```bash
curl -O http://localhost:8000/prompts/a1b2c3d4-e5f6-7890-abcd-ef1234567890/export?format=json
```

**Response headers:**

| Format | `Content-Type` | `Content-Disposition` |
|--------|----------------|-----------------------|
| `md` | `text/markdown` | `attachment; filename=Code Review Prompt.md` |
| `yaml` | `application/x-yaml` | `attachment; filename=Code Review Prompt.yaml` |
| `json` | `application/json` | `attachment; filename=Code Review Prompt.json` |

---

## Templates

### Create a Template

**`POST /templates`**

```bash
curl -X POST http://localhost:8000/templates \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Role-Based Assistant",
    "description": "Generic template for creating a role-specific assistant prompt",
    "content": "You are a {{role}} with expertise in {{domain}}.\n\nYour task is to {{task}}.\n\nRespond in a {{tone}} tone.",
    "variables": [
      {
        "name": "role",
        "description": "The professional role the assistant should adopt, e.g. Senior Python Developer"
      },
      {
        "name": "domain",
        "description": "The area of expertise, e.g. distributed systems, data engineering"
      },
      {
        "name": "task",
        "description": "The specific task the assistant should perform"
      },
      {
        "name": "tone",
        "description": "The tone of response: formal, casual, concise, detailed"
      }
    ]
  }'
```

**Response `201 Created`:**

```json
{
  "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "name": "Role-Based Assistant",
  "description": "Generic template for creating a role-specific assistant prompt",
  "content": "You are a {{role}} with expertise in {{domain}}.\n\nYour task is to {{task}}.\n\nRespond in a {{tone}} tone.",
  "variables": [
    { "name": "role", "description": "The professional role the assistant should adopt" },
    { "name": "domain", "description": "The area of expertise" },
    { "name": "task", "description": "The specific task the assistant should perform" },
    { "name": "tone", "description": "The tone of response" }
  ],
  "created_datetime": "2024-01-15T11:00:00Z",
  "updated_datetime": "2024-01-15T11:00:00Z"
}
```

---

### List All Templates

**`GET /templates`**

```bash
curl http://localhost:8000/templates
```

---

### Search Templates

**`GET /templates?q={query}`**

Searches across `name` and `description`.

```bash
curl "http://localhost:8000/templates?q=role"
```

---

### Get a Single Template

**`GET /templates/{id}`**

```bash
curl http://localhost:8000/templates/b2c3d4e5-f6a7-8901-bcde-f12345678901
```

---

### Update a Template

**`PUT /templates/{id}`**

```bash
curl -X PUT http://localhost:8000/templates/b2c3d4e5-f6a7-8901-bcde-f12345678901 \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated description for role-based assistant template"
  }'
```

---

### Delete a Template

**`DELETE /templates/{id}`**

```bash
curl -X DELETE http://localhost:8000/templates/b2c3d4e5-f6a7-8901-bcde-f12345678901
```

**Response `204 No Content`:** Empty body.

---

### Instantiate a Template (Create Prompt from Template)

**`POST /templates/{template_id}/instantiate`**

Fills in all `{{variable_name}}` placeholders and returns a new `Prompt` object.

```bash
curl -X POST http://localhost:8000/templates/b2c3d4e5-f6a7-8901-bcde-f12345678901/instantiate \
  -H "Content-Type: application/json" \
  -d '{
    "variable_values": {
      "role": "Senior Python Developer",
      "domain": "distributed systems",
      "task": "review this FastAPI service for performance issues",
      "tone": "concise"
    }
  }'
```

**Response `201 Created`:** Returns a fully formed `Prompt` with all placeholders substituted:

```json
{
  "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
  "name": "Role-Based Assistant",
  "description": "Generic template for creating a role-specific assistant prompt",
  "content": "You are a Senior Python Developer with expertise in distributed systems.\n\nYour task is to review this FastAPI service for performance issues.\n\nRespond in a concise tone.",
  "tags": [],
  "template_id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "variable_values": {
    "role": "Senior Python Developer",
    "domain": "distributed systems",
    "task": "review this FastAPI service for performance issues",
    "tone": "concise"
  },
  "created_datetime": "2024-01-15T11:30:00Z",
  "updated_datetime": "2024-01-15T11:30:00Z"
}
```

---

## Error Responses

All errors use FastAPI's default shape.

**`422 Unprocessable Entity`** — missing required field:

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "name"],
      "msg": "Field required",
      "input": {}
    }
  ]
}
```

**`404 Not Found`:**

```json
{
  "detail": "Not found"
}
```

**`500 Internal Server Error`:**

```json
{
  "detail": "Internal server error"
}
```
