"""Suite de aceptación — ÁBRELA SOLO AL FINAL.

Esta suite encierra los 7 comportamientos del enunciado. NO es tu trabajo de TDD:
es el "golden master" para confirmar, una vez cerrados tus ciclos, que no se te
escapó nada. Si la abres antes de escribir tus propios tests, te pierdes lo que el
ejercicio entrena (traducir la spec a tests). Que pase NO sustituye a tu bitácora.

Corre:
    uv run pytest acceptance_test.py
"""

import pytest

from solucion import sumar


def test_vacia_es_cero():
    assert sumar("") == 0


def test_un_numero():
    assert sumar("1") == 1


def test_dos_numeros():
    assert sumar("1,2") == 3


def test_cantidad_arbitraria():
    assert sumar("1,2,3,4") == 10


def test_salto_de_linea_separa():
    assert sumar("1\n2,3") == 6


def test_ignora_espacios():
    assert sumar(" 1 , 2 ") == 3


def test_negativo_lanza_valueerror_con_el_numero():
    with pytest.raises(ValueError, match="-2"):
        sumar("1,-2,3")
