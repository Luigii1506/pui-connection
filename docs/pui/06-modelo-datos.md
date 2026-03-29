# Modelo de Datos

## Tabla `reports`

Representa cada `id` de busqueda recibido de PUI.

Campos minimos:

- `id`
- `curp`
- `status`
- `is_test`
- `continuous_search_enabled`
- `phase_1_completed_at`
- `phase_2_completed_at`
- `last_phase_3_check_at`
- `payload`
- `created_at`
- `updated_at`

## Tabla `inbound_events`

Representa cada evento inbound recibido para soporte de idempotencia.

Campos minimos:

- `id`
- `event_type`
- `report_id`
- `payload_hash`
- `payload`
- `created_at`

Regla:

- unicidad minima por `event_type + report_id + payload_hash`

## Tabla `audit_logs`

Bitacora estructurada basica para trazabilidad.

Campos minimos:

- `id`
- `direction` (`inbound`, `internal`, `outbound`)
- `event_type`
- `report_id`
- `payload`
- `created_at`

## Tablas siguientes del roadmap

## Tabla `phase_runs`

Bitacora estructurada de ejecucion de cada fase.

Campos minimos:

- `report_id`
- `phase_name`
- `status`
- `requested_from_date`
- `effective_from_date`
- `started_at`
- `completed_at`
- `details`

## Tabla `outbound_deliveries`

Registro de cada intento o salto de entrega hacia PUI.

Campos minimos:

- `report_id`
- `endpoint`
- `phase_busqueda`
- `delivery_status`
- `request_payload`
- `response_payload`
- `created_at`

## Siguiente del roadmap

- `phase_3_jobs`
