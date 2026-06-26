"""ADAPTADOR DE ENTRADA (HTTP) — complétalo.

Aquí —y SOLO aquí— se traducen las excepciones de dominio a status codes y se
elige el adaptador concreto. El endpoint pide el PUERTO (`RepositorioTareas`),
no el adaptador; `Depends(obtener_repo)` decide cuál es el concreto. Eso es lo
que `test_api.py` aprovecha: sobreescribe `obtener_repo` con un doble en memoria
(`app.dependency_overrides`) y no toca ninguna base de datos.

Mantén `obtener_repo` como el ÚNICO lugar donde se nombra el adaptador real.
"""

from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from adaptador_sqlalchemy import RepositorioTareasSQLAlchemy
from dominio import LimiteTareasPendientes, RepositorioTareas, ServicioTareas
from modelos import Base

engine = create_engine("postgresql+psycopg://usuario:clave@localhost/tareas")
app = FastAPI()


def obtener_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
        session.commit()


def obtener_repo(
    session: Annotated[Session, Depends(obtener_session)],
) -> RepositorioTareas:
    # Punto único de cableado del adaptador concreto.
    return RepositorioTareasSQLAlchemy(session)


# El endpoint pide el PUERTO, no el adaptador.
RepoTareas = Annotated[RepositorioTareas, Depends(obtener_repo)]


class CrearTareaIn(BaseModel):
    titulo: str


class TareaOut(BaseModel):
    id: int
    titulo: str
    completada: bool


@app.post("/tareas", status_code=201, response_model=TareaOut)
def crear_tarea(payload: CrearTareaIn, repo: RepoTareas) -> TareaOut:
    # TODO: instancia ServicioTareas(repo), llama a crear_tarea, traduce
    #       LimiteTareasPendientes a HTTPException(409) y mapea la entidad a TareaOut.
    raise NotImplementedError("implementa el endpoint POST /tareas")


@app.get("/tareas", response_model=list[TareaOut])
def listar_tareas(repo: RepoTareas) -> list[TareaOut]:
    # TODO: lista vía el servicio y mapea cada entidad a TareaOut.
    raise NotImplementedError("implementa el endpoint GET /tareas")
