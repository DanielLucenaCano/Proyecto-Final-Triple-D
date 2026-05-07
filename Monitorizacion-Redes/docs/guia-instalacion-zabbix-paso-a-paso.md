# Guía Paso a Paso de Instalación y Configuración de Zabbix

## Objetivo

Desplegar **Zabbix Server**, frontend web y agente local en una máquina virtual **Ubuntu Server 24.04 LTS**, con **MariaDB** y **Apache**, dejando la plataforma lista para empezar a monitorizar.

## Alcance

- Sistema operativo de referencia: `Ubuntu Server 24.04 LTS`
- Herramienta: `Zabbix 7.4`
- Base de datos: `MariaDB`
- Servidor web: `Apache`
- Agente: `zabbix-agent`

## Nota Operativa

Si la VM usa **Debian 12** en lugar de Ubuntu 24.04, el flujo es el mismo, pero debes sustituir el paquete del repositorio oficial de Ubuntu por el paquete equivalente de Debian en la web oficial de Zabbix.

## Fase 0. Datos que Debes Definir Antes de Empezar

Define estos valores y utilízalos de forma consistente:

- `IP_VM`: IP de la máquina virtual
- `DB_NAME`: `zabbix`
- `DB_USER`: `zabbix`
- `DB_PASS`: clave de base de datos
- `ZBX_HOSTNAME`: nombre del servidor Zabbix

Ejemplo:

```bash
IP_VM=192.168.56.20
DB_NAME=zabbix
DB_USER=zabbix
DB_PASS=ZabbixDB2026!
ZBX_HOSTNAME=zabbix-server
```

## Fase 1. Preparar el Sistema

### 1. Actualizar el sistema

