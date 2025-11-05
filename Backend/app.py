from flask import Flask, jsonify, request
from flask_cors import CORS
# Suponiendo que Ejemplo.py contiene la clase ThingsBoardSimple
from Ejemplo import ThingsBoardSimple
from os import environ
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, UniqueConstraint
from sqlalchemy.exc import IntegrityError
from datetime import date, datetime, timedelta, timezone # <-- Se añade timezone y timedelta

app = Flask(__file__)
CORS(app)

# Configuración de PostgreSQL
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# --- CONFIGURACIÓN DE ZONA HORARIA CHILENA (SIN LIBRERÍAS EXTERNAS) ---
# Hemos fijado el offset a UTC-3 (Hora de Verano/Estándar de Chile).
# Si la hora chilena pasa a UTC-4 (invierno), solo necesita cambiar el valor a -4.
CHILE_OFFSET_HOURS = -3
CHILE_TZ_DELTA = timedelta(hours=CHILE_OFFSET_HOURS)
CHILE_TZ = timezone(CHILE_TZ_DELTA)
# -----------------------------------------------------------------------


# -----------------------------
# Modelos
# -----------------------------
class Dato1(db.Model):
    __tablename__ = "dato1_referencias"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre}


class Dato2(db.Model):
    __tablename__ = "dato2_referencias"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre}


class RegistroLitro(db.Model):
    __tablename__ = "registros_litros"
    # Almacenamos el campo fecha como NAIVE DATETIME (sin TZ) en la base de datos, 
    # pero nos aseguramos de que sea siempre la hora UTC correcta.
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    litros = db.Column(db.Float)
    ibutton = db.Column(db.String(50))
    dispositivo_id = db.Column(db.Integer, nullable=False)
    dato1_id = db.Column(db.Integer, db.ForeignKey("dato1_referencias.id", ondelete="SET NULL"), nullable=True)
    dato2_id = db.Column(db.Integer, db.ForeignKey("dato2_referencias.id", ondelete="SET NULL"), nullable=True)

    # RESTRICCIÓN DE UNICIDAD COMPUESTA: ¡CLAVE!
    __table_args__ = (UniqueConstraint("fecha", "dispositivo_id", name="uq_fecha_dispositivo"),)

    def to_dict(self):
        # 💡 CORRECCIÓN ZONA HORARIA: 
        # 1. Trata la fecha de la DB (naive) como si fuera UTC.
        utc_datetime = self.fecha.replace(tzinfo=timezone.utc)
        # 2. Convierte explícitamente a la zona horaria chilena (CHILE_TZ).
        local_datetime = utc_datetime.astimezone(CHILE_TZ)
        
        # El .isoformat() ahora incluye automáticamente el offset -03:00.
        iso_local = local_datetime.isoformat()
        
        return {
            "id": self.id,
            "fecha": iso_local,
            "litros": self.litros,
            "ibutton": self.ibutton,
            "dispositivo_id": self.dispositivo_id,
            "dato1_id": self.dato1_id,
            "dato2_id": self.dato2_id,
        }


class LitrosControl(db.Model):
    __tablename__ = "litros_controles"
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    dispositivo = db.Column(db.Integer, nullable=False)
    litros_inicio = db.Column(db.Float, nullable=False)
    litros_final = db.Column(db.Float, nullable=False)
    diferencia_manual = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "fecha": self.fecha.isoformat(),
            "dispositivo": self.dispositivo,
            "litros_inicio": self.litros_inicio,
            "litros_final": self.litros_final,
            "diferencia_manual": self.diferencia_manual,
        }


# Crear tablas si no existen
with app.app_context():
    db.create_all()

tb = ThingsBoardSimple()


# -----------------------------
# Endpoints CRUD Dato1 y Dato2 (Sin cambios)
# -----------------------------
@app.route("/dato1", methods=["GET"])
def get_dato1():
    data = db.session.execute(db.select(Dato1).order_by(Dato1.id)).scalars()
    return jsonify([item.to_dict() for item in data])


@app.route("/dato1", methods=["POST"])
def add_dato1_api():
    data = request.json
    try:
        new_item = Dato1(nombre=data["nombre"])
        db.session.add(new_item)
        db.session.commit()
        return jsonify(new_item.to_dict()), 201
    except (TypeError, KeyError) as e:
        return jsonify({"error": f"Datos incompletos o incorrectos: {e}"}), 400


