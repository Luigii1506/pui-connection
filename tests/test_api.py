from sqlalchemy import select

from pui_adapter_service.db.models import AuditLog, InboundEvent, OutboundDelivery, PhaseRun, Report
from pui_adapter_service.db.session import get_session_factory
from pui_adapter_service.scheduler import Phase3SchedulerService
from pui_adapter_service.config import get_settings


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


def test_activate_report_runs_initial_phases(client):
    activation_payload = {
        "id": "A1B2C3D4E5F6-550e8400-e29b-41d4-a716-446655440099",
        "curp": "TEST010101HDFABC01",
        "lugar_nacimiento": "CDMX",
        "fecha_desaparicion": "2024-12-15",
    }

    headers = _auth_headers(client)
    response = client.post("/activar-reporte", json=activation_payload, headers=headers)
    assert response.status_code == 200

    session = get_session_factory()()
    try:
        report = session.get(Report, activation_payload["id"])
        assert report is not None
        assert report.phase_1_completed_at is not None
        assert report.phase_2_completed_at is not None
        assert report.continuous_search_enabled is True

        audit_events = session.scalars(select(AuditLog.event_type)).all()
        assert "phase-1.completed" in audit_events
        assert "phase-2.completed" in audit_events
        assert "busqueda-finalizada.skipped" in audit_events
    finally:
        session.close()


def test_phase_2_window_is_capped_to_12_years(client):
    activation_payload = {
        "id": "A1B2C3D4E5F6-550e8400-e29b-41d4-a716-446655440777",
        "curp": "TEST010101HDFABC01",
        "lugar_nacimiento": "CDMX",
        "fecha_desaparicion": "2000-01-15",
    }

    headers = _auth_headers(client)
    response = client.post("/activar-reporte", json=activation_payload, headers=headers)
    assert response.status_code == 200

    session = get_session_factory()()
    try:
        phase_2_run = session.scalar(
            select(PhaseRun).where(
                PhaseRun.report_id == activation_payload["id"],
                PhaseRun.phase_name == "2",
            )
        )
        assert phase_2_run is not None
        assert phase_2_run.requested_from_date.isoformat() == "2000-01-15"
        assert phase_2_run.effective_from_date.isoformat() != "2000-01-15"
        assert phase_2_run.status == "completed"
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


def test_phase_3_cycle_updates_active_reports(client):
    activation_payload = {
        "id": "A1B2C3D4E5F6-550e8400-e29b-41d4-a716-446655440123",
        "curp": "TEST010101HDFABC01",
        "lugar_nacimiento": "CDMX",
    }

    headers = _auth_headers(client)
    response = client.post("/activar-reporte", json=activation_payload, headers=headers)
    assert response.status_code == 200

    service = Phase3SchedulerService(get_settings())
    service.run_cycle()

    session = get_session_factory()()
    try:
        report = session.get(Report, activation_payload["id"])
        assert report is not None
        assert report.last_phase_3_check_at is not None

        audit_events = session.scalars(select(AuditLog.event_type).where(AuditLog.report_id == activation_payload["id"])).all()
        assert "phase-3.started" in audit_events
        assert "phase-3.completed" in audit_events
    finally:
        session.close()


def test_outbound_deliveries_are_recorded_when_outbound_is_skipped(client):
    activation_payload = {
        "id": "A1B2C3D4E5F6-550e8400-e29b-41d4-a716-446655440124",
        "curp": "TEST010101HDFABC01",
        "lugar_nacimiento": "CDMX",
    }

    headers = _auth_headers(client)
    response = client.post("/activar-reporte", json=activation_payload, headers=headers)
    assert response.status_code == 200

    session = get_session_factory()()
    try:
        deliveries = session.scalars(
            select(OutboundDelivery).where(OutboundDelivery.report_id == activation_payload["id"])
        ).all()
        assert len(deliveries) == 1
        assert deliveries[0].endpoint == "busqueda-finalizada"
        assert deliveries[0].delivery_status == "skipped"
    finally:
        session.close()
