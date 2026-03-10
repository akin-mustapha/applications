---
name: Development Setup
---

# Development Setup

Complete guide to setting up Prompt Manager locally from scratch.

---

## Prerequisites

| Tool | Version | Notes |
|------|---------|-------|
| Python | 3.10+ | Required |
| Docker | Any recent | For MongoDB |
| Docker Compose | v2+ | Bundled with Docker Desktop |

---

## Step-by-Step Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd prompt-manager
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

You should see `(.venv)` in your terminal prompt.

### 3. Install dependencies

**Production dependencies:**

```bash
pip install -r requirements.txt
```

**Development and test dependencies:**

```bash
pip install -r requirements-dev.txt
```

### 4. Configure environment variables

Copy the example env file:

```bash
cp .env.example .env
```

Edit `.env` and set:

```env
MONGO_URI=mongodb://localhost:27017
API_BASE_URL=http://localhost:8000
```

These are the correct values for local development. Do not commit `.env`.

### 5. Start MongoDB

```bash
docker-compose up -d
```

This starts MongoDB on port `27017`. Verify it's running:

```bash
docker-compose ps
```

### 6. Start the FastAPI service

```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`.

Auto-reload is enabled — the server restarts automatically when you change files in `src/`.

### 7. Start the Dash frontend

Open a second terminal (keep the API running in the first):

```bash
source .venv/bin/activate
python src/app.py
```

The UI will be available at `http://localhost:8050`.

---

## Startup Order

Always start in this order:

1. MongoDB (docker-compose)
2. FastAPI service (uvicorn)
3. Dash frontend (python)

If the API isn't running when the frontend starts, callbacks will fail silently.

---

## Verify the Setup

1. Open `http://localhost:8050` — Dash UI should load
2. Open `http://localhost:8000/docs` — FastAPI Swagger UI should show all endpoints
3. Create a prompt via the UI — it should appear in the sidebar list

---

## Code Quality Tools

### Ruff (formatter + linter)

Ruff is included in `requirements-dev.txt`.

**Format code:**

```bash
ruff format src/ tests/
```

**Lint code:**

```bash
ruff check src/ tests/
```

**Fix auto-fixable issues:**

```bash
ruff check --fix src/ tests/
```

**Recommended:** Install the [Ruff VS Code extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) for inline feedback while editing.

---

## Running Tests

Make sure MongoDB is running and your virtual environment is active.

**All tests:**

```bash
pytest
```

**Unit tests only (no DB required):**

```bash
pytest tests/unit/
```

**Integration tests (requires MongoDB):**

```bash
pytest tests/integration/
```

See [testing.md](testing.md) for full details on test scope and structure.
---

## Stopping Services

**Stop the FastAPI server:** `Ctrl+C` in its terminal

**Stop the Dash app:** `Ctrl+C` in its terminal

**Stop MongoDB:**

```bash
docker-compose down
```

To also remove the MongoDB data volume (full reset):

```bash
docker-compose down -v
```

---

## Common Issues

See [troubleshooting.md](../reference/troubleshooting.md) for solutions to common setup problems.

---

## Dependency Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Production runtime dependencies (FastAPI, Dash, pymongo, etc.) |
| `requirements-dev.txt` | Dev-only tools (pytest, httpx, ruff) |
| `.env.example` | Template showing all required environment variables |
| `.ruff.toml` | Ruff formatter and linter configuration |
