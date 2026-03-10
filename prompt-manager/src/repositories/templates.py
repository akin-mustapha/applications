from datetime import datetime, timezone

from pymongo import MongoClient
from pymongo.collection import ReturnDocument

from src.config import MONGO_URI
from src.models import Template

_client: MongoClient = MongoClient(MONGO_URI)
_collection = _client["prompt_manager"]["templates"]


def create_template(data: Template) -> Template:
    """Insert a new template document and return it.

    Args:
        data: The Template instance to persist.

    Returns:
        The persisted Template instance.
    """
    _collection.insert_one(data.model_dump())
    return data


def get_template(id: str) -> Template | None:
    """Retrieve a single template by UUID.

    Args:
        id: The template UUID string.

    Returns:
        The matching Template, or None if not found.
    """
    doc = _collection.find_one({"id": id}, {"_id": 0})
    if doc is None:
        return None
    return Template(**doc)


def list_templates(q: str = "") -> list[Template]:
    """List templates with optional search across name and description.

    Args:
        q: Search string matched against name and description.

    Returns:
        List of matching Template instances.
    """
    mongo_filter: dict = {}

    if q:
        regex = {"$regex": q, "$options": "i"}
        mongo_filter["$or"] = [
            {"name": regex},
            {"description": regex},
        ]

    docs = _collection.find(mongo_filter, {"_id": 0})
    return [Template(**doc) for doc in docs]


def update_template(id: str, data: dict) -> Template | None:
    """Update a template by UUID and return the updated document.

    Args:
        id: The template UUID string.
        data: Fields to update (partial update supported).

    Returns:
        The updated Template, or None if not found.
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
    return Template(**doc)


def delete_template(id: str) -> bool:
    """Delete a template by UUID.

    Args:
        id: The template UUID string.

    Returns:
        True if the document was deleted, False if not found.
    """
    result = _collection.delete_one({"id": id})
    return result.deleted_count == 1
