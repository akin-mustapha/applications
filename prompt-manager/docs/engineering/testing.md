---
name: Testing
---

# Testing

Prompt Manager uses **pytest** with two test levels: unit tests for isolated logic and integration tests for FastAPI routes against a live MongoDB test database.

---

## Test Structure

```text
tests/
├── conftest.py          # Shared fixtures: test DB client, FastAPI TestClient
├── unit/
│   ├── test_models.py   # Pydantic model validation, UUID/timestamp generation
│   └── test_export.py   # Export formatting: md, yaml, json output correctness
└── integration/
    ├── test_prompts.py  # All /prompts route tests
    └── test_templates.py # All /templates route tests
```

---

## Running Tests

**All tests:**

```bash
pytest
```

**Unit tests only:**

```bash
pytest tests/unit/
```

**Integration tests only:**

```bash
pytest tests/integration/
```

**With output (no capture):**

```bash
pytest -s
```

**Verbose:**

```bash
pytest -v
```

---

## Unit Tests

Unit tests cover logic that can be tested without a database or HTTP layer.

### `tests/unit/test_models.py`

| Test | What it checks |
|------|----------------|
| `test_prompt_uuid_auto_generated` | `id` is a valid UUID string when not provided |
| `test_prompt_timestamps_auto_set` | `created_datetime` and `updated_datetime` are set on creation |
| `test_prompt_name_required` | Creating a `Prompt` without `name` raises `ValidationError` |
| `test_prompt_content_required` | Creating a `Prompt` without `content` raises `ValidationError` |
| `test_template_variable_name_required` | `Variable` without `name` raises `ValidationError` |
| `test_template_variable_description_required` | `Variable` without `description` raises `ValidationError` |

### `tests/unit/test_export.py`

| Test | What it checks |
|------|----------------|
| `test_export_md` | Exported `.md` content matches prompt `content` field |
| `test_export_yaml` | Exported `.yaml` is valid YAML containing all prompt fields |
| `test_export_json` | Exported `.json` is valid JSON with correct field values |
| `test_export_filename_md` | Filename is `{prompt_name}.md` |
| `test_export_filename_yaml` | Filename is `{prompt_name}.yaml` |
| `test_export_filename_json` | Filename is `{prompt_name}.json` |
| `test_export_invalid_format` | Raises error or returns 422 for unknown format |

---

## Integration Tests

Integration tests call FastAPI endpoints using `httpx.TestClient`. They run against a **separate test MongoDB database** (`prompt_manager_test`) — never against the production database.

### MongoDB Test Database

- Database name: `prompt_manager_test`
- Same `docker-compose.yml` MongoDB instance — no separate container needed
- Each test cleans up its own data via pytest fixtures (see `conftest.py`)

### `tests/conftest.py`

Key fixtures:

```python
import pytest
from httpx import TestClient
from src.main import app

@pytest.fixture(scope="session")
def client():
    """FastAPI test client connected to test DB."""
    # Override MONGO_DB_NAME to point at test DB
    with TestClient(app) as c:
        yield c

@pytest.fixture(autouse=True)
def clean_db():
    """Drop test collections before each test."""
    # Clear prompts and templates collections
    yield
    # Teardown: clear again after test
```

### `tests/integration/test_prompts.py`

| Test | Endpoint | What it checks |
|------|----------|----------------|
| `test_create_prompt` | `POST /prompts` | Returns 201, response has `id`, `name`, timestamps |
| `test_create_prompt_missing_name` | `POST /prompts` | Returns 422 |
| `test_get_prompt` | `GET /prompts/{id}` | Returns 200 with correct data |
| `test_get_prompt_not_found` | `GET /prompts/{id}` | Returns 404 |
| `test_list_prompts` | `GET /prompts` | Returns list of all prompts |
| `test_search_prompts_by_name` | `GET /prompts?q=foo` | Returns only matching prompts |
| `test_search_prompts_by_content` | `GET /prompts?q=foo` | Matches on content field |
| `test_filter_prompts_by_tags` | `GET /prompts?tags=gpt` | Returns prompts with matching tag |
| `test_filter_prompts_by_multiple_tags` | `GET /prompts?tags=gpt,creative` | OR logic — any tag matches |
| `test_update_prompt` | `PUT /prompts/{id}` | Returns 200, fields updated |
| `test_update_prompt_not_found` | `PUT /prompts/{id}` | Returns 404 |
| `test_delete_prompt` | `DELETE /prompts/{id}` | Returns 204, prompt gone |
| `test_delete_prompt_not_found` | `DELETE /prompts/{id}` | Returns 404 |
| `test_export_prompt_md` | `GET /prompts/{id}/export?format=md` | Content-Type: text/markdown |
| `test_export_prompt_yaml` | `GET /prompts/{id}/export?format=yaml` | Content-Type: application/x-yaml |
| `test_export_prompt_json` | `GET /prompts/{id}/export?format=json` | Content-Type: application/json |
| `test_export_content_disposition` | `GET /prompts/{id}/export?format=md` | Filename header is `{name}.md` |

### `tests/integration/test_templates.py`

| Test | Endpoint | What it checks |
|------|----------|----------------|
| `test_create_template` | `POST /templates` | Returns 201, has `id`, `variables` |
| `test_create_template_missing_name` | `POST /templates` | Returns 422 |
| `test_get_template` | `GET /templates/{id}` | Returns 200 with correct data |
| `test_get_template_not_found` | `GET /templates/{id}` | Returns 404 |
| `test_list_templates` | `GET /templates` | Returns list |
| `test_search_templates` | `GET /templates?q=foo` | Matches name and description |
| `test_update_template` | `PUT /templates/{id}` | Returns 200, fields updated |
| `test_delete_template` | `DELETE /templates/{id}` | Returns 204 |
| `test_instantiate_template` | `POST /templates/{id}/instantiate` | Returns Prompt with placeholders replaced |
| `test_instantiate_missing_variable` | `POST /templates/{id}/instantiate` | Returns 422 if required variable missing |
| `test_instantiate_extra_variable` | `POST /templates/{id}/instantiate` | Extra keys ignored or returns 422 |

---

## Dev Dependencies

Add to `requirements-dev.txt`:

```text
pytest
httpx
pytest-asyncio  # if async routes are used
```

---

## Notes

- No mocking of MongoDB — integration tests use a real (test) database for accuracy
- Tests are independent — each test creates its own data and does not depend on other tests running first
- The `autouse=True` fixture in `conftest.py` ensures collections are cleared between tests automatically
