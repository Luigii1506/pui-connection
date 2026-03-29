# Endpoints

## Endpoints inbound de la institucion

### `POST /login`

Uso:

- PUI obtiene un JWT para consumir nuestros endpoints protegidos

Payload:

- `usuario`: debe ser `PUI`
- `clave`: secreto compartido configurado para la institucion

Respuesta:

- `200`: `{ "token": "<jwt>" }`
- `401`: credenciales invalidas

### `POST /activar-reporte`

Uso:

- activa un caso real y dispara fase 1 + fase 2 + programacion de fase 3

Campos minimos:

- `id`
- `curp`
- `lugar_nacimiento`

Campos opcionales relevantes:

- `nombre`
- `primer_apellido`
- `segundo_apellido`
- `fecha_nacimiento`
- `fecha_desaparicion`
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

Respuesta MVP:

- `200`: `{"message":"La solicitud de activacion del reporte de busqueda se recibio correctamente."}`
- `400`: payload invalido
- `401`: JWT invalido o expirado
- `403`: sin permisos

### `POST /activar-reporte-prueba`

Uso:

- valida conectividad, autenticacion y contrato del payload antes de operar formalmente

Payload:

- mismo contrato base que `activar-reporte`

Respuesta MVP:

- `200`: `{"message":"La solicitud de activacion del reporte de prueba se recibio correctamente."}`

### `POST /desactivar-reporte`

Uso:

- detiene la busqueda continua y desactiva el caso

Payload:

- `id`

Respuesta MVP:

- `200`: `{"message":"La solicitud de desactivacion del reporte se recibio correctamente."}`

## Endpoints outbound hacia PUI

### `POST /login`

- autenticacion de la institucion ante PUI con `institucion_id` y `clave`

### `POST /notificar-coincidencia`

- notifica coincidencias de fase 1, 2 o 3
- debe incluir al menos:
  - `curp`
  - `id`
  - `institucion_id`
  - `lugar_nacimiento`
  - `fase_busqueda`

### `POST /busqueda-finalizada`

- marca el cierre de la fase 2
- debe incluir:
  - `id`
  - `institucion_id`

### `GET /reportes`

- permite resincronizacion o consulta de reportes activos enviados por PUI
