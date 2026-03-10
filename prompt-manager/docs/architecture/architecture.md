---
name: Architecture
---

# Architecture

## Frontend

- **Framework:** Dash (Python)
- Single-page application
- No routing required — state managed within the single page

## Service

- **Framework:** FastAPI
- REST API only — no auth, no cache
- Runs locally, consumed by the Dash frontend

## Data Models

> Full field definitions are in [`product-requirements.md`](../product/product-requirements.md).

### Prompt

| Field              | Type          | Required | Notes                                       |
|--------------------|---------------|----------|---------------------------------------------|
| `id`               | string (UUID) | yes      | Auto-generated                              |
| `name`             | string        | yes      |                                             |
| `description`      | string        | no       |                                             |
| `content`          | string        | yes      | Markdown body                               |
| `tags`             | string[]      | no       | Free-form, multiple allowed                 |
| `template_id`      | string (UUID) | no       | Set if created from a template              |
| `variable_values`  | map[str, str] | no       | Filled variable values if from a template   |
| `created_datetime` | datetime      | yes      | Auto-set on creation                        |
| `updated_datetime` | datetime      | yes      | Auto-updated on edit                        |

### Template

| Field              | Type          | Required | Notes                                           |
|--------------------|---------------|----------|-------------------------------------------------|
| `id`               | string (UUID) | yes      | Auto-generated                                  |
| `name`             | string        | yes      |                                                 |
| `description`      | string        | no       |                                                 |
| `content`          | string        | yes      | Markdown with `{{variable_name}}` placeholders  |
| `variables`        | Variable[]    | no       | List of variable definitions (see below)        |
| `created_datetime` | datetime      | yes      | Auto-set on creation                            |
| `updated_datetime` | datetime      | yes      | Auto-updated on edit                            |

### Variable (nested in Template)

| Field         | Type   | Required | Notes                                                        |
|---------------|--------|----------|--------------------------------------------------------------|
| `name`        | string | yes      | Matches placeholder in content, e.g. `role` for `{{role}}`  |
| `description` | string | yes      | Shown to user when filling in the value                      |

## Components

### Entities

- `Prompt`
- `Template`

### Use Cases

- Create / Read / Update / Delete Prompt
- Create / Read / Update / Delete Template
- Create Prompt from Template (variable substitution)
- Search Prompts (name, description, content)
- Search Templates (name, description)
- Export Prompt (md, yaml, json)

## API Design

### Prompt Endpoints

| Method     | Endpoint               | Description                                                                                      |
|------------|------------------------|--------------------------------------------------------------------------------------------------|
| `GET`      | `/prompts`             | List all prompts (supports search — see Query Parameters)                                        |
| `POST`     | `/prompts`             | Create a new prompt                                                                              |
| `GET`      | `/prompts/{id}`        | Get a single prompt                                                                              |
| `PUT`      | `/prompts/{id}`        | Update a prompt                                                                                  |
| `DELETE`   | `/prompts/{id}`        | Delete a prompt                                                                                  |
| `GET`      | `/prompts/{id}/export` | Export prompt (`?format=md\|yaml\|json`) — returns file download with Content-Disposition header |

### Template Endpoints

| Method     | Endpoint                               | Description                                                     |
|------------|----------------------------------------|-----------------------------------------------------------------|
| `GET`      | `/templates`                           | List all templates (supports search — see Query Parameters)     |
| `POST`     | `/templates`                           | Create a new template                                           |
| `GET`      | `/templates/{id}`                      | Get a single template                                           |
| `PUT`      | `/templates/{id}`                      | Update a template                                               |
| `DELETE`   | `/templates/{id}`                      | Delete a template                                               |
| `POST`     | `/templates/{template_id}/instantiate` | Instantiate a prompt from this template (variable substitution) |

### Query Parameters

No pagination — all matching results are returned. This is intentional for a local single-user app.

#### GET /prompts

| Parameter | Type   | Description                                                                              |
|-----------|--------|------------------------------------------------------------------------------------------|
| `q`       | string | Full-text search across `name`, `description`, `content`                                 |
| `tags`    | string | Comma-separated tag filter, e.g. `?tags=gpt,creative` (OR logic — any tag matches)       |

#### GET /templates

| Parameter | Type   | Description                            |
|-----------|--------|----------------------------------------|
| `q`       | string | Search across `name` and `description` |

### Instantiate Request Body

`POST /templates/{template_id}/instantiate`

```json
{
  "variable_values": {
    "variable_name": "value"
  }
}
```

- Keys must match the `{{variable_name}}` placeholders defined in the template's `variables` list
- Returns a fully formed `Prompt` object with placeholders substituted

### Export Response Contract

`GET /prompts/{id}/export?format=md|yaml|json` returns a **file download**:

| Format | Content-Type         | Filename             |
|--------|----------------------|----------------------|
| `md`   | `text/markdown`      | `{prompt_name}.md`   |
| `yaml` | `application/x-yaml` | `{prompt_name}.yaml` |
| `json` | `application/json`   | `{prompt_name}.json` |

- `Content-Disposition: attachment; filename={prompt_name}.{format}`
- Response body is raw file content — not a JSON wrapper

## Storage

- **Database:** MongoDB
- **Deployment:** Docker (docker-compose)
- **Collections:** `prompts`, `templates`

### ID Strategy

- Each document stores both:
  - `_id`: MongoDB ObjectId (internal, never exposed in API responses)
  - `id`: UUID string (public, used in all API endpoints and Pydantic models)
- All routes reference `id` (UUID). MongoDB queries use `{"id": <uuid_string>}`.
- A unique index on `id` must be created at startup for both collections to avoid full collection scans:

  ```python
  collection.create_index("id", unique=True)
  ```

## Error Responses

FastAPI's default error shape is used throughout — no custom exception handlers required.

| Status | When                       | Body                                    |
|--------|----------------------------|-----------------------------------------|
| `404`  | Resource not found         | `{"detail": "Not found"}`               |
| `422`  | Request validation failure | `{"detail": [{"msg": "...", ...}]}`     |
| `500`  | Unexpected server error    | `{"detail": "Internal server error"}`   |

- The Dash frontend reads `response["detail"]` to display error messages.
- No custom error envelope — rely on FastAPI defaults.

## Infrastructure

- `docker-compose.yml` runs MongoDB
- FastAPI runs locally via Uvicorn (`uvicorn main:app --reload`)
- Dash app runs locally (`python app.py`)
- `.env` file for config (Mongo connection string, API base URL)
