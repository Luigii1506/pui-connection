import json
import logging
from collections import deque
from collections.abc import Callable
from time import time
from uuid import uuid4

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware

from pui_adapter_service.config import Settings

logger = logging.getLogger("pui_adapter_service.http")


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        request_id = request.headers.get("x-request-id") or str(uuid4())
        request.state.request_id = request_id
        started_at = time()
        response = await call_next(request)
        duration_ms = round((time() - started_at) * 1000, 2)
        client_ip = InMemoryRateLimiter._client_key(request)
        response.headers["X-Request-ID"] = request_id
        logger.info(
            json.dumps(
                {
                    "event": "http_request",
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                    "client_ip": client_ip,
                },
                ensure_ascii=True,
            )
        )
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Cache-Control"] = "no-store"
        response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'; base-uri 'none'"
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


class InMemoryRateLimiter:
    def __init__(self, settings: Settings) -> None:
        self._window_seconds = settings.rate_limit_window_seconds
        self._login_limit = settings.login_rate_limit_requests
        self._api_limit = settings.api_rate_limit_requests
        self._events: dict[tuple[str, str], deque[float]] = {}

    def check_login(self, request: Request) -> None:
        self._check(request, scope="login", limit=self._login_limit)

    def check_api(self, request: Request) -> None:
        self._check(request, scope="api", limit=self._api_limit)

    def _check(self, request: Request, *, scope: str, limit: int) -> None:
        now = time()
        key = (scope, self._client_key(request))
        bucket = self._events.setdefault(key, deque())
        while bucket and bucket[0] <= now - self._window_seconds:
            bucket.popleft()
        if len(bucket) >= limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Demasiadas solicitudes",
            )
        bucket.append(now)

    @staticmethod
    def _client_key(request: Request) -> str:
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        client = request.client.host if request.client else "unknown"
        return client
