# Hosting - Configurador simple en PHP + MySQL

Proyecto básico (sin frameworks) para aprender a:

- Registrar usuarios
- Iniciar sesión
- Configurar servidores
- Calcular precios mensuales
- Simular acciones de servidor (iniciar/detener)

---

## 1) Requisitos

- PHP 8.0+
- MySQL 5.7+ o MariaDB 10+
- Servidor local (XAMPP, Laragon, WAMP, MAMP o similar)

---

## 2) Estructura del proyecto

```
Hosting/
├── index.php
├── login.php
├── register.php
├── dashboard.php
├── config.php
├── functions.php
├── style.css
├── script.js
├── database.sql
└── README.md
```

---

## 3) Instalación rápida

1. Copia la carpeta `Hosting` dentro de tu servidor local (por ejemplo en `htdocs`).
2. Crea una base de datos importando el archivo `database.sql`.
3. Abre `config.php` y ajusta tus credenciales de MySQL:
   - `$host`
   - `$dbname`
   - `$user`
   - `$pass`
4. Abre en el navegador:
   - `http://localhost/Hosting/index.php`

---

## 4) Configuración de base de datos

El archivo `database.sql` crea:

- Base de datos: `hosting_db`
- Tabla `users`:
  - `id`, `nombre`, `email`, `password`, `creado_en`
- Tabla `servers`:
  - Recursos del servidor
  - Extras contratados
  - `precio_base`, `precio_total`
  - Estado simulado: `activo` / `detenido`

> Si ya tienes la base creada, puedes editar `database.sql` para omitir la línea `CREATE DATABASE`.

---

## 5) Reglas de precios (mensual)

- vCPU: **4€ / core**
- RAM: **2.5€ / GB**
- SSD: **0.08€ / GB**
- HDD: **0.025€ / GB**
- Bandwidth: **2€ / cada 100 Mbps**
- Windows Server: **+15€**
- IP estática: **+3€**
- Backup: **+20% del precio base**
- Firewall: **+2€**
- Panel de control: **+12€**

El cálculo se hace:

- En backend: `functions.php` (`calcularPrecio`)
- En frontend: `script.js` (estimación en vivo)

---

## 6) Flujo de uso

1. Entrar a `register.php` y crear un usuario.
2. Ir a `login.php` e iniciar sesión.
3. En `dashboard.php`:
   - Crear un servidor con recursos y extras.
   - Ver precio estimado en tiempo real.
   - Guardar servidor.
   - Iniciar/detener servidores (simulado).

---

## 7) Notas de seguridad (nivel básico)

Este proyecto es educativo y simple. Incluye:

- Contraseñas hasheadas con `password_hash`
- Verificación con `password_verify`
- Consultas preparadas con `mysqli->prepare`
- Control básico de sesión

Mejoras recomendadas para producción:

- Validaciones más estrictas en servidor
- Protección CSRF
- Rate limit de login
- Logs y manejo de errores avanzado
- Separación por capas (controladores/servicios)

---

## 8) Troubleshooting

### Error de conexión a MySQL
Revisa `config.php` y confirma usuario, contraseña, host y nombre de base.

### Página en blanco
Activa errores temporalmente en PHP para depurar:

```php
ini_set('display_errors', 1);
error_reporting(E_ALL);
```

### No carga estilos o JS
Verifica que `style.css` y `script.js` estén en la misma carpeta que `dashboard.php`.

---

## 9) Licencia

Uso libre con fines educativos.
