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