@app.route("/dato1/<int:item_id>", methods=["PUT", "DELETE"])
def manage_dato1(item_id):
    item = db.session.get(Dato1, item_id)
    if not item:
        return jsonify({"error": f"Dato1 con ID {item_id} no encontrado"}), 404

    if request.method == "PUT":
        data = request.json
        try:
            item.nombre = data.get("nombre", item.nombre).strip()
            db.session.commit()
            return jsonify(item.to_dict()), 200
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"error": f"Error al actualizar Dato1: {e}"}), 400

    elif request.method == "DELETE":
        try:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"message": f"Dato1 con ID {item_id} eliminado"}), 204
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"error": f"Error al eliminar Dato1: {e}"}), 500


@app.route("/dato2", methods=["GET"])
def get_dato2():
    data = db.session.execute(db.select(Dato2).order_by(Dato2.id)).scalars()
    return jsonify([item.to_dict() for item in data])


@app.route("/dato2", methods=["POST"])
def add_dato2_api():
    data = request.json
    try:
        new_item = Dato2(nombre=data["nombre"])
        db.session.add(new_item)
        db.session.commit()
        return jsonify(new_item.to_dict()), 201
    except (TypeError, KeyError) as e:
        return jsonify({"error": f"Datos incompletos o incorrectos: {e}"}), 400


@app.route("/dato2/<int:item_id>", methods=["PUT", "DELETE"])
def manage_dato2(item_id):
    item = db.session.get(Dato2, item_id)
    if not item:
        return jsonify({"error": f"Dato2 con ID {item_id} no encontrado"}), 404

    if request.method == "PUT":
        data = request.json
        try:
            item.nombre = data.get("nombre", item.nombre).strip()
            db.session.commit()
            return jsonify(item.to_dict()), 200
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"error": f"Error al actualizar Dato2: {e}"}), 400

    elif request.method == "DELETE":
        try:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"message": f"Dato2 con ID {item_id} eliminado"}), 204
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"error": f"Error al eliminar Dato2: {e}"}), 500


# -----------------------------
# Endpoints CRUD LitrosControl (Sin cambios)
# -----------------------------
@app.route("/litros_control", methods=["GET"])
def get_litros_control():
    data = db.session.execute(db.select(LitrosControl).order_by(LitrosControl.fecha.desc())).scalars()
    return jsonify([item.to_dict() for item in data])


@app.route("/litros_control", methods=["POST"])
def add_litros_control_api():
    data = request.json
    try:
        diferencia = data["litros_final"] - data["litros_inicio"]
        fecha_obj = date.fromisoformat(data["fecha"])
        new_control = LitrosControl(
            fecha=fecha_obj,
            dispositivo=data["dispositivo"],
            litros_inicio=data["litros_inicio"],
            litros_final=data["litros_final"],
            diferencia_manual=diferencia,
        )
        db.session.add(new_control)
        db.session.commit()
        return jsonify(new_control.to_dict()), 201
    except (TypeError, KeyError, ValueError) as e:
        return jsonify({"error": f"Datos incorrectos: {e}"}), 400


@app.route("/litros_control/<int:control_id>", methods=["PUT", "DELETE"])
def manage_litros_control(control_id):
    control = db.session.get(LitrosControl, control_id)
    if not control:
        return jsonify({"error": f"Control con ID {control_id} no encontrado"}), 404

    if request.method == "PUT":
        data = request.json
        try:
            control.fecha = date.fromisoformat(data.get("fecha", control.fecha.isoformat()))
            control.dispositivo = data.get("dispositivo", control.dispositivo)
            control.litros_inicio = data.get("litros_inicio", control.litros_inicio)
            control.litros_final = data.get("litros_final", control.litros_final)
            control.diferencia_manual = control.litros_final - control.litros_inicio
            db.session.commit()
            return jsonify(control.to_dict()), 200
        except (TypeError, KeyError, ValueError, exc.SQLAlchemyError) as e:
            db.session.rollback()
            return jsonify({"error": f"Error al actualizar: {e}"}), 400

    elif request.method == "DELETE":
        try:
            db.session.delete(control)
            db.session.commit()
            return jsonify({"message": f"Control con ID {control_id} eliminado"}), 204
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"error": f"Error al eliminar: {e}"}), 500


