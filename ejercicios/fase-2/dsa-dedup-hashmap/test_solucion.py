"""Tests del ejercicio 2.1 — two-sum con hashmap.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

Estos tests definen el contrato. AÑADE al menos un caso borde tuyo: pensar en
casos borde es parte del Primero-Sin-IA. (Idea: ¿qué pasa con números negativos,
o con el mismo valor en muchas posiciones?)
"""

import pytest

from solucion import tiene_dos_que_suman


@pytest.mark.parametrize(
    "nums, objetivo, esperado",
    [
        ([2, 7, 11, 15], 9, True),    # 2 + 7
        ([3, 3], 6, True),            # dos posiciones distintas, valor repetido
        ([1], 2, False),              # hace falta DOS posiciones
        ([], 0, False),               # lista vacía
        ([1, 5, 9], 8, False),        # ningún par suma 8
        ([0, 4, 3, 0], 0, True),      # 0 + 0 en dos posiciones
        ([-3, 1, 4], 1, True),        # -3 + 4
    ],
)
def test_tiene_dos_que_suman(nums, objetivo, esperado):
    assert tiene_dos_que_suman(nums, objetivo) is esperado


def test_no_empareja_un_elemento_consigo_mismo():
    # 5 aparece una sola vez: no puede sumarse a sí mismo para dar 10.
    assert tiene_dos_que_suman([5, 1, 2], 10) is False


# TODO(estudiante): añade aquí al menos un caso borde tuyo.
# def test_mi_caso_borde():
#     assert tiene_dos_que_suman(...) is ...
