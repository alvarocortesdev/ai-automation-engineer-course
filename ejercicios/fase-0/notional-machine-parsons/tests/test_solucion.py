"""Tests del Parsons `promedio`.

Corre con:  uv run pytest   (o  pytest)

Estos tests definen el contrato. Tu función reordenada debe pasarlos TODOS,
incluido el caso borde de la lista vacía. Al final, agrega un test tuyo.
"""

import pytest

from solucion import promedio


def test_promedio_basico():
    assert promedio([2, 4, 6]) == 4.0


def test_promedio_un_elemento():
    assert promedio([7]) == 7.0


def test_promedio_lista_vacia_devuelve_cero():
    # El caso borde: NO debe lanzar ZeroDivisionError.
    assert promedio([]) == 0.0


def test_promedio_no_revienta_con_vacia():
    # Redundante a propósito: blinda el contrato del caso borde.
    try:
        promedio([])
    except ZeroDivisionError:
        pytest.fail("promedio([]) no debe dividir entre cero; debe devolver 0.0")


def test_promedio_devuelve_float():
    assert isinstance(promedio([1, 2]), float)


# TODO (tú): agrega aquí un test propio. Sugerencia: números negativos
# (p. ej. promedio([-2, -4]) == -3.0) o decimales.
