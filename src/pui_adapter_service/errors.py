from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def _request_id_payload(request: Request) -> dict:
    request_id = getattr(request.state, "request_id", None)
    return {"request_id": request_id} if request_id else {}


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        detail = exc.detail
        if isinstance(detail, list):
            return JSONResponse(
                status_code=exc.status_code,
                content={"errors": detail, **_request_id_payload(request)},
            )
        if isinstance(detail, dict):
            return JSONResponse(
                status_code=exc.status_code,
                content={**detail, **_request_id_payload(request)},
            )
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": str(detail), **_request_id_payload(request)},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        errors = []
        for error in exc.errors():
            location = ".".join(str(item) for item in error["loc"] if item != "body")
            prefix = f"{location}: " if location else ""
            errors.append(f"{prefix}{error['msg']}")
        return JSONResponse(
            status_code=422,
            content={"errors": errors, **_request_id_payload(request)},
        )

    @app.exception_handler(Exception)
    async def unexpected_exception_handler(request: Request, __: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"error": "Error interno del servidor", **_request_id_payload(request)},
        )
