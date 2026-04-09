# Configurador de Hosting (Backend)

Backend base para una aplicación de configuración de servidores virtuales usando **Django + PostgreSQL**.

## Estructura del proyecto

```text
.
├── manage.py
├── requirements.txt
├── .env.example
├── hosting_configurator/
│   └── config/
│       ├── settings.py
│       ├── urls.py
│       ├── wsgi.py
│       └── asgi.py
└── apps/
    ├── accounts/
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   └── services/
    │       └── auth_service.py
    ├── servers/
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   └── services/
    │       └── server_service.py
    └── pricing/
        └── services/
            └── pricing_service.py
```

## Modelo de datos

- `User` (custom user): datos de autenticación + perfil básico.
- `Server`: instancia virtual asociada al usuario.
- `ServerConfiguration`: recursos técnicos y precio mensual.
- `OptionalServices`: servicios extra configurables.

## Endpoints API (sin frontend)

### Accounts
- `POST /api/accounts/register/`
- `POST /api/accounts/login/`
- `GET /api/accounts/profile/` (requiere sesión)

### Servers
- `GET /api/servers/` (lista)
- `POST /api/servers/` (crear servidor + configuración)
- `PATCH /api/servers/<server_id>/` (editar)
- `POST /api/servers/<server_id>/start/`
- `POST /api/servers/<server_id>/stop/`
- `POST /api/servers/configurator/price/` (simulación de precio)

## Reglas de pricing implementadas

- vCPU: `4€/core`
- RAM: `2.5€/GB`
- SSD: `0.08€/GB`
- HDD: `0.025€/GB`
- Bandwidth: `2€/100 Mbps`
- Windows Server: `15€/mes`
- IP estática: `3€/mes`
- Backup: `20%` del precio base
- Firewall: `2€/mes`
- Panel de control: `12€/mes`

## Configuración rápida

1. Crear entorno virtual e instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Configurar variables usando `.env.example`.
3. Ejecutar migraciones:
   ```bash
   python manage.py migrate
   ```
4. Levantar servidor:
   ```bash
   python manage.py runserver
   ```
