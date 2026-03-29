# Prueba del Webhook

## Objetivo

Ejecutar un ensayo controlado del flujo minimo que PUI usara contra la institucion:

1. `GET /health`
2. `POST /login`
3. `POST /activar-reporte-prueba`

## Requisitos

- entorno `sandbox` levantado
- `PUI_INBOUND_PASSWORD` configurado
- webhook accesible por la URL que se este probando

## Script incluido

Archivo:

- `scripts/sandbox_smoke_test.sh`

Payload base:

- `scripts/payloads/activar_reporte_prueba.json`

## Ejecucion local contra el proxy del compose

```bash
export PUI_INBOUND_PASSWORD='tu_password_de_sandbox'
./scripts/sandbox_smoke_test.sh
```

## Ejecucion contra una URL publica

```bash
export BASE_URL='https://sandbox-pui.empresa.com'
export PUI_INBOUND_PASSWORD='tu_password_de_sandbox'
./scripts/sandbox_smoke_test.sh
```

## Resultado esperado

- `/health` responde `200`
- `/login` responde `200` con `token`
- `/activar-reporte-prueba` responde `200`
- todas las respuestas incluyen `X-Request-ID`

## Observaciones

- el script genera un `REPORT_ID` distinto en cada ejecucion
- si el proxy publico esta bien configurado, el flujo debe funcionar igual que en local
- este ensayo no sustituye la prueba oficial de PUI, pero reduce errores antes del alta
- conserva el `X-Request-ID` de cualquier intento fallido para rastrearlo en logs
