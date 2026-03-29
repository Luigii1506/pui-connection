# Casos Borde y Riesgos

## Casos borde funcionales

- `activar-reporte` duplicado con el mismo payload
- `desactivar-reporte` para un `id` inexistente
- `fecha_desaparicion` ausente
- `fecha_desaparicion` mayor a 12 anos de antiguedad
- payload con datos parciales
- coincidencia en fase 1 pero no en fase 2
- ningun hallazgo en fase 1 ni fase 2, pero fase 3 debe quedar activa

## Riesgos tecnicos

- mapeo incompleto del core PHP
- inconsistencias de `CURP` en datos historicos
- falta de campo de fecha confiable para fase 2
- falta de marca de ultimo cambio para fase 3
- scheduler duplicado en despliegues con multiples replicas

## Riesgos regulatorios

- no cerrar fase 2 con `busqueda-finalizada`
- no poder demostrar trazabilidad
- no cumplir requisitos de seguridad previos a certificacion
- almacenar de mas datos sensibles en logs

## Decision MVP

- priorizar exactitud por `CURP`
- rechazar payloads mal formados
- deduplicar por huella del evento
- dejar biometria fuera mientras no sea requisito confirmado
