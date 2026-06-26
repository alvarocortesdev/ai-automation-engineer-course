"""Tests del ejercicio 2.1 — paréntesis balanceados con stack.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

AÑADE al menos un caso borde tuyo. Idea: un anidamiento muy profundo, o un string
solo con caracteres que no son paréntesis.
"""

import pytest

from solucion import parentesis_balanceados


@pytest.mark.parametrize(
    "s, esperado",
    [
        ("()", True),
        ("([])", True),
        ("{[()]}", True),
        ("([)]", False),     # cierre cruzado
        ("(", False),        # apertura sin cerrar
        (")", False),        # cierre sin apertura
        ("", True),          # vacío
        ("a(b)c", True),     # ignora otros caracteres
        ("(()", False),      # una apertura queda sin cerrar
        ("())", False),      # un cierre sobra
    ],
)
def test_parentesis_balanceados(s, esperado):
    assert parentesis_balanceados(s) is esperado


def test_cierre_con_stack_vacio_no_revienta():
    # No debe lanzar IndexError: debe devolver False con elegancia.
    assert parentesis_balanceados("]") is False


# TODO(estudiante): añade aquí al menos un caso borde tuyo.
# def test_mi_caso_borde():
#     assert parentesis_balanceados(...) is ...
