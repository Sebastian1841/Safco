
# ThingsBoard SAFCO EJEMPLO

Una librería Python simple para consultar datos de telemetría desde ThingsBoard por rango de fechas.

## 📋 Descripción

Esta librería permite consultar datos de dos dispositivos diferentes en ThingsBoard, obteniendo las variables de telemetría por rangos de fechas específicos. Es ideal para generar reportes de consumo de combustible.

## 🚀 Características

- **Autenticación automática** con ThingsBoard
- **Consulta por rangos de fechas** flexibles
- **Dos dispositivos soportados**: FIJO y Móvil
- **Conversión automática** de pulsos a litros
- **Interfaz interactiva** para consultas manuales
- **Manejo de errores** robusto

## 🔧 Instalación

### Requisitos
```bash
pip install requests

## 🔧 Configuración

- **El código incluye toda la configuración necesaria:**
 -  # Configuración de conexión
    url = "https://sinergychile.cl"
    usuario = "remisrea@cog.cl"
    password = "nuevavida2050"

- **# Dispositivos**
    dispositivo1 = "52906fe0-a5d5-11f0-9dd9-bb6adf6472c1"  # FIJO
    dispositivo2 = "39dd8c70-6cb0-11f0-9c9f-ebe52b51bbe5"  # Móvil

 ## 🔧  Variables Obtenidas

 Dispositivo FIJO

    Litros_total - Litros de combustible consumidos

    iButton_total - Identificador del usuario (iButton)

Dispositivo Móvil

    pulsos_total - Pulsos del contador de combustible

    ibutton - Identificador del usuario (iButton)

Nota: Los pulsos se convierten automáticamente a litros usando el factor 19.86
🛠️ Uso Básico
Ejemplo 1: Uso Directo

from thingsboard_client import ThingsBoardSimple

# Crear instancia del cliente
tb = ThingsBoardSimple()

# Consultar un día específico
datos = tb.consultar_por_fechas("2024-01-15", "2024-01-15")

# Mostrar resultados
tb.mostrar_resultados(datos)

Ejemplo 2: Consultar Rango Personalizado

# Consultar una semana
datos = tb.consultar_por_fechas("2024-01-10", "2024-01-16")

# Consultar un mes completo
datos = tb.consultar_por_fechas("2024-01-01", "2024-01-31")

Ejemplo 3: Uso Interactivo
# Ejecutar consulta interactiva
tb.consulta_interactiva()

📝 Métodos Principales
consultar_por_fechas(fecha_inicio, fecha_fin)

Consulta datos de ambos dispositivos en el rango especificado.

Parámetros:

    fecha_inicio (str): Fecha inicial en formato "YYYY-MM-DD"

    fecha_fin (str): Fecha final en formato "YYYY-MM-DD"

Retorna:

    dict: Diccionario con datos de ambos dispositivos

mostrar_resultados(datos)

Muestra los resultados de forma legible en la consola.

Parámetros:

    datos (dict): Datos obtenidos de consultar_por_fechas

🎯 Ejemplos de Consulta
Consultar un Solo Día

datos = tb.consultar_por_fechas("2024-01-15", "2024-01-15")

Consultar Varios Días

# Una semana
datos = tb.consultar_por_fechas("2024-01-10", "2024-01-16")

# 15 días
datos = tb.consultar_por_fechas("2024-01-01", "2024-01-15")

# Mes completo
datos = tb.consultar_por_fechas("2024-01-01", "2024-01-31")

 Salida de Ejemplo

 Consultando del 2024-01-15 al 2024-01-15
==================================================

🔹 FIJO - LITROS TOTALES
   Registros encontrados: 8
   2024-01-15 10:30:00 - Litros: 45.2 - iButton: 0146FF1901000033
   2024-01-15 14:15:00 - Litros: 32.1 - iButton: 016E818A01000082

🔹 Móvil - PULSOS
   Registros encontrados: 5
   2024-01-15 09:45:00 - Pulsos: 895 - Litros: 45.07 - iButton: 01C44B1A0100006F

   🔄 Flujo de Trabajo

    Autenticación: Login automático con las credenciales configuradas

    Conversión de fechas: Transforma fechas a timestamps de ThingsBoard

    Consulta API: Obtiene datos de telemetría de ambos dispositivos

    Procesamiento: Convierte pulsos a litros y formatea resultados

    Presentación: Muestra datos de forma legible al usuario


# SAFCO – Backend (Flask + SQLAlchemy + PostgreSQL)

API Flask que integra datos de ThingsBoard y la base de datos local para exponer registros de combustible y referencias.

## Arranque rápido

- Con Docker (recomendado)
  1. Desde la raíz del repo: `docker compose up --build`
  2. Backend: http://localhost:5000
  3. Base de datos: Postgres expuesto en host `localhost:5433` (contenedor `5432`)

- Local (Python 3.11)
  1. `cd Backend`
  2. (opcional) crear venv
  3. `pip install -r requirements.txt`
  4. Exportar `DATABASE_URL` (por ejemplo `postgresql://safcouser:safcopassword@localhost:5433/safcodb`)
  5. `python app.py`

