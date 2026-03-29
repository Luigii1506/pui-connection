# Checklist Sandbox y Seguridad

## Sandbox

- endpoint publico accesible por HTTPS
- IP publica registrada para whitelist
- URL base definida
- `POST /login` funcionando
- `POST /activar-reporte-prueba` funcionando
- credenciales de prueba validadas
- respuesta 200 en prueba de webhook

## Seguridad minima

- TLS 1.2 o superior
- JWT con expiracion
- validacion estricta de payload
- respuestas 401 y 403 sin filtrar detalles internos
- rate limiting
- logs estructurados
- sin stacktraces expuestos
- sin headers `Server` o `X-Powered-By`

## Evidencia para aprobacion

- reporte SAST
- reporte DAST
- reporte SCA
- alcance, metodologia y fecha de ejecucion
- URLs evaluadas
- evidencia sin hallazgos criticos, altos, medios o bajos

## Operacion

- monitoreo de disponibilidad
- monitoreo de errores outbound
- plan de resincronizacion de reportes activos
