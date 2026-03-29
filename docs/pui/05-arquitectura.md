# Arquitectura

## Decision principal

Servicio Python separado + core PHP como fuente de verdad + PUI como sistema externo de interoperabilidad.

## Componentes

- API inbound para recibir solicitudes oficiales de PUI
- Cliente outbound para notificar coincidencias y cierre de fase 2
- Capa de persistencia para reportes, eventos inbound, auditoria y estado de fases
- Adaptador de lectura al core PHP
- Scheduler para fase 3 continua

## Flujo interno

1. PUI llama nuestros endpoints inbound.
2. El servicio valida JWT y payload.
3. Se registra auditoria y deduplicacion.
4. Se persiste o actualiza el estado del reporte.
5. Se ejecutan consultas internas al core por `CURP`.
6. Se envian hallazgos a PUI.
7. El servicio mantiene la fase 3 hasta desactivacion.

## Principios de diseño

- simplicidad
- trazabilidad
- idempotencia
- separacion del core PHP
- cumplimiento minimo regulatorio

## Tecnologia elegida para el MVP

- FastAPI
- SQLAlchemy
- PostgreSQL en productivo
- APScheduler
- JWT para autenticacion inbound y outbound
