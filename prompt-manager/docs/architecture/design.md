---
name: Design
---

# Design

Consolidated technical design for Prompt Manager — extracted from architecture, product, and business requirements.

---

## 1. System Overview

Prompt Manager is a local, single-user tool for an AI Engineer to create, search, reuse, and export prompt files. All data is stored in a local MongoDB instance — no cloud, no auth, no external dependencies beyond Docker.

**Goals:**
- Find any prompt in under 10 seconds via search
- Create reusable templates with variable placeholders and instantiate prompts from them
- Export any prompt as `.md`, `.yaml`, or `.json`

**Scope constraints (v1):**
- Single user, local only
- No authentication
- No caching
- No edit history / versioning
- No cloud dependency

---

## 2. Architecture

Three-tier architecture, all running locally:

```text
+------------------+       HTTP REST       +------------------+       pymongo       +------------------+
|                  | --------------------> |                  | ------------------> |                  |
|   Dash Frontend  |                       |  FastAPI Service  |                    |     MongoDB       |
|   (Python SPA)   | <-------------------- |   (Uvicorn)       | <------------------ |  (docker-compose) |
|                  |       JSON            |                  |       documents     |                  |
+------------------+                       +------------------+                     +------------------+
```

| Layer      | Technology     | How it runs                    |
|------------|----------------|--------------------------------|
| Frontend   | Dash (Python)  | `python app.py` (local)        |
| Backend    | FastAPI        | `uvicorn main:app --reload`    |
| Database   | MongoDB        | `docker-compose up`            |
| Config     | `.env` file    | Mongo connection string, API base URL |

- Frontend is a single-page application — no routing, all state managed within the page
- Backend is REST only — no auth middleware, no cache layer
- MongoDB runs in Docker; FastAPI and Dash run directly on the host

---

## 3. Data Models

### Prompt

| Field              | Type          | Required | Notes                                      |
|--------------------|---------------|----------|--------------------------------------------|
| `id`               | string (UUID) | yes      | Auto-generated; public API identifier      |
| `name`             | string        | yes      |                                            |
| `description`      | string        | no       |                                            |
| `content`          | string        | yes      | Markdown body                              |
| `tags`             | string[]      | no       | Free-form, multiple allowed                |
| `template_id`      | string (UUID) | no       | Set if created from a template             |
| `variable_values`  | map[str, str] | no       | Filled variable values if from a template  |
| `created_datetime` | datetime      | yes      | Auto-set on creation                       |
| `updated_datetime` | datetime      | yes      | Auto-updated on every edit                 |

### Template

| Field              | Type          | Required | Notes                                           |
|--------------------|---------------|----------|-------------------------------------------------|
| `id`               | string (UUID) | yes      | Auto-generated; public API identifier           |
| `name`             | string        | yes      |                                                 |
| `description`      | string        | no       |                                                 |
| `content`          | string        | yes      | Markdown with `{{variable_name}}` placeholders  |
| `variables`        | Variable[]    | no       | List of variable definitions (see below)        |
| `created_datetime` | datetime      | yes      | Auto-set on creation                            |
| `updated_datetime` | datetime      | yes      | Auto-updated on every edit                      |

### Variable (nested in Template)

| Field         | Type   | Required | Notes                                                       |
|---------------|--------|----------|-------------------------------------------------------------|
| `name`        | string | yes      | Matches placeholder in content, e.g. `role` for `{{role}}` |
| `description` | string | yes      | Shown to user when filling in the value                     |

### Storage Details

- **Collections:** `prompts`, `templates`
- **ID strategy:** Each document stores `_id` (MongoDB ObjectId, internal only) and `id` (UUID string, exposed in all API responses and routes)
- **Index:** Unique index on `id` must be created at startup for both collections:
  ```python
  collection.create_index("id", unique=True)
  ```

---

## 4. Use Cases

| Use Case                        | Description                                                                 |
|---------------------------------|-----------------------------------------------------------------------------|
| Create Prompt                   | Create a new prompt with name, content, optional description and tags       |
| Read / List Prompts             | Retrieve a single prompt or list all (with optional search/tag filter)      |
| Update Prompt                   | Edit any field on an existing prompt                                        |
| Delete Prompt                   | Remove a prompt permanently                                                 |
| Create Template                 | Create a template with `{{variable_name}}` placeholders and variable defs   |
| Read / List Templates           | Retrieve a single template or list all (with optional search)               |
| Update Template                 | Edit any field on an existing template                                      |
| Delete Template                 | Remove a template permanently                                               |
| Create Prompt from Template     | Fill variable values, substitute placeholders, produce a new Prompt         |
| Search Prompts                  | Full-text search across `name`, `description`, `content`; filter by tags    |
| Search Templates                | Search across `name` and `description`                                      |
| Export Prompt                   | Download prompt as `.md`, `.yaml`, or `.json`                               |

