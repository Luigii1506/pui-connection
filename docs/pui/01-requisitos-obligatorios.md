# Requisitos Obligatorios

## Endpoints inbound que debe exponer la institucion

- `POST /login`
- `POST /activar-reporte`
- `POST /activar-reporte-prueba`
- `POST /desactivar-reporte`

## Endpoints outbound de PUI que debemos consumir

- `POST /login`
- `POST /notificar-coincidencia`
- `POST /busqueda-finalizada`
- `GET /reportes`

## Requisitos funcionales del MVP

- Usar `CURP` exacta como llave principal de busqueda
- Ejecutar fase 1 al recibir `activar-reporte`
- Ejecutar fase 2 historica desde `fecha_desaparicion` hasta el presente
- Limitar fase 2 a maximo 12 anos hacia atras
- Enviar una notificacion por cada coincidencia encontrada
- Cerrar fase 2 con `busqueda-finalizada` aunque no haya coincidencias
- Mantener fase 3 activa hasta recibir `desactivar-reporte`
- Detener tareas periodicas asociadas al `id` al desactivar

## Requisitos no funcionales minimos

- JWT Bearer en endpoints protegidos
- TLS 1.2 o superior
- Validacion estricta de payloads
- Logs estructurados de solicitudes, consultas internas y respuestas enviadas
- Auditoria basica
- Deduplicacion minima por evento
- Rate limiting y respuestas seguras para 401, 403, 400 y 429

## Fuera del MVP

- Fuzzy matching por nombre
- Biometrics obligatorios
- UI administrativa
- Cambios directos al core PHP salvo necesidad indispensable
