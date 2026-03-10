---
name: Project Structure
---

# Project Structure

This document describes the intended folder and file layout for Prompt Manager. All code lives in `src/` with a flat structure — no nested packages beyond the `repositories/` sub-module.

---

## Directory Layout

```text
prompt-manager/
├── src/
│   ├── main.py              # FastAPI app — entry point for the backend service
│   ├── app.py               # Dash app — entry point for the frontend
│   ├── models.py            # Pydantic models: Prompt, Template, Variable
│   ├── config.py            # Env var loading via python-dotenv
│   └── repositories/
│       ├── __init__.py
│       ├── prompts.py       # MongoDB CRUD operations for prompts
│       └── templates.py     # MongoDB CRUD operations for templates
├── tests/
│   ├── conftest.py          # Shared pytest fixtures (DB client, test app)
│   ├── unit/
│   │   ├── test_models.py   # Pydantic model validation, UUID generation
│   │   └── test_export.py   # Export formatting logic (md, yaml, json)
│   └── integration/
│       ├── test_prompts.py  # FastAPI route tests for /prompts
│       └── test_templates.py # FastAPI route tests for /templates
├── docs/                    # All project documentation
├── docker-compose.yml       # MongoDB container definition
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Dev/test-only dependencies
├── .env                     # Local config — gitignored, never committed
├── .env.example             # Template showing required env vars
├── .ruff.toml               # Ruff formatter and linter config
├── README.md                # Project overview and quick start
└── CLAUDE.md                # AI agent instructions and context
```

---

## File Responsibilities

### `src/main.py`

FastAPI application factory and route registration. Includes:

- App instantiation (`FastAPI()`)
- MongoDB connection and index creation on startup
- Route handlers for `/prompts` and `/templates`
- No business logic — delegates to `repositories/`

### `src/app.py`

Dash single-page application. Includes:

- Layout definition (three-pane: editor, bottom pane, right sidebar)
- Dash callbacks for user interactions
- HTTP calls to the FastAPI service via `API_BASE_URL`

### `src/models.py`

All Pydantic models shared across the app:

- `Variable` — nested in Template
- `Prompt` — full prompt document
- `Template` — full template document
- Request/response variants (create, update) as needed

### `src/config.py`

Loads environment variables from `.env` using `python-dotenv`. Exposes:

- `MONGO_URI` — MongoDB connection string
- `API_BASE_URL` — Base URL for FastAPI (used by Dash frontend)

### `src/repositories/prompts.py`

All MongoDB operations for the `prompts` collection:

- `create_prompt()`
- `get_prompt(id)`
- `list_prompts(q, tags)`
- `update_prompt(id, data)`
- `delete_prompt(id)`
- `export_prompt(id, format)`

### `src/repositories/templates.py`

All MongoDB operations for the `templates` collection:

- `create_template()`
- `get_template(id)`
- `list_templates(q)`
- `update_template(id, data)`
- `delete_template(id)`
- `instantiate_template(template_id, variable_values)`

---

## Naming Conventions

| Entity | Convention | Example |
|--------|------------|---------|
| Files / modules | `snake_case` | `models.py`, `prompts.py` |
| Classes | `PascalCase` | `Prompt`, `TemplateCreate` |
| Functions | `snake_case` | `get_prompt()`, `list_templates()` |
| Variables | `snake_case` | `prompt_id`, `variable_values` |
| Constants | `UPPER_SNAKE_CASE` | `MONGO_URI`, `API_BASE_URL` |

---

## What Goes Where

| Type of code | Location |
|---|---|
| FastAPI routes and app setup | `src/main.py` |
| Dash layout and callbacks | `src/app.py` |
| Data models (Pydantic) | `src/models.py` |
| Config / env loading | `src/config.py` |
| Database access (MongoDB) | `src/repositories/` |
| Unit tests | `tests/unit/` |
| Integration tests | `tests/integration/` |
| Shared test fixtures | `tests/conftest.py` |
| Documentation | `docs/` |
