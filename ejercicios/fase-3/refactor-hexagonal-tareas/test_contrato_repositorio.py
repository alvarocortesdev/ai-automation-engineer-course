"""Test 2 — Los dos adaptadores cumplen el MISMO contrato (son intercambiables).

Corre el mismo set de pruebas contra:
  - RepositorioTareasMemoria  (sin DB)
  - RepositorioTareasSQLAlchemy (SQLite EN MEMORIA, no necesitas Postgres)

Que ambos pasen exactamente las mismas pruebas ES la demostración del beneficio
de la hexagonal: puedes cambiar de infraestructura sin tocar el dominio, porque
ambos honran el puerto RepositorioTareas.

No abras este archivo para adivinar la solución: solo verifica la tuya.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from adaptador_memoria import RepositorioTareasMemoria
from adaptador_sqlalchemy import RepositorioTareasSQLAlchemy
from dominio import Tarea
from modelos import Base


@pytest.fixture(params=["memoria", "sqlalchemy"])
def repo(request):
    if request.param == "memoria":
        yield RepositorioTareasMemoria()
    else:
        # SQLite en memoria; StaticPool reutiliza la misma conexión.
        engine = create_engine("sqlite://", poolclass=StaticPool)
        Base.metadata.create_all(engine)
        with Session(engine) as session:
            yield RepositorioTareasSQLAlchemy(session)


def test_agregar_asigna_id(repo):
    tarea = repo.agregar(Tarea(titulo="comprar pan"))
    assert tarea.id is not None, "agregar() debe devolver la tarea con id asignado"


def test_agregar_devuelve_entidad_de_dominio(repo):
    tarea = repo.agregar(Tarea(titulo="x"))
    assert isinstance(tarea, Tarea), (
        "agregar() debe devolver una entidad de dominio Tarea, "
        "no un TareaORM ni un dict (no filtres el ORM al dominio)"
    )


def test_obtener_recupera_lo_agregado(repo):
    creada = repo.agregar(Tarea(titulo="leer docs"))
    recuperada = repo.obtener(creada.id)
    assert recuperada is not None
    assert recuperada.titulo == "leer docs"


def test_obtener_inexistente_devuelve_none(repo):
    assert repo.obtener(9999) is None


def test_listar_devuelve_todas(repo):
    repo.agregar(Tarea(titulo="a"))
    repo.agregar(Tarea(titulo="b"))
    titulos = {t.titulo for t in repo.listar()}
    assert titulos == {"a", "b"}


def test_contar_pendientes_ignora_completadas(repo):
    repo.agregar(Tarea(titulo="pendiente 1"))
    repo.agregar(Tarea(titulo="pendiente 2"))
    repo.agregar(Tarea(titulo="lista", completada=True))
    assert repo.contar_pendientes() == 2
