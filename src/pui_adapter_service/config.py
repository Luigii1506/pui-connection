from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PUI Adapter Service"
    app_env: str = "local"
    public_base_url: str | None = None
    database_url: str = "sqlite+pysqlite:///./pui_adapter.db"
    core_backend: str = "simulated"
    core_simulation_file: str | None = None
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    pui_inbound_user: str = "PUI"
    pui_inbound_password: str = "ChangeMePassword1!"
    pui_outbound_base_url: str = "https://plataformadebusqueda.gob.mx/api/2_3_0"
    pui_outbound_institucion_id: str = "RFC123456ABC"
    pui_outbound_clave: str = "ChangeMePassword1!"
    pui_outbound_enabled: bool = False
    pui_request_timeout_seconds: int = 10
    scheduler_enabled: bool = True
    scheduler_phase3_minutes: int = 60
    rate_limit_window_seconds: int = 60
    login_rate_limit_requests: int = 5
    api_rate_limit_requests: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    def validate_runtime(self) -> None:
        errors: list[str] = []
        real_env = self.app_env in {"sandbox", "production"}
        default_inbound_password = "ChangeMePassword1!"
        default_jwt_secret = "change-me-in-production"
        default_outbound_institucion = "RFC123456ABC"
        default_outbound_clave = "ChangeMePassword1!"

        if real_env:
            if not self.public_base_url:
                errors.append("PUBLIC_BASE_URL es obligatorio en sandbox/production")
            elif not self.public_base_url.startswith("https://"):
                errors.append("PUBLIC_BASE_URL debe usar HTTPS en sandbox/production")

            if self.pui_inbound_password == default_inbound_password:
                errors.append("PUI_INBOUND_PASSWORD no puede quedarse con el valor por defecto en sandbox/production")

            if self.jwt_secret_key == default_jwt_secret:
                errors.append("JWT_SECRET_KEY no puede quedarse con el valor por defecto en sandbox/production")

        if self.pui_outbound_enabled:
            if not self.pui_outbound_base_url.startswith("https://"):
                errors.append("PUI_OUTBOUND_BASE_URL debe usar HTTPS cuando PUI_OUTBOUND_ENABLED=true")

            if self.pui_outbound_institucion_id == default_outbound_institucion:
                errors.append("PUI_OUTBOUND_INSTITUCION_ID debe ser el RFC real de la empresa")

            if self.pui_outbound_clave == default_outbound_clave:
                errors.append("PUI_OUTBOUND_CLAVE no puede quedarse con el valor por defecto")

        if self.app_env == "production" and self.database_url.startswith("sqlite"):
            errors.append("DATABASE_URL no debe usar SQLite en production")

        if errors:
            raise RuntimeError("Configuracion invalida:\n- " + "\n- ".join(errors))


@lru_cache
def get_settings() -> Settings:
    return Settings()