# -----------------------------
# Endpoints RegistroLitro (fusionar TB + DB)
# -----------------------------
@app.route("/datos", methods=["GET"])
def get_datos_fusionados():
    # Obtener fecha de inicio y fin
    fecha_inicio_str = request.args.get("fecha_inicio")
    fecha_fin_default = datetime.now().strftime("%Y-%m-%d")
    fecha_fin_str = request.args.get("fecha_fin", fecha_fin_default)
    
    if not fecha_inicio_str:
        fecha_inicio_str = "2000-01-01"

    db_items = RegistroLitro.query.all()

    # Mapear usando la clave exacta guardada en la DB (naive UTC en ISO)
    db_map = {
        (item.fecha.isoformat(), item.dispositivo_id): item
        for item in db_items
    }
    matched_keys = set()

    datos_tb = tb.consultar_por_fechas(fecha_inicio_str, fecha_fin_str)
    resultado = []

    # Procesar dispositivo 1 y 2
    for dispositivo_id in [1, 2]:
        codigo = f"codigo{dispositivo_id}"

        if datos_tb.get(codigo):
            if dispositivo_id == 1:
                litros_data = datos_tb[codigo].get("Litros_total", [])
                ibuttons_data = datos_tb[codigo].get("iButton_total", [])
            else:
                litros_data = datos_tb[codigo].get("pulsos_total", [])
                ibuttons_data = datos_tb[codigo].get("ibutton", [])

            for i in range(len(litros_data)):
                raw_ts = litros_data[i]["ts"]

                # --- NORMALIZACIÓN TIMESTAMP A NAIVE UTC ---
                if isinstance(raw_ts, int):
                    fecha_obj_naive_utc = datetime.utcfromtimestamp(raw_ts / 1000).replace(microsecond=0)
                else:
                    fecha_str = raw_ts.split(".")[0]
                    if fecha_str.endswith("Z"):
                        fecha_str = fecha_str[:-1]

                    try:
                        fecha_obj_naive_utc = datetime.fromisoformat(fecha_str).replace(microsecond=0)
                    except ValueError:
                        fecha_obj_naive_utc = datetime.strptime(
                            fecha_str, "%Y-%m-%dT%H:%M:%S"
                        ).replace(microsecond=0)

                key = (fecha_obj_naive_utc.isoformat(), dispositivo_id)
                db_item = db_map.get(key)

                # --- Convertir a horario chileno para el cliente ---
                aware_utc = fecha_obj_naive_utc.replace(tzinfo=timezone.utc)
                local_time = aware_utc.astimezone(CHILE_TZ)
                fecha_local_str = local_time.isoformat()

                # Litros
                litros_value = litros_data[i]["value"]
                if dispositivo_id == 2:
                    litros_value = round(float(litros_value) / 19.86, 2)

                # ✅ Opción B: tomar nombre de dato1/dato2 desde DB
                dato1_nombre = None
                dato2_nombre = None
                dato1_id = None
                dato2_id = None

                if db_item:
                    dato1_id = db_item.dato1_id
                    dato2_id = db_item.dato2_id

                    if dato1_id:
                        d1 = db.session.get(Dato1, dato1_id)
                        dato1_nombre = d1.nombre if d1 else None

                    if dato2_id:
                        d2 = db.session.get(Dato2, dato2_id)
                        dato2_nombre = d2.nombre if d2 else None

                data = {
                    "fecha": fecha_local_str,
                    "litros": litros_value,
                    "ibutton": ibuttons_data[i]["value"] if i < len(ibuttons_data) else "N/A",
                    "dispositivo_id": dispositivo_id,
                    "id": db_item.id if db_item else None,
                    "dato1_id": dato1_id,
                    "dato2_id": dato2_id,
                    "dato1_nombre": dato1_nombre,
                    "dato2_nombre": dato2_nombre,
                }

                resultado.append(data)

                if db_item:
                    matched_keys.add(key)

    # ✅ Agregar registros que están solo en DB
    for key, db_item in db_map.items():
        if key not in matched_keys:

            # ✅ Recuperar nombres
            dato1_nombre = None
            dato2_nombre = None

            if db_item.dato1_id:
                d1 = db.session.get(Dato1, db_item.dato1_id)
                dato1_nombre = d1.nombre if d1 else None

            if db_item.dato2_id:
                d2 = db.session.get(Dato2, db_item.dato2_id)
                dato2_nombre = d2.nombre if d2 else None

            local_dt = db_item.fecha.replace(tzinfo=timezone.utc).astimezone(CHILE_TZ)

            resultado.append({
                "id": db_item.id,
                "fecha": local_dt.isoformat(),
                "litros": db_item.litros,
                "ibutton": db_item.ibutton,
                "dispositivo_id": db_item.dispositivo_id,
                "dato1_id": db_item.dato1_id,
                "dato2_id": db_item.dato2_id,
                "dato1_nombre": dato1_nombre,
                "dato2_nombre": dato2_nombre,
            })

    return jsonify(resultado)


