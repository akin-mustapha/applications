from fastapi import FastAPI, HTTPException

from src.config import MONGO_URI
from src.models import Prompt, PromptCreate, PromptUpdate
from src.repositories import prompts as prompts_repo

app = FastAPI(title="Prompt Manager")


@app.on_event("startup")
def startup() -> None:
    """Create unique indexes on `id` for both collections at startup."""
    from pymongo import MongoClient

    client: MongoClient = MongoClient(MONGO_URI)
    db = client["prompt_manager"]
    db["prompts"].create_index("id", unique=True)
    db["templates"].create_index("id", unique=True)


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
