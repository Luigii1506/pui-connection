from contextlib import asynccontextmanager

from fastapi import FastAPI

from pui_adapter_service.api.routes import router
from pui_adapter_service.config import get_settings
from pui_adapter_service.db.session import init_db
from pui_adapter_service.scheduler import create_phase3_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    init_db()
    scheduler = None
    if settings.scheduler_enabled and settings.app_env != "test":
        scheduler, _ = create_phase3_scheduler(settings)
        scheduler.start()
        app.state.phase_3_scheduler = scheduler
    yield
    if scheduler is not None:
        scheduler.shutdown(wait=False)


def create_app() -> FastAPI:
    settings = get_settings()
    settings.validate_runtime()
    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    app.include_router(router)
    return app


app = create_app()
