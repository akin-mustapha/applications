from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field


class Variable(BaseModel):
    """A placeholder variable definition within a template."""

    name: str
    description: str


class Prompt(BaseModel):
    """A stored prompt with content, tags, and optional template linkage."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: str = ""
    content: str
    tags: list[str] = Field(default_factory=list)
    template_id: str | None = None
    variable_values: dict[str, str] = Field(default_factory=dict)
    created_datetime: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_datetime: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class PromptCreate(BaseModel):
    """Request body for creating a new prompt."""

    name: str
    content: str
    description: str = ""
    tags: list[str] = Field(default_factory=list)
    template_id: str | None = None
    variable_values: dict[str, str] = Field(default_factory=dict)


class PromptUpdate(BaseModel):
    """Request body for partially updating a prompt."""

    name: str | None = None
    content: str | None = None
    description: str | None = None
    tags: list[str] | None = None
    template_id: str | None = None
    variable_values: dict[str, str] | None = None


class Template(BaseModel):
    """A prompt template with variable placeholders."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: str = ""
    content: str
    variables: list[Variable] = Field(default_factory=list)
    created_datetime: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_datetime: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class TemplateCreate(BaseModel):
    """Request body for creating a new template."""

    name: str
    content: str
    description: str = ""
    variables: list[Variable] = Field(default_factory=list)


class TemplateUpdate(BaseModel):
    """Request body for partially updating a template."""

    name: str | None = None
    content: str | None = None
    description: str | None = None
    variables: list[Variable] | None = None


class InstantiateRequest(BaseModel):
    """Request body for instantiating a prompt from a template."""

    variable_values: dict[str, str] = Field(default_factory=dict)
