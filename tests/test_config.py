import pytest

from pui_adapter_service.config import Settings


def test_local_settings_allow_default_values():
    settings = Settings(
        app_env="local",
        jwt_secret_key="change-me-in-production",
        pui_inbound_password="ChangeMePassword1!",
    )
    settings.validate_runtime()


def test_sandbox_requires_public_url_and_non_default_secrets():
    settings = Settings(
        app_env="sandbox",
        public_base_url=None,
        jwt_secret_key="change-me-in-production",
        pui_inbound_password="ChangeMePassword1!",
    )

    with pytest.raises(RuntimeError) as exc:
        settings.validate_runtime()

    message = str(exc.value)
    assert "PUBLIC_BASE_URL es obligatorio" in message
    assert "JWT_SECRET_KEY" in message
    assert "PUI_INBOUND_PASSWORD" in message


def test_production_rejects_sqlite_and_default_outbound_values():
    settings = Settings(
        app_env="production",
        public_base_url="https://pui.empresa.com",
        database_url="sqlite+pysqlite:///./pui_adapter.db",
        jwt_secret_key="prod-secret",
        pui_inbound_password="ProdPassword123!",
        pui_outbound_enabled=True,
        pui_outbound_institucion_id="RFC123456ABC",
        pui_outbound_clave="ChangeMePassword1!",
    )

    with pytest.raises(RuntimeError) as exc:
        settings.validate_runtime()

    message = str(exc.value)
    assert "DATABASE_URL no debe usar SQLite en production" in message
    assert "PUI_OUTBOUND_INSTITUCION_ID" in message
    assert "PUI_OUTBOUND_CLAVE" in message
