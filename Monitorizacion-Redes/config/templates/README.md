# config/templates/

Plantillas de Zabbix (exportadas o de elaboración propia) reutilizables en
el laboratorio.

## Contenido

- `plantilla-laboratorio-base.yaml.example`: plantilla de partida que añade
  triggers de umbral (CPU, memoria, disco, severidades warning/critical)
  sobre los items de la plantilla oficial **"Linux by Zabbix agent"**.
  Los valores de umbral son **provisionales**: deben confirmarse en
  `docs/politicas-monitorizacion.md` y validarse con datos reales antes de
  considerarla definitiva (ver `docs/validacion-pruebas.md`).

## Recomendación de uso

1. Vincula primero la plantilla oficial **"Linux by Zabbix agent"** al host
   (ya viene incluida en Zabbix; cubre items base de CPU, memoria y disco).
2. Importa `plantilla-laboratorio-base.yaml.example` (cambia su extensión a
   `.yaml` si tu instancia de Zabbix lo exige) desde
   **Data collection -> Templates -> Import**.
3. Vincula también esta plantilla al host para activar los triggers de umbral.
4. Ajusta los valores de los triggers según el comportamiento real observado
   y documenta la decisión final en `docs/politicas-monitorizacion.md`.
5. Cuando exportes plantillas ya validadas desde el frontend
   (**Data collection -> Templates -> Export**), guárdalas aquí con un
   nombre descriptivo y sin el sufijo `.example`.
