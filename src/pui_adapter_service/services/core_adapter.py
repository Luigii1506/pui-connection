import json
from datetime import datetime
from pathlib import Path

from pui_adapter_service.config import Settings


def _default_simulation_file() -> Path:
    return Path(__file__).resolve().parent.parent / "fixtures" / "core_simulation.json"


class SimulatedCoreSearchService:
    def __init__(self, settings: Settings) -> None:
        simulation_file = settings.core_simulation_file or str(_default_simulation_file())
        self._data = json.loads(Path(simulation_file).read_text(encoding="utf-8"))

    def search_basic_by_curp(self, curp: str) -> list[dict]:
        return [self._strip_curp(item) for item in self._data.get("basic", []) if item.get("curp") == curp]

    def search_historical_by_curp(self, curp: str, *, from_date: str | None) -> list[dict]:
        return [
            self._strip_curp(item)
            for item in self._data.get("historical", [])
            if item.get("curp") == curp and self._matches_from_date(item.get("fecha_evento"), from_date)
        ]

    def search_continuous_by_curp(self, curp: str, *, since: str | None) -> list[dict]:
        return [
            self._strip_curp(item)
            for item in self._data.get("continuous", [])
            if item.get("curp") == curp and self._matches_since(item.get("fecha_evento"), since)
        ]

    @staticmethod
    def _strip_curp(item: dict) -> dict:
        return {key: value for key, value in item.items() if key != "curp"}

    @staticmethod
    def _matches_from_date(event_date: str | None, from_date: str | None) -> bool:
        if event_date is None or from_date is None:
            return True
        return event_date >= from_date

    @staticmethod
    def _matches_since(event_date: str | None, since: str | None) -> bool:
        if event_date is None or since is None:
            return True
        try:
            since_dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
            return event_date >= since_dt.date().isoformat()
        except ValueError:
            return True


class CoreSearchService:
    """Fachada del backend de consulta al core.

    Mientras no exista la conexion real al core PHP, el backend por defecto es
    una simulacion basada en archivo JSON.
    """

    def __init__(self, settings: Settings) -> None:
        if settings.core_backend != "simulated":
            raise ValueError(f"CORE_BACKEND no soportado: {settings.core_backend}")
        self._backend = SimulatedCoreSearchService(settings)

    def search_basic_by_curp(self, curp: str) -> list[dict]:
        return self._backend.search_basic_by_curp(curp)

    def search_historical_by_curp(self, curp: str, *, from_date: str | None) -> list[dict]:
        return self._backend.search_historical_by_curp(curp, from_date=from_date)

    def search_continuous_by_curp(self, curp: str, *, since: str | None) -> list[dict]:
        return self._backend.search_continuous_by_curp(curp, since=since)
