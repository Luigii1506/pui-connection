import httpx

from pui_adapter_service.config import Settings


class PUIClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._token: str | None = None

    def login(self) -> str:
        if self._token is not None:
            return self._token

        response = httpx.post(
            f"{self._settings.pui_outbound_base_url.rstrip('/')}/login",
            json={
                "institucion_id": self._settings.pui_outbound_institucion_id,
                "clave": self._settings.pui_outbound_clave,
            },
            timeout=self._settings.pui_request_timeout_seconds,
        )
        response.raise_for_status()
        self._token = response.json()["token"]
        return self._token

    def _authorized_post(self, path: str, payload: dict, *, retry: bool = True) -> dict:
        token = self.login()
        response = httpx.post(
            f"{self._settings.pui_outbound_base_url.rstrip('/')}/{path.lstrip('/')}",
            json=payload,
            headers={"Authorization": f"Bearer {token}"},
            timeout=self._settings.pui_request_timeout_seconds,
        )
        if response.status_code == 401 and retry:
            self._token = None
            return self._authorized_post(path, payload, retry=False)

        response.raise_for_status()
        if not response.content:
            return {}
        return response.json()

    def notify_coincidence(self, payload: dict) -> dict:
        return self._authorized_post("/notificar-coincidencia", payload)

    def finalize_search(self, report_id: str) -> dict:
        return self._authorized_post(
            "/busqueda-finalizada",
            {
                "id": report_id,
                "institucion_id": self._settings.pui_outbound_institucion_id,
            },
        )

    def list_reports(self) -> list[dict]:
        token = self.login()
        response = httpx.get(
            f"{self._settings.pui_outbound_base_url.rstrip('/')}/reportes",
            headers={"Authorization": f"Bearer {token}"},
            timeout=self._settings.pui_request_timeout_seconds,
        )
        if response.status_code == 401:
            self._token = None
            token = self.login()
            response = httpx.get(
                f"{self._settings.pui_outbound_base_url.rstrip('/')}/reportes",
                headers={"Authorization": f"Bearer {token}"},
                timeout=self._settings.pui_request_timeout_seconds,
            )

        response.raise_for_status()
        return response.json()
