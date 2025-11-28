import re
import pdfplumber


class FacturaExtractor:

    @staticmethod
    def extraer(pdf_file):
        data = {
            "numero_factura": None,
            "producto": None,
            "litros": None,
            "fecha": None,
            "total": None,
            "proveedor": None,
        }

        # --- Leer PDF ---
        texto = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                contenido = page.extract_text()
                if contenido:
                    texto += contenido + " "

        texto = " ".join(texto.split())  # limpiar espacios

        # NUMERO FACTURA
        match = re.search(r"N[º°]\s*([0-9]{6,12})", texto)
        if match:
            data["numero_factura"] = match.group(1)

        # PROVEEDOR
        match = re.search(r"COPEC", texto, re.IGNORECASE)
        if match:
            data["proveedor"] = "COPEC"

        # ----------------------------------------------------
        # PRODUCTO - detectar el texto ANTES de los litros
        # ----------------------------------------------------

        # Buscar patrón de litros
        litros_match = re.search(r"(\d{1,3}(?:\.\d{3})*,\d{2})\s*L", texto)

        if litros_match:
            idx = litros_match.start()

            # Tomamos 80-120 caracteres antes del match para buscar el producto
            bloque = texto[max(0, idx - 120):idx]

            # Quitamos palabras basura típicas del encabezado
            bloque = re.sub(r"\b(IE|PTOTAL|U|SUBTOTAL)\b", "", bloque, flags=re.IGNORECASE)

            # Limpiamos dobles espacios
            bloque = " ".join(bloque.split())

            # Extraemos solo letras/números típicos del producto
            match = re.search(r"([A-Z0-9\sº°\-]+)$", bloque, re.IGNORECASE)
            
            if match:
                data["producto"] = match.group(1).strip().upper()

        # Litros
        match = re.search(r"(\d{1,3}\.\d{3},\d{2})\s*L", texto)
        if match:
            litros = match.group(1).replace(".", "").replace(",", ".")
            data["litros"] = float(litros)
    
        # ----------------------------------------------------
        # FECHA (Formatear 05-NOV-2025 → 05-11-2025)
        # ----------------------------------------------------
        match = re.search(r"\b([0-9]{2}-[A-Z]{3}-[0-9]{4})\b", texto)
        if match:
            fecha_raw = match.group(1)
            dia, mes_texto, anio = fecha_raw.split("-")

            MESES = {
                "ENE": "01", "FEB": "02", "MAR": "03", "ABR": "04",
                "MAY": "05", "JUN": "06", "JUL": "07", "AGO": "08",
                "SEP": "09", "OCT": "10", "NOV": "11", "DIC": "12",
            }

            mes_num = MESES.get(mes_texto.upper(), "01")
            data["fecha"] = f"{dia}-{mes_num}-{anio}"


        # ----------------------------------------------------
        # TOTAL (Detectar monto correcto después de "TOTAL")
        # ----------------------------------------------------
        pos = texto.find("TOTAL")
        if pos != -1:
            segmento = texto[pos:]  # texto desde TOTAL en adelante

            # Buscar montos grandes
            numeros = re.findall(r"\b([0-9]{1,3}(?:\.[0-9]{3})+)\b", segmento)

            # Tomar el séptimo número si existe (tu lógica original)
            if len(numeros) >= 7:
                total_real = numeros[6]
                data["total"] = int(total_real.replace(".", ""))

        return data