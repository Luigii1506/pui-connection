import json

from fastapi.testclient import TestClient

from pui_adapter_service.config import get_settings
from pui_adapter_service.db.session import get_engine, get_session_factory
from pui_adapter_service.main import create_app


def test_login_rate_limit(monkeypatch, tmp_path):
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("DATABASE_URL", f"sqlite+pysqlite:///{tmp_path / 'rate-limit.db'}")
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret")
    monkeypatch.setenv("PUI_INBOUND_PASSWORD", "TestPassword123!")
    monkeypatch.setenv("SCHEDULER_ENABLED", "false")
    monkeypatch.setenv("CORE_BACKEND", "simulated")
    monkeypatch.setenv("LOGIN_RATE_LIMIT_REQUESTS", "2")
    monkeypatch.setenv("API_RATE_LIMIT_REQUESTS", "100")

    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    app = create_app()
    with TestClient(app) as client:
        for _ in range(2):
            response = client.post("/login", json={"usuario": "PUI", "clave": "TestPassword123!"})
            assert response.status_code == 200

        response = client.post("/login", json={"usuario": "PUI", "clave": "TestPassword123!"})
        assert response.status_code == 429
        assert response.json()["error"] == "Demasiadas solicitudes"


def test_request_id_is_preserved_and_logged(monkeypatch, tmp_path, caplog):
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("DATABASE_URL", f"sqlite+pysqlite:///{tmp_path / 'request-id.db'}")
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret")
    monkeypatch.setenv("PUI_INBOUND_PASSWORD", "TestPassword123!")
    monkeypatch.setenv("SCHEDULER_ENABLED", "false")
    monkeypatch.setenv("CORE_BACKEND", "simulated")

    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    app = create_app()
    with TestClient(app) as client:
        with caplog.at_level("INFO", logger="pui_adapter_service.http"):
            response = client.get("/health", headers={"X-Request-ID": "req-test-123"})

        assert response.status_code == 200
        assert response.headers["x-request-id"] == "req-test-123"
        payload = json.loads(caplog.records[-1].message)
        assert payload["request_id"] == "req-test-123"
        assert payload["path"] == "/health"
