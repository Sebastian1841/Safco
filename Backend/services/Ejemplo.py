import requests
from datetime import datetime, timedelta
import json

class ThingsBoardSimple:
    def __init__(self):
        # Configuración de conexión
        self.url = "https://sinergychile.cl"
        self.usuario = "remisrea@cog.cl"
        self.password = "nuevavida2050"
        self.token = None
        
        # Dispositivos
        self.dispositivo1 = "52906fe0-a5d5-11f0-9dd9-bb6adf6472c1" 
        self.dispositivo2 = "39dd8c70-6cb0-11f0-9c9f-ebe52b51bbe5" 
        
        # Variables a obtener
        self.variables_codigo1 = ["Litros_total", "iButton_total"]
        self.variables_codigo2 = ["pulsos_total", "ibutton"]
        
        # Autenticación automática
        self._login()
    
    def _login(self):
        """Iniciar sesión en ThingsBoard y obtener token"""
        try:
            respuesta = requests.post(
                f"{self.url}/api/auth/login",
                json={"username": self.usuario, "password": self.password},
                headers={"Content-Type": "application/json"}
            )
            
            if respuesta.status_code == 200:
                datos = respuesta.json()
                self.token = datos.get('token')
                print("Login exitoso")
            else:
                print(" Error en login")
                
        except Exception as e:
            print(f" Error de conexión: {e}")
    
    def _fecha_a_timestamp(self, fecha_str):
        """Convertir fecha 'YYYY-MM-DD' a timestamp en milisegundos"""
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        return int(fecha.timestamp() * 1000)
    
    def obtener_datos(self, dispositivo, variables, fecha_inicio, fecha_fin):
        """Obtener datos de telemetría por rango de fechas"""
        if not self.token:
            print(" No hay token de autenticación")
            return None
        
        # Convertir fechas a timestamps
        inicio_ts = self._fecha_a_timestamp(fecha_inicio)
        fin_ts = self._fecha_a_timestamp(fecha_fin) + (23 * 60 * 60 * 1000)  # Hasta las 23:59
        
        # Unir variables en string
        variables_str = ",".join(variables)
        
        try:
            respuesta = requests.get(
                f"{self.url}/api/plugins/telemetry/DEVICE/{dispositivo}/values/timeseries",
                params={
                    "keys": variables_str,
                    "startTs": inicio_ts,
                    "endTs": fin_ts,
                    "limit": 10000,
                    "agg": "NONE"
                },
                headers={
                    "Content-Type": "application/json",
                    "X-Authorization": f"Bearer {self.token}"
                }
            )
            
            if respuesta.status_code == 200:
                return respuesta.json()
            else:
                print(f"Error al obtener datos: {respuesta.status_code}")
                return None
                
        except Exception as e:
            print(f" Error de conexión: {e}")
            return None
    
    def consultar_por_fechas(self, fecha_inicio, fecha_fin):
        """Consultar todas las variables por rango de fechas"""
        print(f"\nConsultando del {fecha_inicio} al {fecha_fin}")
        print("=" * 50)
        
        # Obtener datos del Código 1
        datos1 = self.obtener_datos(
            self.dispositivo1, 
            self.variables_codigo1, 
            fecha_inicio, 
            fecha_fin
        )
        
        # Obtener datos del Código 2
        datos2 = self.obtener_datos(
            self.dispositivo2, 
            self.variables_codigo2, 
            fecha_inicio, 
            fecha_fin
        )
        
        return {
            "codigo1": datos1,
            "codigo2": datos2
        }
    
    def mostrar_resultados(self, datos):
        """Mostrar resultados de forma legible"""
        
        # Procesar Código 1
        if datos["codigo1"]:
            litros = datos["codigo1"].get("Litros_total", [])
            ibuttons = datos["codigo1"].get("iButton_total", [])
            
            print("\n🔹 CÓDIGO 1 - LITROS TOTALES")
            print(f"   Registros encontrados: {len(litros)}")
            
            if litros:
                for i in range(min(3, len(litros))):  # Mostrar primeros 3
                    fecha = datetime.fromtimestamp(litros[i]['ts'] / 1000)
                    print(f"   {fecha} - Litros: {litros[i]['value']} - iButton: {ibuttons[i]['value'] if i < len(ibuttons) else 'N/A'}")
        
        # Procesar Código 2
        if datos["codigo2"]:
            pulsos = datos["codigo2"].get("pulsos_total", [])
            ibuttons = datos["codigo2"].get("ibutton", [])
            
            print("\n🔹 CÓDIGO 2 - PULSOS")
            print(f"   Registros encontrados: {len(pulsos)}")
            
            if pulsos:
                for i in range(min(3, len(pulsos))):  # Mostrar primeros 3
                    fecha = datetime.fromtimestamp(pulsos[i]['ts'] / 1000)
                    litros = round(float(pulsos[i]['value']) / 19.86, 2)
                    print(f"   {fecha} - Pulsos: {pulsos[i]['value']} - Litros: {litros} - iButton: {ibuttons[i]['value'] if i < len(ibuttons) else 'N/A'}")

