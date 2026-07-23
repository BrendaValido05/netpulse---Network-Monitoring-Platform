# Imagen base: Python 3.12 ya instalado, versión "slim" = más ligera
# (menos cosas innecesarias que la imagen completa de Python).
FROM python:3.12-slim

# Carpeta dentro del contenedor donde va a vivir nuestro código.
WORKDIR /app

# Sin esto, herramientas como "alembic" (que se lanzan como programa
# aparte, no como "python -m api...") no saben que /app contiene el
# paquete "api" y fallan con ModuleNotFoundError al hacer imports
# como "from api.config import settings".
ENV PYTHONPATH=/app

# Copiamos primero SOLO requirements.txt (no todo el código) y lo
# instalamos. ¿Por qué en este orden y no copiar todo de golpe?
# Docker cachea cada paso: si luego cambias tu código pero no las
# dependencias, Docker reutiliza esta capa ya instalada en vez de
# reinstalar todo de nuevo — reconstruir la imagen es mucho más rápido.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ahora sí copiamos el resto del código.
COPY . .

# Documenta que este contenedor escucha en el puerto 8000 (informativo,
# no abre el puerto por sí solo, eso lo hace docker-compose).
EXPOSE 8000

# Comando que se ejecuta cuando arranca el contenedor.
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
