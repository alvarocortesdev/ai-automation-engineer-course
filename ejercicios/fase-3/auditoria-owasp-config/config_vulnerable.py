"""ARCHIVO PARA AUDITAR — NO LO EJECUTES NI LO CORRIJAS.

Es el arranque de un backend FastAPI escrito por alguien apurado. "Funciona" en la
demo y está lleno de fallas de seguridad reales. Tu trabajo (ver README) es leerlo
como un semi-senior y producir `auditoria.md`: cada hallazgo mapeado a su categoría
del OWASP Top 10, su severidad, por qué es un riesgo y el fix concreto.

NO edites este archivo. La entrega es tu auditoría en Markdown, no código.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, text

# (1) modo debug encendido
app = FastAPI(debug=True)

# (2) CORS: cualquier origen + credenciales
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# (3) secretos hardcodeados en el código (y commiteados al repo)
JWT_SECRET = "supersecreto123"
DATABASE_URL = "postgresql://app:app1234@db.interno:5432/prod"

engine = create_engine(DATABASE_URL)


@app.post("/login")
def login(email: str, password: str):
    # (4) query construida con f-string a partir de la entrada del usuario
    with engine.connect() as conn:
        fila = conn.execute(
            text(f"SELECT id, password_hash FROM usuarios WHERE email = '{email}'")
        ).first()
    # (5) comparación de contraseña en texto plano contra el hash
    if fila is None or fila.password_hash != password:
        return {"ok": False}
    # (sin límite de intentos: fuerza bruta libre)
    return {"ok": True, "token": "..."}


@app.get("/usuarios/{usuario_id}")
def obtener_usuario(usuario_id: int):
    # (6) sin autenticación ni chequeo de dueño: cualquiera lee cualquier usuario
    with engine.connect() as conn:
        fila = conn.execute(
            text("SELECT * FROM usuarios WHERE id = :id"), {"id": usuario_id}
        ).first()
    # (7) devuelve la fila CRUDA, incluido password_hash y campos internos
    return dict(fila._mapping) if fila else {}


@app.exception_handler(Exception)
async def manejar_todo(request: Request, exc: Exception):
    # (8) devuelve el detalle de la excepción (stack/clase/mensaje) al cliente
    return JSONResponse(status_code=500, content={"error": str(exc), "tipo": type(exc).__name__})
