# Playbook Sandbox

## Objetivo

Levantar una instancia reproducible del webhook de la empresa para pruebas oficiales con PUI.

## Previo al despliegue

- confirmar `PUBLIC_BASE_URL` real del sandbox
- confirmar IP publica que se registrara en PUI
- cargar credenciales de sandbox reales en un `.env.sandbox`
- reemplazar todos los valores `replace-*`
- confirmar que la empresa sera quien haga el alta en Llave MX

## Arranque recomendado con Docker

1. Crear archivo `.env.sandbox` a partir de `.env.sandbox.example`.
2. Ajustar:
   - `PUBLIC_BASE_URL`
   - `PUI_INBOUND_PASSWORD`
   - `PUI_OUTBOUND_INSTITUCION_ID`
   - `PUI_OUTBOUND_CLAVE`
   - `DATABASE_URL`
3. Levantar servicios:

```bash
docker compose --env-file .env.sandbox up --build
```

4. Verificar salud:

```bash
curl http://localhost:8000/health
```

## Antes de registrar el webhook

- `POST /login` responde 200
- `POST /activar-reporte-prueba` responde 200 con JWT valido
- TLS y dominio publico listos en el reverse proxy
- bitacoras habilitadas
- ambiente no usa secretos por defecto

## Reverse proxy

El contenedor expone el servicio en `8000`, pero PUI debe consumir una URL publica HTTPS de la empresa.

Se recomienda poner enfrente:

- Nginx
- Traefik
- balanceador administrado de nube

## No hacer en sandbox

- usar cuentas personales para la inscripcion oficial
- usar RFC ficticio
- dejar `PUI_OUTBOUND_ENABLED=true` sin credenciales reales
- reutilizar secretos de desarrollo
