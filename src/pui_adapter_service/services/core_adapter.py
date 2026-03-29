class CoreSearchService:
    """Adaptador minimo del core PHP.

    La integracion real se implementara cuando exista el mapeo de tablas y
    consultas exactas. Por ahora devuelve listas vacias para permitir la
    orquestacion del flujo sin acoplarse al core.
    """

    def search_basic_by_curp(self, curp: str) -> list[dict]:
        _ = curp
        return []

    def search_historical_by_curp(self, curp: str, *, from_date: str | None) -> list[dict]:
        _ = (curp, from_date)
        return []

    def search_continuous_by_curp(self, curp: str, *, since: str | None) -> list[dict]:
        _ = (curp, since)
        return []
