"""Dependencias, errores globales y background tasks en FastAPI.

API de NOTAS en memoria que conecta cuatro piezas que todo backend real usa:
  1. una dependencia de autenticación por header `x-api-key` (Depends),
  2. una dependencia de paginación compartida (Depends),
  3. un exception handler global que traduce una excepción de DOMINIO a un 404,
  4. una background task que registra auditoría tras crear.

Corre el servidor para jugar a mano:
    uv run fastapi dev app.py        # http://127.0.0.1:8000/docs

Corre los tests:
    uv run pytest

Tu trabajo está marcado con TODO. NO cambies las firmas ni los modelos.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    Header,
    HTTPException,
    Query,
    status,
)
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from pydantic import BaseModel

app = FastAPI(title="API de notas")

# --- Estado en memoria (ya provisto) ---------------------------------------
API_KEY = "secreto-demo"                 # la clave válida (en real iría en una env var)
_NOTAS: dict[int, dict] = {}
_siguiente_id = 1
_AUDITORIA: list[str] = []               # el "log" donde escribe la background task


# --- Modelos ----------------------------------------------------------------
class NotaCrear(BaseModel):
    titulo: str
    cuerpo: str


class NotaPublica(BaseModel):
    id: int
    titulo: str
    cuerpo: str


# --- Excepción de DOMINIO (no sabe nada de HTTP) ---------------------------
class RecursoNoEncontrado(Exception):
    """La lógica lanza esto; el borde HTTP lo traduce a 404 (ver TODO del handler)."""

    def __init__(self, recurso: str, id_: int) -> None:
        self.recurso = recurso
        self.id = id_


def registrar_auditoria(mensaje: str) -> None:
    """Background task: anota un evento. (Ya provista; tú solo la agendas.)"""
    _AUDITORIA.append(mensaje)


# --- Dependencias (impleméntalas) ------------------------------------------
def obtener_api_key(x_api_key: Annotated[str | None, Header()] = None) -> str:
    """Lee el header `x-api-key` y exige que sea la correcta.

    TODO: si `x_api_key` no coincide con API_KEY, `raise HTTPException(status_code=401, ...)`.
          Si coincide, devuélvela.
    """
    raise NotImplementedError("implementa obtener_api_key")


def parametros_paginacion(
    saltar: Annotated[int, Query(ge=0)] = 0,
    limite: Annotated[int, Query(ge=1, le=100)] = 20,
) -> dict[str, int]:
    """Devuelve los parámetros de paginación ya validados.

    TODO: devuelve un dict {"saltar": saltar, "limite": limite}.
    """
    raise NotImplementedError("implementa parametros_paginacion")


# Alias reutilizables: el Depends va dentro del tipo.
ApiKeyDep = Annotated[str, Depends(obtener_api_key)]
PaginacionDep = Annotated[dict[str, int], Depends(parametros_paginacion)]


# --- Exception handler global ----------------------------------------------
# TODO: registra un handler para RecursoNoEncontrado con @app.exception_handler(...)
#       que devuelva un JSONResponse con status 404 y este cuerpo EXACTO:
#           {"error": "no_encontrado", "recurso": <exc.recurso>, "id": <exc.id>}
#       Firma del handler:  async def ...(request: Request, exc: RecursoNoEncontrado)


# --- Endpoints (impleméntalos) ---------------------------------------------
@app.get("/notas", response_model=list[NotaPublica])
async def listar_notas(api_key: ApiKeyDep, paginacion: PaginacionDep) -> list[dict]:
    """Lista notas (protegido por api-key). Aplica saltar/limite de la paginación.

    TODO: ordena por id, aplica `saltar` y `limite`, devuelve la lista.
    """
    raise NotImplementedError("implementa listar_notas")


@app.get("/notas/{nota_id}", response_model=NotaPublica)
async def obtener_nota(nota_id: int, api_key: ApiKeyDep) -> dict:
    """Devuelve una nota o lanza RecursoNoEncontrado (que el handler vuelve 404).

    TODO: si `nota_id` no está en _NOTAS, `raise RecursoNoEncontrado("nota", nota_id)`.
    """
    raise NotImplementedError("implementa obtener_nota")


@app.post("/notas", response_model=NotaPublica, status_code=status.HTTP_201_CREATED)
async def crear_nota(
    datos: NotaCrear, api_key: ApiKeyDep, tareas: BackgroundTasks
) -> dict:
    """Crea una nota y agenda una background task de auditoría.

    TODO:
      - usa `_siguiente_id` (recuerda `global`) y guarda en _NOTAS,
      - `tareas.add_task(registrar_auditoria, f"nota creada: {nueva_id}")`,
      - devuelve la nota.
    """
    raise NotImplementedError("implementa crear_nota")
