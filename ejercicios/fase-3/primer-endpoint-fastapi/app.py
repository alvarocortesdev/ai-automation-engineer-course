"""Tu primera API FastAPI: una mini-API de TAREAS en memoria.

Implementa tres endpoints sobre el contrato que fija este archivo y el README.
Almacenamiento: un dict en memoria (no necesitas base de datos).

Corre el servidor para jugar a mano:
    uv run fastapi dev app.py        # luego abre http://127.0.0.1:8000/docs

Corre los tests:
    uv run pytest                    # o simplemente:  pytest

Tu trabajo está marcado con TODO. NO cambies las firmas de las funciones ni el
modelo `TareaPublica` (fijan el contrato que el test verifica).
"""

from __future__ import annotations

from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel

app = FastAPI(title="API de tareas")

# --- Almacenamiento en memoria (ya provisto) -------------------------------
# Cada tarea es un dict: {"id", "titulo", "descripcion", "completada"}.
_TAREAS: dict[int, dict] = {}
_siguiente_id = 1


# --- Modelos ----------------------------------------------------------------
class TareaPublica(BaseModel):
    """Modelo de SALIDA. Fija el contrato del response. NO lo modifiques."""

    id: int
    titulo: str
    descripcion: str | None = None
    completada: bool


class TareaCrear(BaseModel):
    """Modelo de ENTRADA del body de POST /tareas.

    TODO: define los campos.
      - `titulo`: str, OBLIGATORIO y NO vacío (pista: pydantic `Field(min_length=1)`).
      - `descripcion`: str opcional (default None).
    """

    ...  # TODO: reemplaza esto por los campos


# --- Endpoints --------------------------------------------------------------
@app.post("/tareas", response_model=TareaPublica, status_code=status.HTTP_201_CREATED)
async def crear_tarea(datos: TareaCrear) -> dict:
    """Crea una tarea (nace con completada=False) y devuélvela.

    TODO:
      - usa el contador `_siguiente_id` (recuerda `global`),
      - construye el dict con id, titulo, descripcion y completada=False,
      - guárdalo en `_TAREAS` y devuélvelo.
    """
    raise NotImplementedError("implementa crear_tarea")


@app.get("/tareas/{tarea_id}", response_model=TareaPublica)
async def obtener_tarea(tarea_id: int) -> dict:
    """Devuelve la tarea con ese id, o 404 si no existe.

    TODO: busca en `_TAREAS`; si no está, `raise HTTPException(status_code=404, ...)`.
    """
    raise NotImplementedError("implementa obtener_tarea")


@app.get("/tareas", response_model=list[TareaPublica])
async def listar_tareas(
    completada: bool | None = None,
    limite: Annotated[int, Query(ge=1, le=100)] = 20,
) -> list[dict]:
    """Lista tareas. Si `completada` viene dado, filtra por ese valor.
    Devuelve a lo más `limite` resultados.

    TODO: filtra `_TAREAS.values()` por `completada` (si no es None) y recorta a `limite`.
    """
    raise NotImplementedError("implementa listar_tareas")
