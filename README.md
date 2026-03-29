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

Plantillas recomendadas:

- `.env.local.example`
- `.env.local.mock.example`
- `.env.sandbox.example`
- `.env.production.example`

## Modo simulado del core PHP

Mientras no exista el mapeo real del core, el servicio puede operar con `CORE_BACKEND=simulated`.

- dataset por defecto: `src/pui_adapter_service/fixtures/core_simulation.json`
- override opcional: `CORE_SIMULATION_FILE=/ruta/al/json`

Esto permite ejercitar fases 1, 2 y 3 sin depender todavia del sistema PHP real.

## Ambientes

La transicion correcta es `local -> sandbox -> production`.

- `local`: desarrollo con cuentas y datos no oficiales
- `sandbox`: pruebas oficiales con identidad e infraestructura de la empresa
- `production`: operacion real con PUI

Referencia: `docs/pui/10-despliegue-ambientes.md`

Documento para la empresa:

- `docs/pui/13-requerimientos-empresa-para-sandbox.md`

## Ejecucion local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn pui_adapter_service.main:app --reload
```

## Sandbox con Docker

Artefactos disponibles:

- `Dockerfile`
- `docker-compose.yml`
- `deploy/nginx/sandbox.conf`
- `docs/pui/11-playbook-sandbox.md`
- `docs/pui/12-prueba-webhook.md`
- `docs/pui/14-pui-mock-local.md`
- `scripts/sandbox_smoke_test.sh`

Flujo base:

```bash
cp .env.sandbox.example .env.sandbox
docker compose --env-file .env.sandbox up --build
```

Acceso local de prueba:

```bash
curl http://localhost:8080/health
```

Ensayo del webhook:

```bash
export PUI_INBOUND_PASSWORD='tu_password_de_sandbox'
./scripts/sandbox_smoke_test.sh
```

Flujo E2E local con PUI mock:

```bash
./scripts/local_e2e_with_mock_pui.sh
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

Tambien ya incluye:

- simulacion del core PHP por archivo JSON
- separacion de ambientes `local`, `sandbox` y `production`
- validaciones de configuracion para onboarding real
- artefactos base de despliegue para sandbox
- headers de seguridad, errores consistentes y rate limiting basico
- `X-Request-ID` y logging estructurado por request
