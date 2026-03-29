from contextlib import asynccontextmanager

from fastapi import FastAPI

from pui_adapter_service.api.routes import router
from pui_adapter_service.config import get_settings
from pui_adapter_service.db.session import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    app.include_router(router)
    return app


app = create_app()
