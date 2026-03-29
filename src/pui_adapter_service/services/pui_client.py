from pui_adapter_service.config import Settings


class PUIClient:
    """Cliente outbound hacia PUI.

    Se deja como esqueleto para la siguiente fase de implementacion.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
