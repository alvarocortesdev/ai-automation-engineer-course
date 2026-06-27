"""App FastAPI mínima para contenerizar.

NO necesitas modificar este archivo. Es la app que tu Dockerfile debe empaquetar.
El endpoint `/health` existe a propósito: es el que tu HEALTHCHECK debe golpear.

Para correrla localmente (opcional, fuera de Docker):
    uv run --with "fastapi[standard]" fastapi dev app/main.py
"""

from fastapi import FastAPI

app = FastAPI(title="API de ejemplo F5")


@app.get("/health")
def health():
    """Endpoint de salud: el HEALTHCHECK del contenedor lo consulta."""
    return {"status": "ok"}


@app.get("/")
def root():
    return {"mensaje": "Hola desde un contenedor"}
