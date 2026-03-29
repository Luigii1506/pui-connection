from fastapi.testclient import TestClient

from pui_adapter_service.mock_pui import app


def test_mock_pui_login_and_notification_flow(monkeypatch):
    monkeypatch.setenv("PUI_MOCK_INSTITUCION_ID", "RFC123456ABC")
    monkeypatch.setenv("PUI_MOCK_CLAVE", "ChangeMePassword1!")
    monkeypatch.setenv("PUI_MOCK_JWT_SECRET", "mock-secret")

    with TestClient(app) as client:
        login_response = client.post(
            "/login",
            json={"institucion_id": "RFC123456ABC", "clave": "ChangeMePassword1!"},
        )
        assert login_response.status_code == 200
        token = login_response.json()["token"]

        notify_response = client.post(
            "/notificar-coincidencia",
            json={"id": "test", "curp": "SIMU010101HDFABC01", "fase_busqueda": "1"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert notify_response.status_code == 200
        assert notify_response.json()["message"] == "Coincidencia recibida correctamente"
