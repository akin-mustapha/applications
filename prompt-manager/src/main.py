from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from src.config import MONGO_URI
from src.models import (
    Prompt,
    PromptCreate,
    PromptUpdate,
    Template,
    TemplateCreate,
    TemplateUpdate,
)
from src.repositories import prompts as prompts_repo
from src.repositories import templates as templates_repo

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create unique indexes on `id` for both collections at startup."""
    from pymongo import MongoClient

    client: MongoClient = MongoClient(MONGO_URI)
    db = client["prompt_manager"]
    db["prompts"].create_index("id", unique=True)
    db["templates"].create_index("id", unique=True)
    yield


app = FastAPI(title="Prompt Manager", lifespan=lifespan)


@app.get("/prompts", response_model=list[Prompt])
def list_prompts(q: str = "", tags: str = "") -> list[Prompt]:
    """List all prompts with optional full-text search and tag filter.

    Args:
        q: Full-text search string matched against name, description, content.
        tags: Comma-separated tag filter (OR logic), e.g. ``gpt,creative``.

    Returns:
        List of matching Prompt instances.
    """
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else None
    return prompts_repo.list_prompts(q=q, tags=tag_list)


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(data: PromptCreate) -> Prompt:
    """Create a new prompt.

    Args:
        data: Validated prompt creation payload.

    Returns:
        The newly created Prompt with auto-generated id and timestamps.
    """
    prompt = Prompt(**data.model_dump())
    return prompts_repo.create_prompt(prompt)


@app.get("/prompts/{id}", response_model=Prompt)
def get_prompt(id: str) -> Prompt:
    """Retrieve a single prompt by UUID.

    Args:
        id: The prompt UUID string.

    Returns:
        The matching Prompt.

    Raises:
        HTTPException: 404 if the prompt is not found.
    """
    prompt = prompts_repo.get_prompt(id)
    if prompt is None:
        raise HTTPException(status_code=404, detail="Not found")
    return prompt


@app.put("/prompts/{id}", response_model=Prompt)
def update_prompt(id: str, data: PromptUpdate) -> Prompt:
    """Partially update a prompt by UUID.

    Args:
        id: The prompt UUID string.
        data: Fields to update — omitted fields are left unchanged.

    Returns:
        The updated Prompt.

    Raises:
        HTTPException: 404 if the prompt is not found.
    """
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    prompt = prompts_repo.update_prompt(id, update_data)
    if prompt is None:
        raise HTTPException(status_code=404, detail="Not found")
    return prompt


@app.delete("/prompts/{id}")
def delete_prompt(id: str) -> dict[str, bool]:
    """Delete a prompt by UUID.

    Args:
        id: The prompt UUID string.

    Returns:
        ``{"deleted": true}`` on success.

    Raises:
        HTTPException: 404 if the prompt is not found.
    """
    deleted = prompts_repo.delete_prompt(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Not found")
    return {"deleted": True}


@app.get("/templates", response_model=list[Template])
def list_templates(q: str = "") -> list[Template]:
    """List all templates with optional search across name and description.

    Args:
        q: Search string matched against name and description.

    Returns:
        List of matching Template instances.
    """
    return templates_repo.list_templates(q=q)


@app.post("/templates", response_model=Template, status_code=201)
def create_template(data: TemplateCreate) -> Template:
    """Create a new template.

    Args:
        data: Validated template creation payload.

    Returns:
        The newly created Template with auto-generated id and timestamps.
    """
    template = Template(**data.model_dump())
    return templates_repo.create_template(template)


@app.get("/templates/{id}", response_model=Template)
def get_template(id: str) -> Template:
    """Retrieve a single template by UUID.

    Args:
        id: The template UUID string.

    Returns:
        The matching Template.

    Raises:
        HTTPException: 404 if the template is not found.
    """
    template = templates_repo.get_template(id)
    if template is None:
        raise HTTPException(status_code=404, detail="Not found")
    return template


@app.put("/templates/{id}", response_model=Template)
def update_template(id: str, data: TemplateUpdate) -> Template:
    """Partially update a template by UUID.

    Args:
        id: The template UUID string.
        data: Fields to update — omitted fields are left unchanged.

    Returns:
        The updated Template.

    Raises:
        HTTPException: 404 if the template is not found.
    """
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    template = templates_repo.update_template(id, update_data)
    if template is None:
        raise HTTPException(status_code=404, detail="Not found")
    return template


@app.delete("/templates/{id}")
def delete_template(id: str) -> dict[str, bool]:
    """Delete a template by UUID.

    Args:
        id: The template UUID string.

    Returns:
        ``{"deleted": true}`` on success.

    Raises:
        HTTPException: 404 if the template is not found.
    """
    deleted = templates_repo.delete_template(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Not found")
    return {"deleted": True}
