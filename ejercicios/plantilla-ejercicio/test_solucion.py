"""Tests de ejemplo del ejercicio.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

Estos tests definen el contrato. Para esta plantilla, el ejercicio es pasar texto
a mayúsculas (incluido el caso borde del string vacío). En un ejercicio real,
reemplázalos por los casos que correspondan y AÑADE al menos un caso tuyo: pensar
en casos borde es parte del Primero-Sin-IA.
"""

import pytest

from solucion import resolver


def test_caso_basico():
    assert resolver("hola") == "HOLA"


def test_caso_borde_vacio():
    # El string vacío debe devolver string vacío, no error.
    assert resolver("") == ""


@pytest.mark.parametrize(
    "entrada,esperado",
    [
        ("a", "A"),
        ("Mundo", "MUNDO"),
        ("123 go", "123 GO"),
    ],
)
def test_casos_parametrizados(entrada, esperado):
    assert resolver(entrada) == esperado


# TODO(estudiante): añade aquí al menos un caso borde tuyo.
# def test_mi_caso_borde():
#     assert resolver(...) == ...
