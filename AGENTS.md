# AGENTS.md

## Proyecto
Servicio intermedio en Python para integración con la Plataforma Única de Identidad (PUI).

## Contexto
La empresa ya cuenta con un sistema core grande en PHP nativo para centro cambiario.
El core maneja clientes, CURP, operaciones, alertas y reportes internos.
La lógica PUI NO debe integrarse directamente al core salvo necesidad estricta.

## Objetivo
Construir un MVP regulatorio que cumpla lo mínimo obligatorio:
- recibir activar-reporte
- recibir activar-reporte-prueba
- recibir desactivar-reporte
- ejecutar fase 1, fase 2 y fase 3
- reportar coincidencias
- cerrar fase 2 con busqueda-finalizada
- mantener auditoría básica
- deduplicación mínima por evento
- usar CURP exacta como criterio principal de búsqueda

## Restricciones
- No agregar funcionalidades “nice to have”.
- No implementar fuzzy matching por nombre.
- No implementar biométricos en MVP salvo requisito confirmado.
- No modificar el core PHP salvo que sea indispensable.
- Priorizar trazabilidad, simplicidad, idempotencia y cumplimiento.

## Antes de programar
Leer:
- docs/pui/00-resumen-ejecutivo.md
- docs/pui/01-requisitos-obligatorios.md
- docs/pui/02-flujo-oficial.md
- docs/pui/03-mvp-alcance.md
- docs/pui/04-mapeo-core-php.md
- docs/pui/05-arquitectura.md
- docs/pui/07-endpoints.md

## Forma de trabajar
- Primero proponer plan.
- Luego listar archivos a crear/modificar.
- Después implementar por fases pequeñas.
- Agregar pruebas mínimas.
