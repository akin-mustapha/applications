from datetime import datetime, timezone

from pymongo import MongoClient
from pymongo.collection import ReturnDocument

from src.config import MONGO_URI
from src.models import Prompt

_client: MongoClient = MongoClient(MONGO_URI)
_collection = _client["prompt_manager"]["prompts"]


def create_prompt(data: Prompt) -> Prompt:
    """Insert a new prompt document and return it.

    Args:
        data: The Prompt instance to persist.

    Returns:
        The persisted Prompt instance.
    """
    _collection.insert_one(data.model_dump())
    return data


def get_prompt(id: str) -> Prompt | None:
    """Retrieve a single prompt by UUID.

    Args:
        id: The prompt UUID string.

    Returns:
        The matching Prompt, or None if not found.
    """
    doc = _collection.find_one({"id": id}, {"_id": 0})
    if doc is None:
        return None
    return Prompt(**doc)


def list_prompts(q: str = "", tags: list[str] | None = None) -> list[Prompt]:
    """List prompts with optional full-text search and tag filter.

    Args:
        q: Search string matched against name, description, and content.
        tags: Tag list for OR-filter; returns prompts matching any tag.

    Returns:
        List of matching Prompt instances.
    """
    mongo_filter: dict = {}

    if q:
        regex = {"$regex": q, "$options": "i"}
        mongo_filter["$or"] = [
            {"name": regex},
            {"description": regex},
            {"content": regex},
        ]

    if tags:
        mongo_filter["tags"] = {"$in": tags}

    docs = _collection.find(mongo_filter, {"_id": 0})
    return [Prompt(**doc) for doc in docs]


def update_prompt(id: str, data: dict) -> Prompt | None:
    """Update a prompt by UUID and return the updated document.

    Args:
        id: The prompt UUID string.
        data: Fields to update (partial update supported).

    Returns:
        The updated Prompt, or None if not found.
    """
    data["updated_datetime"] = datetime.now(timezone.utc)
    doc = _collection.find_one_and_update(
        {"id": id},
        {"$set": data},
        projection={"_id": 0},
        return_document=ReturnDocument.AFTER,
    )
    if doc is None:
        return None
    return Prompt(**doc)


def delete_prompt(id: str) -> bool:
    """Delete a prompt by UUID.

    Args:
        id: The prompt UUID string.

    Returns:
        True if the document was deleted, False if not found.
    """
    result = _collection.delete_one({"id": id})
    return result.deleted_count == 1
