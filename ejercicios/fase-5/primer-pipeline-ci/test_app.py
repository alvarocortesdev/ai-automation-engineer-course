"""Tests del módulo de ejemplo (`app.py`).

Estos son los tests que TU pipeline de CI debe correr. Ya pasan en verde;
no los toques. Tu trabajo es que el workflow los ejecute en un runner limpio.
"""

import pytest

from app import es_palindromo


@pytest.mark.parametrize(
    "entrada,esperado",
    [
        ("anita lava la tina", True),
        ("hola mundo", False),
        ("oso", True),
        ("", True),            # caso borde: el string vacío es palíndromo
        ("a", True),
    ],
)
def test_es_palindromo(entrada, esperado):
    assert es_palindromo(entrada) == esperado
