# PUI Mock Local

## Objetivo

Probar el flujo extremo a extremo sin depender todavia del `sandbox` oficial:

- una PUI mock local recibe las notificaciones outbound del adapter
- la PUI mock local tambien dispara `activar-reporte` hacia nuestro webhook

## Componentes

- adapter principal: `pui_adapter_service.main:app`
- PUI mock: `pui_adapter_service.mock_pui:app`

## Variables utiles para la PUI mock

- `PUI_MOCK_INSTITUCION_ID`
- `PUI_MOCK_CLAVE`
- `PUI_MOCK_JWT_SECRET`
- `PUI_MOCK_WEBHOOK_BASE_URL`
- `PUI_MOCK_WEBHOOK_USER`
- `PUI_MOCK_WEBHOOK_PASSWORD`

## Ejecucion manual

### Terminal 1: adapter

```bash
cp .env.local.mock.example .env
source .venv/bin/activate
uvicorn pui_adapter_service.main:app --reload --port 8000
```

### Terminal 2: PUI mock

```bash
export PUI_MOCK_WEBHOOK_BASE_URL='http://localhost:8000'
export PUI_MOCK_WEBHOOK_PASSWORD='LocalPassword123!'
source .venv/bin/activate
uvicorn pui_adapter_service.mock_pui:app --reload --port 8010
```

### Terminal 3: flujo E2E

```bash
./scripts/local_e2e_with_mock_pui.sh
```

## Resultado esperado

- la PUI mock envia `activar-reporte` al adapter
- el adapter ejecuta fases 1 y 2 con el core simulado
- el adapter envia `notificar-coincidencia` y `busqueda-finalizada` a la PUI mock
- el endpoint `/state` de la PUI mock muestra las notificaciones recibidas

## Archivo recomendado

- `.env.local.mock.example`
