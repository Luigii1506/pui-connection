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

- `outbound_deliveries`
- `phase_runs`
- `phase_3_jobs`
