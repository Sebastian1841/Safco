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
        }

        # --- Leer PDF ---
        texto = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                contenido = page.extract_text()
                if contenido:
                    texto += contenido + " "

        texto = " ".join(texto.split())  # limpiar espacios

        # --- Nº factura ---
        match = re.search(r"N[º°]\s*([0-9]{6,12})", texto)
        if match:
            data["numero_factura"] = match.group(1)

        # --- Producto ---
        match = re.search(
            r"PETROLEO\s+DIESEL\s+GRADO\s+B\s+NU\s+1202", texto, re.IGNORECASE
        )
        if match:
            data["producto"] = match.group(0).upper()

        # --- Litros ---
        match = re.search(r"(\d{1,3}\.\d{3},\d{2})\s*L", texto)
        if match:
            litros = match.group(1).replace(".", "").replace(",", ".")
            data["litros"] = float(litros)

        # --- Fecha ---
        match = re.search(r"\b([0-9]{2}-[A-Z]{3}-[0-9]{4})\b", texto)
        if match:
            data["fecha"] = match.group(1)


        # --- TOTAL (7° número después de la palabra TOTAL) ---
        pos = texto.find("TOTAL")
        if pos != -1:
            segmento = texto[pos:]  # texto desde TOTAL en adelante

            # Buscar todos los números grandes en ese segmento
            numeros = re.findall(r"\b([0-9]{1,3}(?:\.[0-9]{3})+)\b", segmento)

            # Tomar el séptimo número si existe
            if len(numeros) >= 7:
                total_real = numeros[6]  # índice 6 = séptimo número
                data["total"] = int(total_real.replace(".", ""))

        return data
