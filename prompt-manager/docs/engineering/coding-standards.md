---
name: Coding Standards
---

# Coding Standards

All Python code in this project follows PEP 8 with Ruff as the single tool for formatting and linting. These standards apply to everything in `src/` and `tests/`.

---

## Tooling

### Ruff

[Ruff](https://docs.astral.sh/ruff/) handles both formatting and linting. It replaces Black, isort, and Flake8.

**Format code:**

```bash
ruff format src/ tests/
```

**Lint code:**

```bash
ruff check src/ tests/
```

**Auto-fix lint issues:**

```bash
ruff check --fix src/ tests/
```

### Configuration

Project Ruff config lives in `.ruff.toml` at the root:

```toml
line-length = 88
target-version = "py310"

[lint]
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "I",   # isort
    "UP",  # pyupgrade
]
ignore = []

[lint.isort]
known-first-party = ["src"]
```

---

## Python Version

**Minimum: Python 3.10**

Use Python 3.10+ features freely: `match` statements, `X | Y` union types, `TypeAlias`.

---

## Naming Conventions

| Entity | Convention | Example |
|--------|------------|---------|
| Files / modules | `snake_case` | `models.py`, `prompts.py` |
| Classes | `PascalCase` | `Prompt`, `TemplateCreate` |
| Functions / methods | `snake_case` | `get_prompt()`, `list_templates()` |
| Variables | `snake_case` | `prompt_id`, `variable_values` |
| Constants | `UPPER_SNAKE_CASE` | `MONGO_URI`, `API_BASE_URL` |
| Private helpers | leading underscore | `_build_query()` |

---

## Type Hints

Type hints are **required** on all function signatures — parameters and return types.

```python
# Good
def get_prompt(prompt_id: str) -> Prompt | None:
    ...

# Bad — no hints
def get_prompt(prompt_id):
    ...
```

For `None` return types, annotate explicitly:

```python
def delete_prompt(prompt_id: str) -> None:
    ...
```

---

## Docstrings

Use **Google style** docstrings. Required on all public functions, methods, and classes. Not required on private helpers or trivial one-liners.

```python
def create_prompt(data: PromptCreate) -> Prompt:
    """Create a new prompt and persist it to MongoDB.

    Args:
        data: Validated prompt creation payload.

    Returns:
        The newly created Prompt with auto-generated id and timestamps.

    Raises:
        DuplicateKeyError: If a prompt with the same id already exists.
    """
    ...
```

Class docstrings go immediately after the `class` line:

```python
class Prompt(BaseModel):
    """A stored prompt with content, tags, and optional template linkage."""
    ...
```

---

## Import Ordering

Ruff (isort rules) enforces this automatically. Order is:

1. Standard library (`uuid`, `datetime`, `os`)
2. Third-party (`fastapi`, `pydantic`, `pymongo`)
3. Local (`src.models`, `src.config`)

Each group separated by a blank line. Do not manually sort — let `ruff check --fix` handle it.

---

## Code Style Rules

### Line length

Max **88 characters** (Ruff default, matches Black).

### Strings

Prefer double quotes `"` for all strings (Ruff formats this consistently).

### Blank lines

- 2 blank lines between top-level definitions (functions, classes)
- 1 blank line between methods inside a class

### No unused imports

Remove unused imports immediately. Ruff (`F401`) will flag them.

### No bare `except`

Always specify the exception type:

```python
# Good
try:
    ...
except ValueError as e:
    ...

# Bad
try:
    ...
except:
    ...
```

---

## FastAPI Conventions

- Route handlers in `src/main.py` — one handler per endpoint
- Request bodies typed with Pydantic models
- Return types annotated on all route handlers
- No business logic in route handlers — delegate to `repositories/`

```python
@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(data: PromptCreate) -> Prompt:
    """Create a new prompt."""
    return prompts_repo.create_prompt(data)
```

---

## Pydantic Conventions

- Use `BaseModel` for all data models
- Fields use `snake_case`
- Use `Field(default_factory=...)` for mutable defaults
- Auto-generate UUIDs and timestamps in validators, not in route handlers

```python
from uuid import uuid4
from datetime import datetime, UTC
from pydantic import BaseModel, Field

class Prompt(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    created_datetime: datetime = Field(default_factory=lambda: datetime.now(UTC))
```
