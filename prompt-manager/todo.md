# Prompt Manager — Implementation Plan

## Iteration 1 — Foundation & Data Layer

**Goal:** Runnable skeleton with data models and MongoDB access.

- [ ] `docker-compose.yml` — MongoDB container
- [ ] `.env` / `.env.example` — `MONGO_URI`, `API_BASE_URL`
- [ ] `src/config.py` — env var loading
- [ ] `src/models.py` — `Variable`, `Prompt`, `Template` Pydantic models (with UUID auto-gen, datetime auto-set)
- [ ] `src/repositories/prompts.py` — `create`, `get`, `list`, `update`, `delete`
- [ ] `src/repositories/templates.py` — `create`, `get`, `list`, `update`, `delete`
- [ ] `requirements.txt` / `requirements-dev.txt`
- [ ] Unit tests: `tests/unit/test_models.py`

---

## Iteration 2 — FastAPI Backend (Prompts + Templates CRUD)

**Goal:** All REST endpoints working and testable via curl.

- [ ] `src/main.py` — FastAPI app, startup index creation, all `/prompts` and `/templates` routes
- [ ] Full CRUD for both resources
- [ ] Search: `?q` (full-text), `?tags` (OR filter) on `/prompts`; `?q` on `/templates`
- [ ] Integration tests: `tests/integration/test_prompts.py` (includes export route tests), `tests/integration/test_templates.py`
- [ ] `tests/conftest.py` — shared fixtures (test MongoDB client, test app)

---

## Iteration 3 — Template Instantiation & Prompt Export

**Goal:** The two differentiating features working end-to-end.

- [ ] `POST /templates/{id}/instantiate` — variable substitution (`{{var}}` → value), returns new `Prompt`
- [ ] `GET /prompts/{id}/export?format=md|yaml|json` — route handler in `src/main.py` calls `_format_export()` helper; correct `Content-Type`, `Content-Disposition`, raw body
- [ ] `_format_export()` lives in `src/main.py` — pure serialization, no DB access
- [ ] Unit tests: `tests/unit/test_export.py` — covers `_format_export()` directly

---

## Iteration 4 — Dash Frontend

**Goal:** Functional UI connected to the API.

- [ ] `src/app.py` — three-pane layout (center editor + preview, bottom metadata, right sidebar)
- [ ] Right sidebar: prompt list, template list, search bar, "New Prompt" / "New Template" buttons
- [ ] Center: split markdown editor (left) + live preview (right)
- [ ] Bottom: name/description/tags fields, export controls
- [ ] Callbacks: create, load, update, delete prompts and templates
- [ ] All HTTP calls via `API_BASE_URL`

---

## Iteration 5 — Template Instantiation UI & Polish

**Goal:** Complete user flows, hardened, documented.

- [ ] Template variable input form in bottom pane (shown when creating from template)
- [ ] Variable descriptions displayed as field labels/hints
- [ ] Error handling in UI: reads `response["detail"]` and surfaces messages
- [ ] `docs/reference/troubleshooting.md` — common setup issues
- [ ] `docs/reference/api-examples.md` — curl examples for every endpoint
- [ ] `README.md` — quick start (`docker-compose up` → `uvicorn` → `python app.py`)
- [ ] Final smoke test of all 12 use cases from design.md §4
