"""Tests del ejercicio 0.8 — Spec-first: divisor de cuenta.

Estos tests son el CONTRATO escrito en código. Cada uno debería corresponder a una
fila de tu `spec.md` (entradas / salida / casos borde). Hazlos pasar todos en verde
y luego AÑADE al menos un caso borde tuyo: pensar los bordes es parte del spec-first.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""

import pytest

from dividir_cuenta import dividir_cuenta


def test_reparte_en_partes_iguales():
    assert dividir_cuenta(100, 4) == 25.0


def test_una_sola_persona_paga_todo():
    assert dividir_cuenta(50, 1) == 50.0


def test_division_no_exacta_devuelve_float_completo():
    # 100 / 3 = 33.333...  No se redondea: lo comparamos con tolerancia.
    assert dividir_cuenta(100, 3) == pytest.approx(100 / 3)


def test_total_cero_es_valido():
    assert dividir_cuenta(0, 3) == 0.0


def test_total_negativo_lanza_value_error():
    with pytest.raises(ValueError):
        dividir_cuenta(-1000, 2)


def test_cero_personas_lanza_value_error():
    # Debe ser ValueError (validación propia), NO ZeroDivisionError.
    with pytest.raises(ValueError):
        dividir_cuenta(100, 0)


def test_personas_negativas_lanza_value_error():
    with pytest.raises(ValueError):
        dividir_cuenta(100, -2)


# TODO(estudiante): añade aquí al menos un caso borde tuyo, tomado de tu spec.md.
# def test_mi_caso_borde():
#     assert dividir_cuenta(...) == ...
