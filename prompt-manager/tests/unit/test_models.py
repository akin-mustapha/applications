import pytest
from pydantic import ValidationError

from src.models import Prompt, Template, Variable


def test_prompt_uuid_auto_generated():
    prompt = Prompt(name="Test", content="body")
    assert isinstance(prompt.id, str)
    assert len(prompt.id) == 36  # UUID4 string length


def test_prompt_timestamps_auto_set():
    prompt = Prompt(name="Test", content="body")
    assert prompt.created_datetime is not None
    assert prompt.updated_datetime is not None
    assert prompt.created_datetime.tzinfo is not None


def test_prompt_name_required():
    with pytest.raises(ValidationError):
        Prompt(content="body")


def test_prompt_content_required():
    with pytest.raises(ValidationError):
        Prompt(name="Test")


def test_template_variable_name_required():
    with pytest.raises(ValidationError):
        Variable(description="x")


def test_template_variable_description_required():
    with pytest.raises(ValidationError):
        Variable(name="role")


def test_prompt_defaults():
    prompt = Prompt(name="Test", content="body")
    assert prompt.description == ""
    assert prompt.tags == []
    assert prompt.template_id is None
    assert prompt.variable_values == {}


def test_template_uuid_auto_generated():
    template = Template(name="T", content="Hello {{name}}")
    assert isinstance(template.id, str)
    assert len(template.id) == 36


def test_template_variables_default_empty():
    template = Template(name="T", content="body")
    assert template.variables == []
