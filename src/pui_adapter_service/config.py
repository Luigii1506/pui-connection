from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PUI Adapter Service"
    app_env: str = "local"
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

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