@app.route("/datos", methods=["POST"])
def create_datos_referencia():
    data = request.json
    try:
        raw_fecha = data["fecha"]
        dispositivo_id = data.get("dispositivo_id")
        fecha_obj = None

        if isinstance(raw_fecha, int) or (isinstance(raw_fecha, str) and raw_fecha.isdigit()):
            # Convierte timestamp (ms) a datetime NAIVE que representa la hora UTC.
            fecha_obj = datetime.utcfromtimestamp(int(raw_fecha) / 1000)
        elif isinstance(raw_fecha, str):
            # 💡 CORRECCIÓN PARA POST: Acepta ISO string con o sin offset.
            try:
                fecha_obj = datetime.fromisoformat(raw_fecha)
                
                if fecha_obj.tzinfo is not None:
                    # Si viene con offset (ej: -03:00), lo convertimos a UTC para guardar.
                    fecha_obj = fecha_obj.astimezone(timezone.utc)
                else:
                    # Si es naive, asumimos que el cliente lo envió en HORA CHILENA, 
                    # y lo hacemos aware de CHILE_TZ para convertirlo a UTC y guardar.
                    aware_local = fecha_obj.replace(tzinfo=CHILE_TZ)
                    fecha_obj = aware_local.astimezone(timezone.utc)
                    
            except ValueError:
                 return jsonify({"error": "Formato de fecha ISO 8601 no válido."}), 400
        else:
            return jsonify({"error": "Formato de fecha no compatible."}), 400
        
        # NORMALIZACIÓN CLAVE: Quita microsegundos y se asegura que sea NAIVE para la DB
        # Almacenamos la hora en la DB como NAIVE UTC
        fecha_tb = fecha_obj.replace(microsecond=0, tzinfo=None)


        item = RegistroLitro.query.filter_by(fecha=fecha_tb, dispositivo_id=dispositivo_id).first()

        if item:
            # 1. ACTUALIZAR (Si existe)
            if "dato1_id" in data:
                item.dato1_id = data["dato1_id"]
            if "dato2_id" in data:
                item.dato2_id = data["dato2_id"]
            db.session.commit()
            return jsonify(item.to_dict()), 200
        else:
            # 2. CREAR (Si no existe)
            new_item = RegistroLitro(
                fecha=fecha_tb, # Usamos la fecha naive UTC
                litros=data.get("litros"),
                ibutton=data.get("ibutton"),
                dispositivo_id=dispositivo_id,
                dato1_id=data.get("dato1_id"),
                dato2_id=data.get("dato2_id"),
            )
            db.session.add(new_item)
            db.session.commit()
            return jsonify(new_item.to_dict()), 201

    # MANEJO ESPECÍFICO DE CONFLICTO (IntegrityError)
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Conflicto: Ya existe un registro con esta fecha y dispositivo. El registro no fue insertado."}), 409

    # MANEJO GENÉRICO DE ERRORES
    except (TypeError, KeyError, ValueError, exc.SQLAlchemyError) as e:
        db.session.rollback()
        return jsonify({"error": f"Error general al guardar/actualizar el registro: {e}"}), 400


@app.route("/datos/<int:item_id>", methods=["PATCH"])
def update_datos_referencia(item_id):
    item = db.session.get(RegistroLitro, item_id)
    if not item:
        return jsonify({"message": "Registro no encontrado. Use POST para crear."}), 404

    data = request.json
    try:
        if "dato1_id" in data:
            item.dato1_id = data["dato1_id"]
        if "dato2_id" in data:
            item.dato2_id = data["dato2_id"]
        db.session.commit()
        return jsonify(item.to_dict()), 200
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Error al actualizar: {e}"}), 400


# -----------------------------
# Endpoint de dispositivos (Sin cambios)
# -----------------------------
@app.route("/dispositivos")
def dispositivos():
    fecha_fin_default = datetime.now().strftime("%Y-%m-%d")
    datos_tb = tb.consultar_por_fechas("2000-01-01", fecha_fin_default)
    
    ids_unicos = set()
    if datos_tb.get("codigo1"): ids_unicos.add(1)
    if datos_tb.get("codigo2"): ids_unicos.add(2)
    nombres_custom = {1: "Tanque Fijo", 2: "Tanque Movil"}
    return jsonify([{"id": did, "nombre": nombres_custom.get(did, f"Dispositivo {did}")} for did in ids_unicos])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
