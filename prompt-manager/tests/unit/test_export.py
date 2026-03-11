import json

import yaml

from src.main import _format_export
from src.models import Prompt


def _make_prompt(**kwargs) -> Prompt:
    defaults = {"name": "My Prompt", "content": "Hello world"}
    defaults.update(kwargs)
    return Prompt(**defaults)


def test_export_md():
    prompt = _make_prompt(content="# Title\n\nBody text.")
    content, _, _ = _format_export(prompt, "md")
    assert content == "# Title\n\nBody text."


def test_export_yaml():
    prompt = _make_prompt(name="Test", content="body")
    content, _, _ = _format_export(prompt, "yaml")
    data = yaml.safe_load(content)
    assert data["name"] == "Test"
    assert data["content"] == "body"
    assert "id" in data


def test_export_json():
    prompt = _make_prompt(name="Test", content="body")
    content, _, _ = _format_export(prompt, "json")
    data = json.loads(content)
    assert data["name"] == "Test"
    assert data["content"] == "body"
    assert "id" in data


def test_export_filename_md():
    prompt = _make_prompt(name="My Prompt")
    _, _, filename = _format_export(prompt, "md")
    assert filename == "My_Prompt.md"


def test_export_filename_yaml():
    prompt = _make_prompt(name="My Prompt")
    _, _, filename = _format_export(prompt, "yaml")
    assert filename == "My_Prompt.yaml"


def test_export_filename_json():
    prompt = _make_prompt(name="My Prompt")
    _, _, filename = _format_export(prompt, "json")
    assert filename == "My_Prompt.json"


def test_export_invalid_format(client):
    resp = client.get("/prompts/any-id/export?format=csv")
    assert resp.status_code == 422
