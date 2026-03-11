import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient

from src.config import MONGO_URI
from src.main import app
import src.repositories.prompts as prompts_repo
import src.repositories.templates as templates_repo

_test_client = MongoClient(MONGO_URI)
_test_db = _test_client["prompt_manager_test"]


@pytest.fixture(scope="session")
def client(monkeypatch_session):
    monkeypatch_session.setattr(prompts_repo, "_collection", _test_db["prompts"])
    monkeypatch_session.setattr(templates_repo, "_collection", _test_db["templates"])
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def monkeypatch_session():
    from _pytest.monkeypatch import MonkeyPatch
    mp = MonkeyPatch()
    yield mp
    mp.undo()


@pytest.fixture(autouse=True)
def clean_collections():
    _test_db["prompts"].drop()
    _test_db["templates"].drop()
    yield
    _test_db["prompts"].drop()
    _test_db["templates"].drop()