# EJEMPLOS DE USO
def main():
    # Crear instancia
    tb = ThingsBoardSimple()
    
    if not tb.token:
        print("No se pudo conectar. Verifica credenciales.")
        return
    
    print("\n" + "="*60)
    print("CONSULTAS THINGSBOARD - EJEMPLOS PRÁCTICOS")
    print("="*60)
    
    # EJEMPLO 1: Consultar un día específico
    print("\n1. CONSULTAR UN DÍA ESPECÍFICO")
    datos = tb.consultar_por_fechas("2025-09-15", "2025-09-15")
    tb.mostrar_resultados(datos)
    
    # EJEMPLO 2: Consultar una semana
    print("\n2. CONSULTAR UNA SEMANA")
    datos = tb.consultar_por_fechas("2025-09-15", "2025-10-28")
    tb.mostrar_resultados(datos)
    
    # EJEMPLO 3: Consultar el mes completo
    print("\n3. CONSULTAR UN MES COMPLETO")
    datos = tb.consultar_por_fechas("2025-08-01", "2025-08-31")
    tb.mostrar_resultados(datos)
    
    # EJEMPLO 4: Consultar rango personalizado
    print("\n4. CONSULTAR RANGO PERSONALIZADO")
    datos = tb.consultar_por_fechas("2025-07-20", "2025-07-25")
    tb.mostrar_resultados(datos)

# Función para uso interactivo
def consulta_interactiva():
    """Permite al usuario ingresar fechas manualmente"""
    tb = ThingsBoardSimple()
    
    if not tb.token:
        return
    
    print("\nCONSULTA INTERACTIVA")
    print("Ingresa las fechas en formato YYYY-MM-DD")
    
    while True:
        try:
            fecha_inicio = input("\nFecha inicio (YYYY-MM-DD): ").strip()
            fecha_fin = input("Fecha fin (YYYY-MM-DD): ").strip()
            
            # Validar formato
            datetime.strptime(fecha_inicio, "%Y-%m-%d")
            datetime.strptime(fecha_fin, "%Y-%m-%d")
            
            print("\nConsultando datos...")
            datos = tb.consultar_por_fechas(fecha_inicio, fecha_fin)
            tb.mostrar_resultados(datos)
            
            continuar = input("\n¿Otra consulta? (s/n): ").lower()
            if continuar != 's':
                break
                
        except ValueError:
            print("Formato incorrecto. Usa YYYY-MM-DD")
        except KeyboardInterrupt:
            print("\n¡Hasta luego!")
            break

if __name__ == "__main__":
    # Ejecutar ejemplos
    main()
    
    # Ejecutar consulta interactiva
    consulta_interactiva()