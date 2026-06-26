"""Lista cada autor con los títulos de sus libros — SIN disparar el N+1.

El test siembra 10 autores con 3 libros cada uno, cuenta las queries que
ejecutas, y exige que sean <= 2 (sin importar cuántos autores haya). La
versión "ingenua" (lazy) dispara 1 + N = 11 queries y el test FALLA: ese es
el bug que entrena este ejercicio.

Tu trabajo: implementar `listar_autores_con_libros` con eager loading
(joinedload o selectinload), de modo que el número de queries NO crezca con
el número de autores.

Corre el test:
    uv run pytest        # o simplemente:  pytest

Anota en bitacora.md qué estrategia elegiste, por qué, y cuántas queries
ejecuta la versión ingenua frente a la curada.
"""

from sqlalchemy.orm import Session


def listar_autores_con_libros(session: Session) -> list[dict]:
    """Devuelve una lista de dicts, uno por autor, con sus títulos de libro:

        [
            {"autor": "Autor 0", "libros": ["Libro 0-0", "Libro 0-1", ...]},
            {"autor": "Autor 1", "libros": [...]},
            ...
        ]

    DEBE resolverse en a lo más 2 queries, sin importar cuántos autores haya.

    Pista: una consulta normal `select(Autor)` trae los autores, pero acceder
    a `autor.libros` en un bucle dispara una query por autor (N+1). Carga la
    relación por adelantado con `.options(selectinload(...))` o
    `.options(joinedload(...))` — y recuerda el `.unique()` si usas joinedload
    sobre una colección.
    """
    raise NotImplementedError("implementa la consulta sin N+1")
