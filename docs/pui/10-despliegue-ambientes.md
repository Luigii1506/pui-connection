# Despliegue por Ambientes

## Regla principal

No mezclar pruebas personales con el alta oficial de la empresa.

- `local`: desarrollo individual, datos simulados, sin conexion oficial a PUI
- `sandbox`: validacion tecnica con identidad, RFC, URL e IP de la empresa
- `production`: operacion real con credenciales y aprobacion oficial

## Local

Objetivo:

- desarrollar el servicio
- probar payloads, fases y auditoria
- simular el core PHP

Configuracion base:

- `.env.local.example`
- `CORE_BACKEND=simulated`
- `PUI_OUTBOUND_ENABLED=false`

No requiere:

- Llave MX de persona moral
- e.Firma de la empresa
- credenciales reales de PUI

## Sandbox

Objetivo:

- validar webhook
- probar conectividad oficial
- ejecutar pruebas funcionales previas a produccion

Configuracion base:

- `.env.sandbox.example`
- `APP_ENV=sandbox`
- `PUBLIC_BASE_URL` real de la empresa
- credenciales reales registradas para sandbox

Requiere:

- alta institucional via Llave MX
- e.Firma de la persona moral
- RFC real con homoclave
- IP publica registrada
- URL base HTTPS registrada

## Production

Objetivo:

- operar con PUI en forma real

Configuracion base:

- `.env.production.example`
- `APP_ENV=production`
- `DATABASE_URL` productiva
- `PUI_OUTBOUND_ENABLED=true`

Requiere adicionalmente:

- aprobacion de sandbox
- evidencia SAST, DAST y SCA
- monitoreo y respaldos

## Secuencia recomendada

1. Desarrollar y probar todo en `local`.
2. Congelar contrato del webhook.
3. Registrar la empresa en PUI.
4. Desplegar una instancia `sandbox` con dominio de la empresa.
5. Ejecutar `activar-reporte-prueba`.
6. Ajustar credenciales y seguridad.
7. Pasar a `production`.
