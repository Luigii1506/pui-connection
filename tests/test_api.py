from sqlalchemy import select

from pui_adapter_service.db.models import InboundEvent, Report
from pui_adapter_service.db.session import get_session_factory


def _login(client) -> str:
    response = client.post("/login", json={"usuario": "PUI", "clave": "TestPassword123!"})
    assert response.status_code == 200
    return response.json()["token"]


def _auth_headers(client) -> dict[str, str]:
    token = _login(client)
    return {"Authorization": f"Bearer {token}"}


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_login_returns_jwt(client):
    response = client.post("/login", json={"usuario": "PUI", "clave": "TestPassword123!"})
    assert response.status_code == 200
    assert "token" in response.json()


def test_activate_report_prueba_is_idempotent(client):
    payload = {
        "id": "A1B2C3D4E5F6-550e8400-e29b-41d4-a716-446655440000",
        "curp": "TEST010101HDFABC01",
        "nombre": "JUAN",
        "primer_apellido": "PEREZ",
        "segundo_apellido": "LOPEZ",
        "fecha_nacimiento": "1990-01-01",
        "fecha_desaparicion": "2024-12-15",
        "lugar_nacimiento": "CDMX",
        "sexo_asignado": "H",
        "telefono": "5512345678",
        "correo": "juan.perez@example.com",
        "direccion": "CALLE FICTICIA 123, CENTRO",
        "calle": "CALLE FICTICIA",
        "numero": "123",
        "colonia": "CENTRO",
        "codigo_postal": "06000",
        "municipio_o_alcaldia": "CUAUHTEMOC",
        "entidad_federativa": "CDMX",
    }

    headers = _auth_headers(client)
    first = client.post("/activar-reporte-prueba", json=payload, headers=headers)
    second = client.post("/activar-reporte-prueba", json=payload, headers=headers)

    assert first.status_code == 200
    assert second.status_code == 200

    session = get_session_factory()()
    try:
        events = session.scalars(select(InboundEvent).where(InboundEvent.event_type == "activar-reporte-prueba")).all()
        assert len(events) == 1
    finally:
        session.close()


def test_desactivar_reporte_marks_report_inactive(client):
    activation_payload = {
        "id": "A1B2C3D4E5F6-550e8400-e29b-41d4-a716-446655440001",
        "curp": "TEST010101HDFABC01",
        "lugar_nacimiento": "CDMX",
    }

    headers = _auth_headers(client)
    activate_response = client.post("/activar-reporte", json=activation_payload, headers=headers)
    assert activate_response.status_code == 200

    deactivate_response = client.post(
        "/desactivar-reporte",
        json={"id": activation_payload["id"]},
        headers=headers,
    )
    assert deactivate_response.status_code == 200

    session = get_session_factory()()
    try:
        report = session.get(Report, activation_payload["id"])
        assert report is not None
        assert report.status == "inactive"
        assert report.continuous_search_enabled is False
    finally:
        session.close()
