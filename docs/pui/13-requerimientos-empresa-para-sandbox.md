# Requerimientos de la Empresa Para Sandbox

## Objetivo del documento

Este documento esta pensado para la persona de la empresa que debe coordinar el alta y las pruebas del `sandbox` real con PUI.

No describe como programar el servicio.
Describe que tiene que gestionar la empresa y que informacion debe entregarle al equipo tecnico.

## Que ya esta cubierto por el equipo tecnico

El equipo tecnico ya tiene preparado:

- el servicio webhook en Python
- endpoints requeridos por PUI
- entorno local de desarrollo
- entorno `sandbox` reproducible con Docker
- prueba tecnica local de `/login` y `/activar-reporte-prueba`
- simulacion del core para desarrollo

## Que tiene que hacer la empresa

La empresa debe gestionar cuatro frentes:

1. Alta institucional ante PUI.
2. Infraestructura publica para `sandbox`.
3. Credenciales y datos oficiales.
4. Coordinacion operativa para pruebas.

## 1. Alta institucional ante PUI

La empresa debe proporcionar o gestionar:

- representante legal que realizara el tramite
- acceso a Llave MX del representante legal
- e.Firma vigente de la persona moral
- RFC con homoclave de la empresa
- razon social exacta de la empresa
- nombre comercial y giro, si el portal lo solicita

Sin esto no se puede hacer el alta oficial del `sandbox`.

## 2. Infraestructura publica para sandbox

La empresa debe definir y entregar:

- dominio o subdominio para `sandbox`
- URL publica HTTPS del webhook
- IP publica que se registrara o pondra en whitelist
- responsable interno de red/infraestructura
- mecanismo de TLS

Ejemplos validos:

- `https://sandbox-pui.empresa.com`
- `https://api-sandbox.empresa.com/pui`

## 3. Credenciales y datos que la empresa debe entregar al equipo tecnico

El equipo tecnico necesita estos datos para configurar el entorno real:

### Datos institucionales

- RFC con homoclave real de la empresa
- razon social exacta
- nombre del representante legal
- correo del contacto operativo
- telefono del contacto operativo

### Datos de sandbox PUI

- credenciales oficiales que PUI entregue para pruebas
- password o clave que PUI usara contra nuestro `POST /login`
- `institucion_id` oficial a usar con PUI
- URL oficial de PUI para `sandbox`, si difiere de la documentada
- confirmacion de si `PUI_OUTBOUND_ENABLED` ya puede activarse o no

### Datos de infraestructura

- `PUBLIC_BASE_URL` real de `sandbox`
- IP publica registrada
- credenciales o acceso del servidor donde se desplegara el `sandbox`
- base de datos disponible para `sandbox`
- si habra reverse proxy corporativo, balanceador o WAF

## 4. Decisiones que la empresa debe tomar

La empresa debe decidir y comunicar:

- quien sera el owner del alta en PUI
- quien aprueba uso de dominio/IP de `sandbox`
- quien entrega y resguarda las credenciales
- quien valida funcionalmente la prueba de webhook
- quien sera el contacto con PUI o SEGOB si algo falla

## Checklist de informacion que el equipo tecnico debe recibir

Antes de intentar el `sandbox` real, la empresa debe entregar:

- RFC real con homoclave
- nombre o razon social oficial
- `PUBLIC_BASE_URL` real
- IP publica real
- password real para `POST /login`
- credenciales de `sandbox` para consumir PUI
- confirmacion de que el alta institucional en Llave MX ya esta hecha o en proceso
- confirmacion de que se puede publicar el webhook en Internet

## Entregables concretos que puede pedir el desarrollador

Para evitar ambiguedad, el desarrollador debe pedir esto literalmente:

1. RFC con homoclave de la empresa.
2. URL publica HTTPS exacta del `sandbox`.
3. IP publica exacta del `sandbox`.
4. Password real que PUI usara para autenticarse contra `/login`.
5. Credenciales de salida hacia PUI para `sandbox`.
6. Confirmacion de si ya se hizo el alta por Llave MX y con que folio.
7. Confirmacion del responsable de infraestructura para DNS/TLS/firewall.

## Lo que NO debe entregar la empresa al desarrollador si no es necesario

- e.Firma completa sin control administrativo
- acceso personal del representante legal a Llave MX
- secretos de produccion cuando solo se esta trabajando `sandbox`

Lo correcto es que la empresa administre esos accesos y solo comparta con desarrollo lo estrictamente necesario para la configuracion tecnica.

## Flujo recomendado con la empresa

1. El equipo tecnico valida todo localmente.
2. La empresa entrega RFC, URL, IP y responsables.
3. La empresa hace o confirma el alta institucional en PUI.
4. Infraestructura publica el `sandbox`.
5. Se cargan credenciales reales de `sandbox`.
6. Se ejecuta `scripts/sandbox_smoke_test.sh`.
7. Se realiza `activar-reporte-prueba` contra la URL publica.
8. Si la prueba pasa, se agenda la validacion oficial con PUI.

## Formato sugerido para pedir la informacion

Se puede pedir en una sola tabla o correo con estos campos:

- RFC con homoclave:
- Razon social:
- Nombre del representante legal:
- Correo del contacto operativo:
- Telefono del contacto operativo:
- URL publica HTTPS de sandbox:
- IP publica de sandbox:
- Password para endpoint `/login`:
- Credenciales outbound de sandbox:
- Estado del alta en Llave MX:
- Folio o referencia de inscripcion:
- Responsable de infraestructura:
- Responsable de cumplimiento/operacion:

## Referencias

- `docs/pui/10-despliegue-ambientes.md`
- `docs/pui/11-playbook-sandbox.md`
- `docs/pui/12-prueba-webhook.md`