## Variables de entorno

- `DATABASE_URL` – cadena de conexión a PostgreSQL.
- `THINGSBOARD_HOST` – URL base de ThingsBoard.

En docker-compose ya se configuran:

DATABASE_URL=postgresql://safcouser:safcopassword@db:5432/safcodb
THINGSBOARD_HOST=http://localhost:8080


## Endpoints principales

- `GET /datos`
  - Params: `fecha_inicio` (YYYY-MM-DD), `fecha_fin` (YYYY-MM-DD)
  - Fusiona datos de TB con la DB. Convierte `fecha` a hora de Chile (ISO con offset) para el cliente.
- `POST /datos` – inserción de registros manuales (ver campos del modelo `RegistroLitro`).
- `PATCH /datos/<id>` – actualización puntual (ej: `dato1_id`, `dato2_id`).
- `GET /dato1`, `POST /dato1`, `PUT/DELETE /dato1/<id>` – CRUD referencias Dato1.
- `GET /dato2`, `POST /dato2`, `PUT/DELETE /dato2/<id>` – CRUD referencias Dato2.
- `GET /litros_control`, `POST /litros_control`, `PUT/DELETE /litros_control/<id>` – control de litros por día/dispositivo.
- `GET /dispositivos` – IDs detectados en TB con nombres amigables.

## Modelos

- `RegistroLitro`: `id`, `fecha` (naive UTC), `litros`, `ibutton`, `dispositivo_id`, `dato1_id`, `dato2_id`.
  - Unicidad: `(fecha, dispositivo_id)`.
- `Dato1` / `Dato2`: referencias simples `id`, `nombre`.
- `LitrosControl`: `fecha`, `dispositivo`, `litros_inicio`, `litros_final`, `diferencia_manual`.

## Zona horaria

- La fecha se almacena como NAIVE en UTC. Al serializar al cliente se hace:
  1) `fecha.replace(tzinfo=timezone.utc)`
  2) `.astimezone(CHILE_TZ)` donde `CHILE_TZ` se define con `timedelta(hours=-3)` (ajustar a -4 en invierno)
  3) `.isoformat()`

## Persistencia

- `db.create_all()` crea tablas si no existen al iniciar la app.
- Volumen de Postgres en docker-compose: `pgdata`.

## Requisitos y notas

- Python 3.11, Flask, Flask-CORS, Flask-SQLAlchemy, psycopg2-binary.
- Si compilas local y psycopg2 falla, usa Docker o instala dependencias de libpq.
- CORS está habilitado para desarrollo; restringir orígenes en producción.

## Solución de problemas

- `409 Conflicto` al insertar en `/datos`: existe un registro con el mismo `(fecha, dispositivo_id)`.
- Desfase de fechas: el cliente opera con días locales; si prefieres UTC en cliente ajusta conversión en `app.py` o normaliza en el frontend.
- Conectividad DB en host: usa puerto `5433` (mapeado a `5432` del contenedor).

## Estructura

- `Backend/app.py` – app Flask, modelos, endpoints
- `Backend/Ejemplo.py` – integración ThingsBoard (stub/implementación)
- `Backend/requirements.txt` – dependencias
- `Backend/Dockerfile` – imagen de la API
```