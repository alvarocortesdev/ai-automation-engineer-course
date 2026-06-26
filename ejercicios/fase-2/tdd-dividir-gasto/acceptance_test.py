"""Suite de aceptación — ÁBRELA SOLO AL FINAL.

Encierra los comportamientos del enunciado más las invariantes del reparto justo. NO es
tu trabajo de TDD: es el "golden master" para confirmar, una vez cerrados tus ciclos, que
no se te escapó nada. Si la abres antes, te pierdes lo que el ejercicio entrena (traducir
la spec a tests). Que pase NO sustituye a tu bitácora.

Corre:
    uv run pytest acceptance_test.py
"""

import pytest

from solucion import dividir_gasto


def test_division_exacta():
    assert dividir_gasto(100, 2) == [50, 50]


def test_resto_uno_a_la_primera():
    assert dividir_gasto(100, 3) == [34, 33, 33]


def test_resto_dos_a_las_primeras():
    assert dividir_gasto(10, 4) == [3, 3, 2, 2]


def test_monto_cero():
    assert dividir_gasto(0, 3) == [0, 0, 0]


def test_una_persona():
    assert dividir_gasto(100, 1) == [100]


def test_cero_personas_lanza_valueerror():
    with pytest.raises(ValueError):
        dividir_gasto(100, 0)


def test_monto_negativo_lanza_valueerror():
    with pytest.raises(ValueError):
        dividir_gasto(-100, 2)


@pytest.mark.parametrize("monto, personas", [(100, 3), (10, 4), (7, 3), (1234, 7), (1, 5)])
def test_invariantes_del_reparto_justo(monto, personas):
    partes = dividir_gasto(monto, personas)
    assert sum(partes) == monto                 # suma exacta
    assert len(partes) == personas              # una parte por persona
    assert max(partes) - min(partes) <= 1       # diferencia de a lo más 1 peso
