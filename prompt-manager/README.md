# Prompt Manager

A local web app for AI engineers to create, search, and reuse prompt files and templates.

## What it does

- Create, edit, and delete prompts with a live markdown editor and preview
- Search prompts instantly by name, description, or content
- Build reusable templates with `{{variable}}` placeholders and guided input
- Export any prompt to `.md`, `.yaml`, or `.json`
- Tag prompts freely for easy browsing and filtering

## Tech Stack

| Layer    | Tool           |
|----------|----------------|
| Frontend | Dash (Python)  |
| Backend  | FastAPI        |
| Database | MongoDB (Docker) |

## Getting Started

**Prerequisites:** Docker, Python 3.10+

```bash
# 1. Start MongoDB
docker-compose up -d

# 2. Start the API
uvicorn main:app --reload

# 3. Start the UI
python app.py
```

Open `http://localhost:8050` in your browser.

## Configuration

Copy `.env.example` to `.env` and set:

```
MONGO_URI=mongodb://localhost:27017
API_BASE_URL=http://localhost:8000
```

## Docs

See [`docs/`](docs/) for full requirements and architecture details.