---

## 5. API Design

### Prompt Endpoints

| Method   | Endpoint                  | Description                                                                        |
|----------|---------------------------|------------------------------------------------------------------------------------|
| `GET`    | `/prompts`                | List all prompts — supports `q` and `tags` query params                           |
| `POST`   | `/prompts`                | Create a new prompt                                                                |
| `GET`    | `/prompts/{id}`           | Get a single prompt by UUID                                                        |
| `PUT`    | `/prompts/{id}`           | Update a prompt                                                                    |
| `DELETE` | `/prompts/{id}`           | Delete a prompt                                                                    |
| `GET`    | `/prompts/{id}/export`    | Export prompt as file (`?format=md\|yaml\|json`)                                  |

### Template Endpoints

| Method   | Endpoint                               | Description                                                  |
|----------|----------------------------------------|--------------------------------------------------------------|
| `GET`    | `/templates`                           | List all templates — supports `q` query param               |
| `POST`   | `/templates`                           | Create a new template                                        |
| `GET`    | `/templates/{id}`                      | Get a single template by UUID                               |
| `PUT`    | `/templates/{id}`                      | Update a template                                            |
| `DELETE` | `/templates/{id}`                      | Delete a template                                            |
| `POST`   | `/templates/{template_id}/instantiate` | Instantiate a prompt from a template (variable substitution) |

### Query Parameters

No pagination — all matching results are returned (single-user local app).

**GET /prompts**

| Parameter | Type   | Description                                                               |
|-----------|--------|---------------------------------------------------------------------------|
| `q`       | string | Full-text search across `name`, `description`, `content`                  |
| `tags`    | string | Comma-separated tag filter, e.g. `?tags=gpt,creative` (OR logic)         |

**GET /templates**

| Parameter | Type   | Description                          |
|-----------|--------|--------------------------------------|
| `q`       | string | Search across `name`, `description`  |

### Instantiate Request Body

`POST /templates/{template_id}/instantiate`

```json
{
  "variable_values": {
    "variable_name": "value"
  }
}
```

- Keys must match `{{variable_name}}` placeholders defined in the template's `variables` list
- Returns a fully formed `Prompt` object with all placeholders substituted

### Export Response Contract

`GET /prompts/{id}/export?format=md|yaml|json`

| Format | Content-Type         | Filename             |
|--------|----------------------|----------------------|
| `md`   | `text/markdown`      | `{prompt_name}.md`   |
| `yaml` | `application/x-yaml` | `{prompt_name}.yaml` |
| `json` | `application/json`   | `{prompt_name}.json` |

- `Content-Disposition: attachment; filename={prompt_name}.{format}`
- Response body is raw file content — not a JSON wrapper

### Error Responses

FastAPI defaults used throughout — no custom exception handlers.

| Status | When                       | Body                                  |
|--------|----------------------------|---------------------------------------|
| `404`  | Resource not found         | `{"detail": "Not found"}`             |
| `422`  | Request validation failure | `{"detail": [{"msg": "...", ...}]}`   |
| `500`  | Unexpected server error    | `{"detail": "Internal server error"}` |

The Dash frontend reads `response["detail"]` to display error messages.

---

## 6. UI Layout

Three-pane layout:

```text
+------------------------------------------+------------------+
|                                          |                  |
|         CENTER: Editor (split)           |  RIGHT SIDEBAR   |
|   [Markdown Editor] | [Live Preview]     |                  |
|                                          |  - Prompt list   |
|                                          |  - Template list |
|                                          |  - Search bar    |
+------------------------------------------+  - New buttons   |
|                                          |                  |
|         BOTTOM PANE                      +------------------+
|                                          |
|  - Metadata: name, description, tags     |
|  - Template variable input form          |
|    (shown when creating from template)   |
|  - Export controls                       |
+------------------------------------------+
```

| Pane           | Contents                                                                           |
|----------------|------------------------------------------------------------------------------------|
| Center (main)  | Split markdown editor (left) and live preview (right)                             |
| Bottom         | Metadata fields (name, description, tags), template variable form, export actions |
| Right sidebar  | Navigation: prompt list, template list, search bar, create new buttons            |

---

## 7. Infrastructure & Configuration

```
docker-compose.yml    → runs MongoDB on default port
.env                  → MONGO_URI, API_BASE_URL
uvicorn main:app      → FastAPI service (local)
python app.py         → Dash frontend (local)
```

**Startup sequence:**
1. `docker-compose up` — starts MongoDB
2. `uvicorn main:app --reload` — starts FastAPI service
3. `python app.py` — starts Dash frontend

**`.env` variables:**

| Variable       | Purpose                        |
|----------------|--------------------------------|
| `MONGO_URI`    | MongoDB connection string      |
| `API_BASE_URL` | Base URL for FastAPI service   |
