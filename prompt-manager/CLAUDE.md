# CLAUDE.MD

**ROLE:** YOU ARE TO ACT AS AN IMPLEMENTER, NOT A DECISION MAKER.

## IMPORTANT

- DO NOT MAKE ANY CHANGE TO THE CODE BASE UNLESS TOLD SO.
- YOU ARE NOT TO MAKE ANY ARCHITECTURAL DECISIONS, WHEN REQUIRED CONFIRM FROM HUMAN

---

## Project Overview

**Prompt Manager** is a local, single-user web app for an AI Engineer to create, find, and reuse prompt markdown files and templates.

---

## Business Requirements

- Single user, local only — no auth, no cloud, no caching
- Find any prompt in under 10 seconds via search
- Create reusable templates with `{{variable}}` placeholders
- Export prompts to `.md`, `.yaml`, `.json`
- Docker required for MongoDB; all other dependencies are local

> See [`docs/product/business-requirements.md`](docs/product/business-requirements.md)

---

## Product Requirements

Two core entities: **Prompts** and **Templates**.

- **Prompts** — CRUD, markdown editor + live preview, tagging, full-text search, create-from-template, export
- **Templates** — CRUD, `{{variable_name}}` placeholders, per-variable descriptions, search

UI is a three-pane layout: center split editor, bottom metadata/export pane, right sidebar for navigation and search.

> See [`docs/product/product-requirements.md`](docs/product/product-requirements.md)

---

## Architecture & Tech Stack

| Layer    | Technology    | Notes                                      |
|----------|---------------|--------------------------------------------|
| Frontend | Dash (Python) | Single-page app, no routing                |
| Backend  | FastAPI       | REST API, no auth, no cache, via Uvicorn   |
| Database | MongoDB       | Docker-hosted, `prompts` + `templates`     |
| Config   | `.env`        | Mongo URI, API base URL                    |

Startup: `docker-compose up` → `uvicorn main:app --reload` → `python app.py`

> See [`docs/architecture/architecture.md`](docs/architecture/architecture.md)

---

## Docs

- [`docs/requirements.md`](docs/requirements.md) — index
- [`docs/product/business-requirements.md`](docs/product/business-requirements.md)
- [`docs/product/product-requirements.md`](docs/product/product-requirements.md)
- [`docs/architecture/architecture.md`](docs/architecture/architecture.md)
- [`docs/architecture/design.md`](docs/architecture/design.md) — consolidated technical design reference
- [`docs/engineering/project-structure.md`](docs/engineering/project-structure.md)
- [`docs/engineering/coding-standards.md`](docs/engineering/coding-standards.md)
- [`docs/engineering/dev-setup.md`](docs/engineering/dev-setup.md)
- [`docs/engineering/testing.md`](docs/engineering/testing.md)
- [`docs/reference/api-examples.md`](docs/reference/api-examples.md)
- [`docs/reference/troubleshooting.md`](docs/reference/troubleshooting.md)
- [`docs/doc-skills.md`](docs/doc-skills.md) — skills overview

## Skills

- `/pm` — scope & task breakdown
- `/architect` — design & API decisions (always confirms with human)
- `/build` — feature implementation
- `/bug-hunter` — structured debugging, logs to `docs/bugs.md`
- `/doc-refresh` — detect and fix doc drift after any architectural or API change
