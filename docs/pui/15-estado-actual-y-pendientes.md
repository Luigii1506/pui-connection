# Estado Actual y Pendientes

## Estado actual

El proyecto ya cubre:

- webhook inbound en Python
- autenticacion `POST /login`
- `POST /activar-reporte`
- `POST /activar-reporte-prueba`
- `POST /desactivar-reporte`
- fases 1, 2 y 3
- `busqueda-finalizada`
- auditoria basica
- deduplicacion minima
- sandbox local con Docker y Nginx
- core PHP simulado
- PUI mock local para pruebas E2E
- headers de seguridad, rate limiting y `X-Request-ID`

## Que ya se puede probar sin informacion real

- funcionamiento del webhook
- login de PUI hacia la institucion
- `activar-reporte-prueba`
- flujo de activacion real con fases 1 y 2
- fase 3 continua
- entrega outbound contra una PUI simulada
- flujo extremo a extremo local

## Que sigue bloqueado por informacion real

- RFC real con homoclave
- alta institucional via Llave MX
- e.Firma de la persona moral
- credenciales reales de sandbox
- password real de `/login`
- `PUBLIC_BASE_URL` real
- IP publica real
- infraestructura real de la empresa
- mapeo real del core PHP
- validacion oficial con PUI
- evidencia SAST, DAST y SCA

## Siguiente paso recomendado

1. Compartir `docs/pui/13-requerimientos-empresa-para-sandbox.md` con la empresa.
2. Obtener URL, IP y credenciales reales.
3. Desplegar `sandbox` con la configuracion de empresa.
4. Ejecutar `docs/pui/12-prueba-webhook.md`.
5. Cerrar la integracion real del core PHP.

## Estado de desarrollo

### Terminado

- MVP tecnico local
- seguridad HTTP base
- trazabilidad y auditoria
- pruebas locales y E2E con mocks

### Pendiente dependiente de la empresa

- onboarding oficial a PUI
- infraestructura publica de sandbox
- datos institucionales reales
- integracion real con el core PHP
