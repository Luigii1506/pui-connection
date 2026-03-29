# Mapeo Core PHP

## Principio

El core PHP sigue siendo la fuente de verdad. El servicio PUI solo consulta y transforma informacion para cumplir con la interoperabilidad requerida por SEGOB.

## Datos que el servicio necesita del core

- `curp`
- `nombre`
- `primer_apellido`
- `segundo_apellido`
- `fecha_nacimiento`
- `lugar_nacimiento`
- `sexo_asignado`
- `telefono`
- `correo`
- `direccion`
- `calle`
- `numero`
- `colonia`
- `codigo_postal`
- `municipio_o_alcaldia`
- `entidad_federativa`
- historial de eventos administrativos para fase 2
- eventos nuevos o modificados para fase 3

## Consultas minimas requeridas

- Consulta por `CURP` exacta para datos basicos mas recientes
- Consulta historica por `CURP` exacta y rango de fechas
- Consulta incremental por `CURP` exacta y fecha de ultimo procesamiento

## Pendientes de mapeo real

Definir en cuanto se conozca el core:

- tabla o vista maestra de clientes
- tabla o vista donde vive la `CURP`
- tablas de operaciones o eventos administrativos que sirven como coincidencias
- campos de fecha relevantes para fase 2
- campos que permiten detectar nuevos o modificados para fase 3
- restricciones de acceso al core y mecanismo de lectura recomendado

## Estado actual del proyecto

Mientras no exista el mapeo real del core PHP, el servicio opera con un backend simulado configurable por archivo JSON.

- variable: `CORE_BACKEND=simulated`
- archivo por defecto: `src/pui_adapter_service/fixtures/core_simulation.json`

## Regla de integracion

- Preferir lectura desde vistas o consultas dedicadas
- No mover logica PUI al core
- No modificar tablas del core para el MVP salvo necesidad comprobada
