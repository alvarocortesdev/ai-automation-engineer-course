"""Broken Access Control (IDOR) + fuga de datos en FastAPI.

API de NOTAS con autenticación SIMPLIFICADA: el header `x-user-id` identifica al
usuario que llama (en producción esto vendría de un JWT, ver 3.12). Cada nota tiene
un dueño (`owner_id`) y un campo interno que NUNCA debe salir al cliente.

El código que te entregan es VULNERABLE a propósito:
  - GET /notas        devuelve las notas de TODO el mundo.
  - GET /notas/{id}   devuelve cualquier nota sin comprobar dueño, y filtra el
                      campo interno (no usa response_model).
  - DELETE /notas/{id} borra cualquier nota sin comprobar dueño.

Tu trabajo (busca los TODO): cerrar el control de acceso y la fuga. NO cambies la
forma de la autenticación ni los modelos ya dados salvo donde el TODO lo pida.

Corre el servidor para jugar a mano:
    uv run fastapi dev app.py        # http://127.0.0.1:8000/docs

Corre los tests:
    uv run pytest
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI(title="API de notas (control de acceso)")

# --- Estado en memoria (ya provisto) ---------------------------------------
# Cada nota: {"id", "owner_id", "titulo", "cuerpo", "nota_privada_interna"}
_NOTAS: dict[int, dict] = {}
_siguiente_id = 1


# --- Modelos ----------------------------------------------------------------
class Usuario(BaseModel):
    id: int


class NotaCrear(BaseModel):
    titulo: str
    cuerpo: str


class NotaPublica(BaseModel):
    """Lo que el cliente PUEDE ver. Nota: no incluye owner_id ni el campo interno."""

    id: int
    titulo: str
    cuerpo: str


# --- Autenticación simplificada (ya provista) ------------------------------
def usuario_actual(x_user_id: Annotated[int | None, Header()] = None) -> Usuario:
    """Lee el header `x-user-id`. 401 si falta. (En real: validar un JWT, ver 3.12.)"""
    if x_user_id is None:
        raise HTTPException(status_code=401, detail="falta el header x-user-id")
    return Usuario(id=x_user_id)


UsuarioActual = Annotated[Usuario, Depends(usuario_actual)]


# --- Endpoints --------------------------------------------------------------
@app.post("/notas", response_model=NotaPublica, status_code=status.HTTP_201_CREATED)
async def crear_nota(datos: NotaCrear, usuario: UsuarioActual) -> dict:
    """Crea una nota cuyo dueño es el usuario actual. (Ya correcto; no lo toques.)"""
    global _siguiente_id
    nota = {
        "id": _siguiente_id,
        "owner_id": usuario.id,
        "titulo": datos.titulo,
        "cuerpo": datos.cuerpo,
        "nota_privada_interna": f"flags-internos-de-{usuario.id}",
    }
    _NOTAS[_siguiente_id] = nota
    _siguiente_id += 1
    return nota


@app.get("/notas", response_model=list[NotaPublica])
async def listar_notas(usuario: UsuarioActual) -> list[dict]:
    # TODO (1): VULNERABLE. Devuelve TODAS las notas, de todos los usuarios.
    #           Filtra para devolver SOLO las del usuario actual (owner_id == usuario.id).
    return [_NOTAS[k] for k in sorted(_NOTAS)]


@app.get("/notas/{nota_id}")  # TODO (2a): falta response_model=NotaPublica (filtra la fuga)
async def obtener_nota(nota_id: int, usuario: UsuarioActual):
    nota = _NOTAS.get(nota_id)
    # TODO (2b): VULNERABLE. Solo comprueba que exista, no que sea del usuario.
    #            Devuelve 404 si no existe O no es del usuario actual (no 403: no filtres
    #            la existencia del recurso ajeno).
    if nota is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return nota  # además filtra nota_privada_interna porque no hay response_model


@app.delete("/notas/{nota_id}", status_code=status.HTTP_204_NO_CONTENT)
async def borrar_nota(nota_id: int, usuario: UsuarioActual) -> Response:
    nota = _NOTAS.get(nota_id)
    # TODO (3): VULNERABLE. Borra cualquier nota. Aplica el MISMO chequeo de dueño
    #           que en obtener_nota (404 si no existe o no es suya) ANTES de borrar.
    if nota is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    del _NOTAS[nota_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
