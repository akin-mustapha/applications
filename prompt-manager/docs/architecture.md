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

| Method   | Endpoint                      | Description                              |
|----------|-------------------------------|------------------------------------------|
| `GET`    | `/prompts`                    | List all prompts (supports search)       |
| `POST`   | `/prompts`                    | Create a new prompt                      |
| `GET`    | `/prompts/{id}`               | Get a single prompt                      |
| `PUT`    | `/prompts/{id}`               | Update a prompt                          |
| `DELETE` | `/prompts/{id}`               | Delete a prompt                          |
| `POST`   | `/prompts/from-template/{id}` | Instantiate prompt from template         |
| `GET`    | `/prompts/{id}/export`        | Export prompt (`?format=md\|yaml\|json`) |

### Template Endpoints

| Method   | Endpoint          | Description                          |
|----------|-------------------|--------------------------------------|
| `GET`    | `/templates`      | List all templates (supports search) |
| `POST`   | `/templates`      | Create a new template                |
| `GET`    | `/templates/{id}` | Get a single template                |
| `PUT`    | `/templates/{id}` | Update a template                    |
| `DELETE` | `/templates/{id}` | Delete a template                    |

## Storage

- **Database:** MongoDB
- **Deployment:** Docker (docker-compose)
- **Collections:** `prompts`, `templates`

## Infrastructure

- `docker-compose.yml` runs MongoDB
- FastAPI runs locally via Uvicorn (`uvicorn main:app --reload`)
- Dash app runs locally (`python app.py`)
- `.env` file for config (Mongo connection string, API base URL)
