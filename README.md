# PUI Adapter Service

Servicio intermedio en Python para integrar el core PHP con la Plataforma Unica de Identidad (PUI) sin meter la logica regulatoria dentro del core.

## Objetivo

Cumplir el MVP obligatorio de integracion para instituciones diversas:

- recibir `activar-reporte`
- recibir `activar-reporte-prueba`
- recibir `desactivar-reporte`
- ejecutar fase 1, fase 2 y fase 3
- reportar coincidencias a PUI
- cerrar fase 2 con `busqueda-finalizada`
- mantener auditoria basica
- aplicar deduplicacion minima por evento
- usar `CURP` exacta como criterio principal de busqueda

## Fuente de verdad

La especificacion base para este repo es:

- `sources/MANUAL Técnico de la Solución Tecnológica para Instituciones Diversas.pdf`
- `sources/Presentacion de la PUI para Particulares.pdf`
- `sources/Guia_del_Sitio_de_Inscripcion_para_Instituciones_Diversas.pdf`

Los documentos en `docs/pui/` funcionan como traduccion operativa del manual al MVP del proyecto.

## Stack

- Python 3.12+
- FastAPI
- SQLAlchemy
- PostgreSQL en produccion
- SQLite para pruebas locales
- APScheduler para fase 3

## Estructura

- `src/pui_adapter_service/`: servicio principal
- `tests/`: pruebas minimas del MVP
- `docs/pui/`: especificacion interna derivada del manual oficial

## Variables principales

Ver `.env.example`.

## Ejecucion local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn pui_adapter_service.main:app --reload
```

## Pruebas

```bash
pytest
```

## Estado actual

La base inicial del servicio ya incluye:

- `healthcheck`
- autenticacion inbound por JWT para PUI
- endpoints inbound requeridos del MVP
- persistencia minima para reportes, eventos inbound y auditoria
- deduplicacion basica por huella del evento

Lo siguiente es implementar el cliente outbound hacia PUI y la orquestacion completa de fases 1, 2 y 3.