```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Instalar dependencias base

```bash
sudo apt install -y wget curl gnupg lsb-release ca-certificates software-properties-common
```

### 3. Verificar la IP de la VM

```bash
ip a
```

### 4. Fijar el nombre del equipo

```bash
sudo hostnamectl set-hostname zabbix-server
```

### 5. Validar resolución local

```bash
hostnamectl
cat /etc/hosts
```

### Evidencias a Capturar

- Salida de `hostnamectl`
- Salida de `ip a`

## Fase 2. Instalar MariaDB y Apache

### 1. Instalar base de datos y servidor web

```bash
sudo apt install -y mariadb-server apache2
```

### 2. Arrancar y habilitar servicios

```bash
sudo systemctl enable --now mariadb apache2
```

### 3. Verificar estado

```bash
sudo systemctl status mariadb --no-pager
sudo systemctl status apache2 --no-pager
```

### 4. Endurecer MariaDB

```bash
sudo mysql_secure_installation
```

Recomendación de respuesta:

- `Set root password`: según criterio del laboratorio
- `Remove anonymous users`: `Y`
- `Disallow root login remotely`: `Y`
- `Remove test database`: `Y`
- `Reload privilege tables`: `Y`

### Evidencias a Capturar

- Salida de estado de `mariadb`
- Salida de estado de `apache2`

## Fase 3. Configurar el Repositorio Oficial de Zabbix

### 1. Descargar el paquete oficial para Ubuntu 24.04

```bash
wget https://repo.zabbix.com/zabbix/7.4/release/ubuntu/pool/main/z/zabbix-release/zabbix-release_latest_7.4+ubuntu24.04_all.deb
```

### 2. Instalar el paquete

```bash
sudo dpkg -i zabbix-release_latest_7.4+ubuntu24.04_all.deb
```

### 3. Actualizar índice de paquetes

```bash
sudo apt update
```

### 4. Validar que el repositorio ha quedado operativo

```bash
apt policy | grep -i zabbix -A 3
```

### Evidencias a Capturar

- Salida de `apt policy | grep -i zabbix -A 3`

## Fase 4. Instalar Zabbix Server, Frontend y Agente

### 1. Instalar paquetes principales

```bash
sudo apt install -y zabbix-server-mysql zabbix-frontend-php zabbix-apache-conf zabbix-sql-scripts zabbix-agent
```

### 2. Verificar instalación de paquetes

```bash
dpkg -l | grep -E 'zabbix-server|zabbix-frontend|zabbix-apache-conf|zabbix-sql-scripts|zabbix-agent'
```

### Evidencias a Capturar

- Salida de `dpkg -l | grep zabbix`

## Fase 5. Crear la Base de Datos de Zabbix

### 1. Entrar en MariaDB como root

```bash
sudo mysql
```

### 2. Ejecutar sentencias SQL

```sql
create database zabbix character set utf8mb4 collate utf8mb4_bin;
create user 'zabbix'@'localhost' identified by 'ClaveSeguraZabbixDB';
grant all privileges on zabbix.* to 'zabbix'@'localhost';
set global log_bin_trust_function_creators = 1;
flush privileges;
quit;
```

Sustituye `ClaveSeguraZabbixDB` por el valor real definido en `DB_PASS`.

### 3. Importar el esquema inicial de Zabbix

```bash
zcat /usr/share/zabbix-sql-scripts/mysql/server.sql.gz | mysql --default-character-set=utf8mb4 -uzabbix -p zabbix
```

### 4. Desactivar el ajuste temporal de funciones

```bash
sudo mysql -e "set global log_bin_trust_function_creators = 0;"
```

### 5. Validar que la base de datos contiene tablas

```bash
mysql -uzabbix -p -e "use zabbix; show tables;" | head
```

### Evidencias a Capturar

- Salida del comando de importación
- Salida de `show tables`

## Fase 6. Configurar Zabbix Server

### 1. Editar el fichero del servidor

```bash
sudo nano /etc/zabbix/zabbix_server.conf
```

### 2. Ajustar parámetros mínimos

```ini
DBName=zabbix
DBUser=zabbix
DBPassword=ClaveSeguraZabbixDB
```

### 3. Validar configuración

```bash
grep -E '^(DBName|DBUser|DBPassword)=' /etc/zabbix/zabbix_server.conf
```

### Evidencias a Capturar

- Salida del `grep` de parámetros de base de datos

## Fase 7. Ajustar PHP y Apache

### 1. Revisar configuración del frontend

```bash
sudo nano /etc/zabbix/apache.conf
```

### 2. Verificar zona horaria

```apache
php_value date.timezone Europe/Madrid
```

### 3. Reiniciar Apache

```bash
sudo systemctl restart apache2
```

### 4. Verificar sintaxis y estado

```bash
sudo apache2ctl configtest
sudo systemctl status apache2 --no-pager
```

### Evidencias a Capturar

- Salida de `apache2ctl configtest`
- Salida de estado de `apache2`

## Fase 8. Arrancar y Habilitar los Servicios de Zabbix

### 1. Habilitar y arrancar servicios

```bash
sudo systemctl enable --now zabbix-server zabbix-agent apache2
```

### 2. Verificar estado

```bash
sudo systemctl status zabbix-server --no-pager
sudo systemctl status zabbix-agent --no-pager
sudo systemctl status apache2 --no-pager
```

### 3. Verificar puertos publicados

```bash
ss -lntp | grep -E '10051|80'
```

### 4. Revisar log si hay fallo en Zabbix Server

```bash
sudo tail -n 50 /var/log/zabbix/zabbix_server.log
```

### Evidencias a Capturar

- Estado de `zabbix-server`
- Estado de `zabbix-agent`
- Estado de `apache2`
- Salida de `ss -lntp`

## Fase 9. Acceso Web y Asistente Inicial

### 1. Abrir en navegador

```text
http://IP_DE_LA_VM/zabbix
```

### 2. Completar el asistente inicial

Configura estos valores:

- Tipo de base de datos: `MySQL`
- Host de base de datos: `localhost`
- Puerto: `0` o `3306`
- Nombre de base de datos: `zabbix`
- Usuario: `zabbix`
- Password: la definida en `DB_PASS`
- Zabbix server host: `localhost`
- Zabbix server port: `10051`
- Name: `Zabbix Lab`

### 3. Iniciar sesión

Credenciales por defecto:

- Usuario: `Admin`
- Password: `zabbix`

### 4. Cambiar la contraseña de `Admin`

Esto es obligatorio desde el punto de vista operativo.

### Evidencias a Capturar

- Captura del asistente
- Captura del dashboard inicial
- Evidencia del cambio de password

## Fase 10. Configuración Básica Post-Instalación

### 1. Verificar el host local desde la interfaz

Ruta recomendada:

```text
Data collection -> Hosts
```

### 2. Comprobar que el host `Zabbix server` está habilitado

### 3. Verificar que el agente local reporta métricas

Ruta recomendada:

```text
Monitoring -> Latest data
```

### 4. Validar servicios desde consola

```bash
sudo systemctl is-active zabbix-server
sudo systemctl is-active zabbix-agent
```

### 5. Revisar logs finales

```bash
sudo tail -n 30 /var/log/zabbix/zabbix_server.log
sudo tail -n 30 /var/log/zabbix/zabbix_agentd.log
```

### Evidencias a Capturar

- Captura de `Latest data`
- Logs finales sin errores críticos

## Fase 11. Validación Mínima de la Instalación

La instalación debe considerarse correcta solo si se cumple todo lo siguiente:

- `MariaDB` activo
- `Apache` activo
- `zabbix-server` activo
- `zabbix-agent` activo
- Puerto `80` en escucha
- Puerto `10051` en escucha
- Frontend accesible por navegador
- Login funcional con usuario `Admin`
- Host local visible en Zabbix

## Bloque de Comandos Consolidado

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y wget curl gnupg lsb-release ca-certificates software-properties-common
sudo apt install -y mariadb-server apache2
sudo systemctl enable --now mariadb apache2
wget https://repo.zabbix.com/zabbix/7.4/release/ubuntu/pool/main/z/zabbix-release/zabbix-release_latest_7.4+ubuntu24.04_all.deb
sudo dpkg -i zabbix-release_latest_7.4+ubuntu24.04_all.deb
sudo apt update
sudo apt install -y zabbix-server-mysql zabbix-frontend-php zabbix-apache-conf zabbix-sql-scripts zabbix-agent
sudo mysql -e "create database zabbix character set utf8mb4 collate utf8mb4_bin;"
sudo mysql -e "create user 'zabbix'@'localhost' identified by 'ClaveSeguraZabbixDB';"
sudo mysql -e "grant all privileges on zabbix.* to 'zabbix'@'localhost';"
sudo mysql -e "set global log_bin_trust_function_creators = 1;"
sudo mysql -e "flush privileges;"
zcat /usr/share/zabbix-sql-scripts/mysql/server.sql.gz | mysql --default-character-set=utf8mb4 -uzabbix -p zabbix
sudo mysql -e "set global log_bin_trust_function_creators = 0;"
sudo sed -i 's/^# DBPassword=/DBPassword=ClaveSeguraZabbixDB/' /etc/zabbix/zabbix_server.conf
sudo sed -i 's#php_value date.timezone Europe/Riga#php_value date.timezone Europe/Madrid#' /etc/zabbix/apache.conf
sudo systemctl restart apache2
sudo systemctl enable --now zabbix-server zabbix-agent apache2
```

