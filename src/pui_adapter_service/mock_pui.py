import os
from datetime import datetime, timedelta, timezone

import httpx
import jwt
from fastapi import FastAPI, Header, HTTPException, status


def _env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Missing env var: {name}")
    return value


app = FastAPI(title="PUI Mock")

_notifications: list[dict] = []
_finalizations: list[dict] = []
_reports: list[dict] = []


def _create_token(subject: str) -> str:
    secret = _env("PUI_MOCK_JWT_SECRET", "pui-mock-secret")
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=1)).timestamp()),
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def _check_bearer_token(auth_header: str | None) -> None:
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token no proporcionado")
    token = auth_header.split(" ", 1)[1]
    try:
        jwt.decode(token, _env("PUI_MOCK_JWT_SECRET", "pui-mock-secret"), algorithms=["HS256"])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido o expirado") from exc


@app.get("/health")
def health():
    return {"status": "ok", "service": "pui-mock"}


@app.get("/state")
def state():
    return {
        "notifications": _notifications,
        "finalizations": _finalizations,
        "reports": _reports,
    }


@app.post("/login")
def login(payload: dict):
    institucion_id = _env("PUI_MOCK_INSTITUCION_ID", "RFC123456ABC")
    clave = _env("PUI_MOCK_CLAVE", "ChangeMePassword1!")
    if payload.get("institucion_id") != institucion_id or payload.get("clave") != clave:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credenciales invalidas")
    return {"token": _create_token(payload["institucion_id"])}


@app.post("/notificar-coincidencia")
def notify_coincidence(payload: dict, authorization: str | None = Header(default=None)):
    _check_bearer_token(authorization)
    _notifications.append(payload)
    return {"message": "Coincidencia recibida correctamente"}


@app.post("/busqueda-finalizada")
def finalize_search(payload: dict, authorization: str | None = Header(default=None)):
    _check_bearer_token(authorization)
    _finalizations.append(payload)
    return {"message": "Registro de finalizacion de busqueda historica guardado correctamente."}


@app.get("/reportes")
def list_reports(authorization: str | None = Header(default=None)):
    _check_bearer_token(authorization)
    return _reports


def _dispatch_to_webhook(path: str, payload: dict) -> dict:
    webhook_base_url = _env("PUI_MOCK_WEBHOOK_BASE_URL", "http://localhost:8000")
    webhook_user = _env("PUI_MOCK_WEBHOOK_USER", "PUI")
    webhook_password = _env("PUI_MOCK_WEBHOOK_PASSWORD", "LocalPassword123!")

    login_response = httpx.post(
        f"{webhook_base_url.rstrip('/')}/login",
        json={"usuario": webhook_user, "clave": webhook_password},
        timeout=10,
    )
    login_response.raise_for_status()
    token = login_response.json()["token"]

    response = httpx.post(
        f"{webhook_base_url.rstrip('/')}/{path.lstrip('/')}",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


@app.post("/dispatch/activar-reporte")
def dispatch_activate_report(payload: dict):
    _reports.append(payload)
    return _dispatch_to_webhook("/activar-reporte", payload)


@app.post("/dispatch/activar-reporte-prueba")
def dispatch_activate_report_test(payload: dict):
    return _dispatch_to_webhook("/activar-reporte-prueba", payload)


@app.post("/dispatch/desactivar-reporte")
def dispatch_deactivate_report(payload: dict):
    return _dispatch_to_webhook("/desactivar-reporte", payload)
