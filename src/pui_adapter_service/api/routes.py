from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from pui_adapter_service.api.schemas import (
    ActivateReportRequest,
    DeactivateReportRequest,
    HealthResponse,
    LoginRequest,
    LoginResponse,
    MessageResponse,
)
from pui_adapter_service.config import Settings, get_settings
from pui_adapter_service.db.session import get_db
from pui_adapter_service.security import authenticate_login_request, create_access_token, get_current_claims
from pui_adapter_service.services.reports import activate_report, deactivate_report

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health(settings: Settings = Depends(get_settings)) -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        environment=settings.app_env,
    )


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, settings: Settings = Depends(get_settings)) -> LoginResponse:
    if not authenticate_login_request(payload.usuario, payload.clave, settings):
        from fastapi import HTTPException

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas")

    token = create_access_token(subject=payload.usuario, settings=settings)
    return LoginResponse(token=token)


@router.post("/activar-reporte", response_model=MessageResponse)
def activate_report_endpoint(
    payload: ActivateReportRequest,
    db: Session = Depends(get_db),
    claims: dict = Depends(get_current_claims),
) -> MessageResponse:
    _ = claims
    activate_report(
        db,
        event_type="activar-reporte",
        payload=payload.model_dump(mode="json", exclude_none=True),
        is_test=False,
    )
    return MessageResponse(message="La solicitud de activacion del reporte de busqueda se recibio correctamente.")


@router.post("/activar-reporte-prueba", response_model=MessageResponse)
def activate_test_report_endpoint(
    payload: ActivateReportRequest,
    db: Session = Depends(get_db),
    claims: dict = Depends(get_current_claims),
) -> MessageResponse:
    _ = claims
    activate_report(
        db,
        event_type="activar-reporte-prueba",
        payload=payload.model_dump(mode="json", exclude_none=True),
        is_test=True,
    )
    return MessageResponse(message="La solicitud de activacion del reporte de prueba se recibio correctamente.")


@router.post("/desactivar-reporte", response_model=MessageResponse)
def deactivate_report_endpoint(
    payload: DeactivateReportRequest,
    db: Session = Depends(get_db),
    claims: dict = Depends(get_current_claims),
) -> MessageResponse:
    _ = claims
    deactivate_report(db, payload=payload.model_dump(mode="json", exclude_none=True))
    return MessageResponse(message="La solicitud de desactivacion del reporte se recibio correctamente.")
