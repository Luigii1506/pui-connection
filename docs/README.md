# Documentacion del Proyecto

Este archivo es el punto de entrada principal de la documentacion del repositorio.

## Empezar por perfil

### Si eres programador

Lee en este orden:

1. `README.md`
2. `TASKS.md`
3. `docs/pui/15-estado-actual-y-pendientes.md`
4. `docs/pui/05-arquitectura.md`
5. `docs/pui/07-endpoints.md`
6. `docs/pui/06-modelo-datos.md`
7. `docs/pui/14-pui-mock-local.md`

Archivos tecnicos clave:

- `src/pui_adapter_service/`
- `tests/`
- `scripts/`

### Si eres encargado de cumplimiento o negocio

Lee en este orden:

1. `docs/pui/00-resumen-ejecutivo.md`
2. `docs/pui/01-requisitos-obligatorios.md`
3. `docs/pui/03-mvp-alcance.md`
4. `docs/pui/13-requerimientos-empresa-para-sandbox.md`
5. `docs/pui/15-estado-actual-y-pendientes.md`

### Si eres responsable de infraestructura o DevOps

Lee en este orden:

1. `docs/pui/10-despliegue-ambientes.md`
2. `docs/pui/11-playbook-sandbox.md`
3. `docs/pui/09-checklist-sandbox-seguridad.md`
4. `docs/pui/12-prueba-webhook.md`

Artefactos clave:

- `Dockerfile`
- `docker-compose.yml`
- `deploy/nginx/sandbox.conf`
- `.env.local.example`
- `.env.local.mock.example`
- `.env.sandbox.example`
- `.env.production.example`

## Mapa de documentacion

### Base funcional

- `docs/pui/00-resumen-ejecutivo.md`
- `docs/pui/01-requisitos-obligatorios.md`
- `docs/pui/02-flujo-oficial.md`
- `docs/pui/03-mvp-alcance.md`

### Diseno tecnico

- `docs/pui/04-mapeo-core-php.md`
- `docs/pui/05-arquitectura.md`
- `docs/pui/06-modelo-datos.md`
- `docs/pui/07-endpoints.md`
- `docs/pui/08-casos-borde-y-riesgos.md`

### Sandbox y operacion

- `docs/pui/09-checklist-sandbox-seguridad.md`
- `docs/pui/10-despliegue-ambientes.md`
- `docs/pui/11-playbook-sandbox.md`
- `docs/pui/12-prueba-webhook.md`
- `docs/pui/13-requerimientos-empresa-para-sandbox.md`
- `docs/pui/14-pui-mock-local.md`

### Estado y seguimiento

- `docs/pui/15-estado-actual-y-pendientes.md`
- `TASKS.md`

## Mapa del repo

### Codigo

- `src/pui_adapter_service/main.py`: arranque de la API
- `src/pui_adapter_service/api/`: rutas y esquemas
- `src/pui_adapter_service/services/`: orquestacion, core simulado y cliente PUI
- `src/pui_adapter_service/mock_pui.py`: PUI mock local
- `src/pui_adapter_service/db/`: persistencia

### Pruebas

- `tests/test_api.py`: flujo principal del adapter
- `tests/test_config.py`: validaciones de ambientes
- `tests/test_security.py`: seguridad del webhook
- `tests/test_mock_pui.py`: validacion basica de PUI mock

### Scripts

- `scripts/sandbox_smoke_test.sh`: smoke test del webhook
- `scripts/local_e2e_with_mock_pui.sh`: flujo extremo a extremo local
- `scripts/payloads/`: payloads base para pruebas
