"""Test de aceptación: la consulta NO debe tener N+1.

Siembra 10 autores con 3 libros cada uno en una base SQLite EN MEMORIA
(no necesitas Postgres ni DATABASE_URL), cuenta las queries que ejecuta tu
`listar_autores_con_libros`, y exige:

  1. Corrección: estructura y datos correctos.
  2. Sin N+1: <= 2 queries, sin importar el número de autores.

La versión ingenua (lazy) ejecuta 1 + 10 = 11 queries y FALLA el test.

Requiere solo `sqlalchemy` (pysqlite viene con Python). Instálalo con:
    uv add sqlalchemy pytest        # o:  pip install sqlalchemy pytest

NO abras este archivo para "adivinar" la solución: solo verifica la tuya.
"""

import pytest
from sqlalchemy import create_engine, event, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from modelos import Autor, Base, Libro
from solucion import listar_autores_con_libros

N_AUTORES = 10
LIBROS_POR_AUTOR = 3
MAX_QUERIES = 2


class _ContadorQueries:
    """Cuenta cada SELECT que pasa por el engine vía event listener."""

    def __init__(self) -> None:
        self.selects = 0

    def __call__(self, conn, cursor, statement, parameters, context, executemany) -> None:
        if statement.lstrip().upper().startswith("SELECT"):
            self.selects += 1


@pytest.fixture
def engine():
    # SQLite en memoria; StaticPool reutiliza la misma conexión para que la
    # base sobreviva entre la siembra y la consulta del test.
    eng = create_engine("sqlite://", poolclass=StaticPool)
    Base.metadata.create_all(eng)
    with Session(eng) as s:
        for a in range(N_AUTORES):
            autor = Autor(nombre=f"Autor {a}")
            autor.libros = [
                Libro(titulo=f"Libro {a}-{b}") for b in range(LIBROS_POR_AUTOR)
            ]
            s.add(autor)
        s.commit()
    return eng


def test_datos_correctos(engine):
    # Sesión fresca: como en un request real, sin objetos precargados.
    with Session(engine) as s:
        resultado = listar_autores_con_libros(s)

    assert isinstance(resultado, list), "debe devolver una lista"
    assert len(resultado) == N_AUTORES, f"se esperaban {N_AUTORES} autores"

    nombres = {fila["autor"] for fila in resultado}
    assert nombres == {f"Autor {a}" for a in range(N_AUTORES)}

    for fila in resultado:
        assert "libros" in fila, "cada autor debe traer su lista de libros"
        assert len(fila["libros"]) == LIBROS_POR_AUTOR, (
            f"cada autor debe tener {LIBROS_POR_AUTOR} libros, "
            f"'{fila['autor']}' trajo {len(fila['libros'])}"
        )


def test_no_hay_n_mas_1(engine):
    contador = _ContadorQueries()
    event.listen(engine, "before_cursor_execute", contador)
    try:
        with Session(engine) as s:
            listar_autores_con_libros(s)
    finally:
        event.remove(engine, "before_cursor_execute", contador)

    assert contador.selects <= MAX_QUERIES, (
        f"se ejecutaron {contador.selects} SELECTs para {N_AUTORES} autores: "
        f"eso es un N+1 (1 + N). Con eager loading deben ser <= {MAX_QUERIES}, "
        f"sin importar cuántos autores haya."
    )
