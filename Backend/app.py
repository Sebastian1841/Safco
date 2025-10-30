from flask import Flask, jsonify
from flask_cors import CORS
from Ejemplo import ThingsBoardSimple 

app = Flask(__name__)
CORS(app)

tb = ThingsBoardSimple()

@app.route("/datos")
def datos():
    fecha_inicio = "2025-10-01"
    fecha_fin = "2025-10-28"
    
    datos_tb = tb.consultar_por_fechas(fecha_inicio, fecha_fin)
    
    resultado = []

    if datos_tb.get("codigo1"):
        litros = datos_tb["codigo1"].get("Litros_total", [])
        ibuttons = datos_tb["codigo1"].get("iButton_total", [])
        for i in range(len(litros)):
            resultado.append({
                "fecha": litros[i]["ts"],
                "litros": litros[i]["value"],
                "ibutton": ibuttons[i]["value"] if i < len(ibuttons) else "N/A",
                "dispositivo_id": 1,
                "dato1": "Codigo1",
                "dato2": "En Proceso"
            })

    if datos_tb.get("codigo2"):
        pulsos = datos_tb["codigo2"].get("pulsos_total", [])
        ibuttons = datos_tb["codigo2"].get("ibutton", [])
        for i in range(len(pulsos)):
            litros_calc = round(float(pulsos[i]['value']) / 19.86, 2)
            resultado.append({
                "fecha": pulsos[i]["ts"],
                "litros": litros_calc,
                "ibutton": ibuttons[i]["value"] if i < len(ibuttons) else "N/A",
                "dispositivo_id": 2,
                "dato1": "Codigo2",
                "dato2": "Pendiente"
            })

    return jsonify(resultado)

# -----------------------------
# Endpoint nuevo: solo dispositivos con datos
# -----------------------------
@app.route("/dispositivos")
def dispositivos():
    datos_tb = tb.consultar_por_fechas("2025-10-01", "2025-10-28")
    ids_unicos = set()

    if datos_tb.get("codigo1"):
        ids_unicos.add(1)
    if datos_tb.get("codigo2"):
        ids_unicos.add(2)
        
    nombres_custom = {
        1: "Tanque Fijo",
        2: "Tanque Movil"
    }

    dispositivos_list = [
        {"id": did, "nombre": nombres_custom.get(did, f"Dispositivo {did}")}
        for did in ids_unicos
    ]
    return jsonify(dispositivos_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
