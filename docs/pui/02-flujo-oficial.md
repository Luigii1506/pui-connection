# Flujo Oficial

## Flujo operativo

1. PUI autentica contra nuestro `POST /login`.
2. PUI envia `POST /activar-reporte` con `id`, `curp` y datos disponibles.
3. El servicio valida JWT, registra el evento y activa el reporte.
4. Se ejecuta fase 1 para completar datos basicos mas recientes.
5. Si hay coincidencia en fase 1, se envia `POST /notificar-coincidencia` a PUI con `fase_busqueda=1`.
6. Se ejecuta fase 2 historica desde `fecha_desaparicion` hasta hoy, con tope maximo de 12 anos.
7. Por cada hallazgo de fase 2, se envia `POST /notificar-coincidencia` con `fase_busqueda=2`.
8. Al terminar fase 2, siempre se envia `POST /busqueda-finalizada`.
9. El caso entra en fase 3 continua.
10. Fase 3 revisa periodicamente registros nuevos o modificados relacionados con la `CURP`.
11. Por cada hallazgo de fase 3, se envia `POST /notificar-coincidencia` con `fase_busqueda=3`.
12. PUI envia `POST /desactivar-reporte`.
13. El servicio desactiva el caso, detiene tareas periodicas y conserva trazabilidad.

## Flujo de certificacion previa

1. PUI autentica contra nuestro `POST /login`.
2. PUI envia `POST /activar-reporte-prueba`.
3. El servicio valida autenticacion, payload y respuesta HTTP.
4. Si la prueba es exitosa, la institucion puede continuar con la inscripcion y validacion.
