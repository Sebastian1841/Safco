# Imagen base Python
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copiar archivos del backend
COPY Ejemplo.py .
COPY app.py .
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer puerto Flask
EXPOSE 5000

# Comando para levantar el backend
CMD ["python", "app.py"]
