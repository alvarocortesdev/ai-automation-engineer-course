"""Backend de ejemplo para AUDITAR — tiene varias violaciones de 12-factor.

NO lo copies a producción. Tu trabajo NO es ejecutarlo ni arreglarlo aquí, sino
identificar en `auditoria.md` qué factores viola, qué síntoma provoca cada uno
en producción, y cómo se arregla. Hay al menos seis violaciones reales entre
este archivo, el Dockerfile y el compose.yaml.
"""

import logging

# Config y secretos escritos directamente en el código:
DATABASE_URL = "postgresql://admin:s3cr3t@db-prod.internal:5432/tienda"
STRIPE_API_KEY = "sk_live_51Hxxxxxxxxxxxxxxxx_CLAVE_REAL"
PORT = 8000

# Estado del proceso en memoria:
SESSIONS: dict[str, int] = {}        # session_id -> user_id
CARRITOS: dict[int, list] = {}       # user_id -> items del carrito

# Logs a un archivo en disco, dentro del contenedor:
logging.basicConfig(filename="/var/log/tienda/app.log", level=logging.INFO)


def login(session_id: str, user_id: int) -> None:
    SESSIONS[session_id] = user_id
    logging.info("login user=%s", user_id)


def agregar_al_carrito(user_id: int, item: dict) -> None:
    CARRITOS.setdefault(user_id, []).append(item)


def correr() -> None:
    import uvicorn
    # Se ata a un puerto fijo escrito en el código:
    uvicorn.run("app:api", host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    correr()