## Incidencias Frecuentes

### 1. Error: `Unable to locate package zabbix-apache-conf` o `zabbix-sql-scripts`

Causa habitual: repositorio oficial mal instalado o paquete de otra versión de Ubuntu/Debian.

Acción:

```bash
sudo apt update
```

Revisa además que el paquete `.deb` descargado corresponda a la versión correcta del sistema operativo.

### 2. Error: `server.sql.gz: No such file or directory`

Causa habitual: no se instaló `zabbix-sql-scripts`.

Acción:

```bash
sudo apt install -y zabbix-sql-scripts
```

### 3. Error de acceso a base de datos desde Zabbix Server

Causa habitual: contraseña incorrecta en `/etc/zabbix/zabbix_server.conf`.

Acción:

```bash
sudo systemctl restart zabbix-server
```

Corrige antes el valor de `DBPassword`.

### 4. La web carga pero el asistente falla en prerrequisitos PHP

Causa habitual: timezone o parámetros PHP no alineados.

Acción:

Revisa `/etc/zabbix/apache.conf` y reinicia Apache.

## Resultado Final Esperado

La VM debe exponer el frontend web de Zabbix, con backend funcional, agente local activo y base de datos inicializada, de modo que en la siguiente fase se puedan registrar hosts adicionales, definir triggers y construir dashboards.
