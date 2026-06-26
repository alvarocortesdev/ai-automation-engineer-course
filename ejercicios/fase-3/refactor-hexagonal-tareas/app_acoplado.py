"""EL PUNTO DE PARTIDA (acoplado) — léelo, NO lo edites.

Este es el endpoint "que funciona" pero que mezcla TRES trabajos en una sola
función: parsear HTTP, aplicar la regla de negocio (no más de 5 tareas
pendientes) y hablar con SQLAlchemy. Tu tarea NO es arreglar este archivo, sino
refactorizarlo en las cuatro piezas que pide el README:

    dominio.py · adaptador_memoria.py · adaptador_sqlalchemy.py · api.py

Pregúntate, antes de tocar nada:
  1. ¿Dónde está la regla de negocio y con qué está enredada?
  2. ¿Por qué para testear "el 6º pendiente es rechazado" necesito Postgres?
  3. Si mañana las tareas se guardan en otro sistema, ¿qué tendría que reescribir?

La respuesta a (3) es "demasiado": ese es el problema que la hexagonal resuelve.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from modelos import Base, TareaORM

engine = create_engine("postgresql+psycopg://usuario:clave@localhost/tareas")
Base.metadata.create_all(engine)
app = FastAPI()

MAX_PENDIENTES = 5


class CrearTareaIn(BaseModel):
    titulo: str


@app.post("/tareas", status_code=201)
def crear_tarea(payload: CrearTareaIn):
    with Session(engine) as session:
        # --- regla de negocio enredada con SQL: imposible de testear sin DB ---
        pendientes = session.scalar(
            select(func.count()).select_from(TareaORM).where(TareaORM.completada == False)  # noqa: E712
        )
        if pendientes >= MAX_PENDIENTES:
            raise HTTPException(status_code=409, detail="Demasiadas tareas pendientes")
        # --- persistencia ---
        fila = TareaORM(titulo=payload.titulo, completada=False)
        session.add(fila)
        session.commit()
        return {"id": fila.id, "titulo": fila.titulo, "completada": fila.completada}


@app.get("/tareas")
def listar_tareas():
    with Session(engine) as session:
        filas = session.scalars(select(TareaORM)).all()
        return [{"id": f.id, "titulo": f.titulo, "completada": f.completada} for f in filas]
