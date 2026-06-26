"""Tests del ejercicio 0.7 — Resumen de gastos por categoría.

Estos tests definen el CONTRATO de la función. Hazlos pasar todos en verde.
Luego AÑADE al menos un caso borde tuyo (pensar en casos borde es parte del
Primero-Sin-IA).

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""

import pytest

from gastos import total_por_categoria


def test_lista_vacia_devuelve_dict_vacio():
    assert total_por_categoria([]) == {}


def test_un_solo_gasto():
    assert total_por_categoria([{"categoria": "ocio", "monto": 9990}]) == {"ocio": 9990}


def test_agrupa_y_suma_por_categoria():
    gastos = [
        {"categoria": "comida", "monto": 5000},
        {"categoria": "comida", "monto": 3500},
        {"categoria": "transporte", "monto": 1200},
    ]
    assert total_por_categoria(gastos) == {"comida": 8500, "transporte": 1200}


def test_acepta_montos_float():
    gastos = [
        {"categoria": "café", "monto": 2.5},
        {"categoria": "café", "monto": 2.5},
    ]
    assert total_por_categoria(gastos) == {"café": 5.0}


def test_monto_negativo_lanza_valueerror():
    with pytest.raises(ValueError):
        total_por_categoria([{"categoria": "x", "monto": -1}])


def test_categoria_vacia_lanza_valueerror():
    with pytest.raises(ValueError):
        total_por_categoria([{"categoria": "", "monto": 10}])


# TODO(estudiante): añade aquí al menos un caso borde tuyo.
# def test_mi_caso_borde():
#     assert total_por_categoria(...) == ...
