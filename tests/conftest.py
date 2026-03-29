from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from pui_adapter_service.config import get_settings
from pui_adapter_service.db.session import get_engine, get_session_factory
from pui_adapter_service.main import create_app


@pytest.fixture
def client(tmp_path, monkeypatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("DATABASE_URL", f"sqlite+pysqlite:///{tmp_path / 'test.db'}")
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret")
    monkeypatch.setenv("PUI_INBOUND_PASSWORD", "TestPassword123!")

    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    app = create_app()
    with TestClient(app) as test_client:
        yield test_client
