# TASKS

Estado resumido:

- terminado: base del servicio, endpoints inbound, fases 1-3, core simulado, sandbox local, PUI mock, seguridad base
- pendiente con informacion real: alta institucional, credenciales reales, infraestructura publica, core PHP real

## Fase 0. Aterrizaje de especificacion

- Alinear `docs/pui/` al manual oficial y la presentacion
- Fijar payloads, estados internos y respuestas HTTP del MVP
- Documentar riesgos, sandbox y seguridad minima

## Fase 1. Base del servicio

- Crear `pyproject.toml`
- Configurar FastAPI
- Configurar settings por variables de entorno
- Configurar base de datos y modelos base
- Exponer `GET /health`

## Fase 2. Endpoints inbound requeridos

- Implementar `POST /login`
- Implementar `POST /activar-reporte`
- Implementar `POST /activar-reporte-prueba`
- Implementar `POST /desactivar-reporte`
- Agregar validacion fuerte del payload y JWT Bearer

## Fase 3. Persistencia, auditoria e idempotencia

- Guardar reportes activos
- Guardar eventos inbound recibidos
- Guardar auditoria basica de entradas
- Aplicar deduplicacion minima por `event_type + report_id + payload_hash`

## Fase 4. Integracion outbound con PUI

- Consumir `POST /login` de PUI
- Consumir `POST /notificar-coincidencia`
- Consumir `POST /busqueda-finalizada`
- Consumir `GET /reportes` para resincronizacion basica

## Fase 5. Busquedas

- Implementar fase 1 con datos basicos mas recientes
- Implementar fase 2 historica con limite maximo de 12 anos
- Implementar fase 3 continua con scheduler

## Fase 6. Core PHP

- Conectar el servicio con el core PHP como fuente de verdad
- Definir mapeo real de tablas, campos y consultas por CURP
- Mantener el core sin cambios salvo necesidad estricta

## Fase 7. Validacion

- Pruebas unitarias y de integracion minima
- Checklist de sandbox
- Checklist de seguridad previa a certificacion
