# Instalación

## Alcance

La instalación objetivo del proyecto se basa en **Zabbix 7.4**, con **MariaDB/MySQL**, **Apache** y **agente local**, desplegado en una máquina virtual Linux tipo Ubuntu/Debian.

## Documento operativo principal

La guía paso a paso de ejecución se ha documentado en:

- [guia-instalacion-zabbix-paso-a-paso.md](/mnt/c/Users/G513/OneDrive%20-%20Sa%20Palomera/Documentos/Codex/Zabbix/Monitorizacion-Redes/docs/guia-instalacion-zabbix-paso-a-paso.md)

## Resultado esperado

Al finalizar la instalación deben quedar validados los siguientes puntos:

- Repositorio oficial de Zabbix configurado.
- Base de datos creada e inicializada.
- Servicio `zabbix-server` arrancado.
- Servicio `zabbix-agent` arrancado.
- Apache operativo.
- Asistente web accesible en `http://IP_DE_LA_VM/zabbix`.

## Evidencias mínimas a capturar

- Salida de `systemctl status zabbix-server --no-pager`.
- Salida de `systemctl status zabbix-agent --no-pager`.
- Salida de `systemctl status apache2 --no-pager`.
- Captura de la pantalla de login o del asistente inicial de Zabbix.
- Salida de validación de puerto con `ss -lntp | grep -E '10051|80'`.
