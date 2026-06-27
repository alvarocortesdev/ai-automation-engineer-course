"""Tests para la calculadora de costo.

El pricing se inyecta: los tests no dependen de ninguna API ni de precios reales.
Verifican la FÓRMULA y la política de elección, no números mágicos de un proveedor.
"""

import pytest

from costo import calcular_costo, modelo_mas_barato


# Tabla de precios de referencia (USD por millón de tokens). Solo para los tests.
PRECIOS = {
    "opus": {"in": 5, "out": 25},
    "sonnet": {"in": 3, "out": 15},
    "haiku": {"in": 1, "out": 5},
}


def test_costo_opus():
    # 10000/1e6*5 + 2000/1e6*25 = 0.05 + 0.05 = 0.10
    assert calcular_costo(10_000, 2_000, "opus", PRECIOS) == pytest.approx(0.10)


def test_costo_sonnet():
    assert calcular_costo(10_000, 2_000, "sonnet", PRECIOS) == pytest.approx(0.06)


def test_costo_haiku():
    assert calcular_costo(10_000, 2_000, "haiku", PRECIOS) == pytest.approx(0.02)


def test_salida_pesa_mas_que_entrada():
    # mismos tokens en cada lado: el lado de salida cuesta más (precio out > in)
    solo_entrada = calcular_costo(1_000, 0, "opus", PRECIOS)
    solo_salida = calcular_costo(0, 1_000, "opus", PRECIOS)
    assert solo_salida > solo_entrada


def test_cero_tokens_cuesta_cero():
    assert calcular_costo(0, 0, "haiku", PRECIOS) == 0.0


def test_modelo_desconocido_falla():
    with pytest.raises((KeyError, ValueError)):
        calcular_costo(100, 100, "gpt-inventado", PRECIOS)


def test_mas_barato_es_haiku():
    assert modelo_mas_barato(10_000, 2_000, PRECIOS) == "haiku"


def test_mas_barato_depende_de_la_proporcion_in_out():
    # un modelo barato para leer pero caro para escribir, y otro al revés:
    # el "más barato" cambia según la carga.
    precios = {
        "barato_in": {"in": 1, "out": 100},   # barato leer, carísimo escribir
        "barato_out": {"in": 100, "out": 1},  # carísimo leer, barato escribir
    }
    # mucha SALIDA -> gana el barato para escribir
    assert modelo_mas_barato(1, 1_000, precios) == "barato_out"
    # mucha ENTRADA -> gana el barato para leer
    assert modelo_mas_barato(1_000, 1, precios) == "barato_in"


def test_precios_vacio_falla():
    with pytest.raises(ValueError):
        modelo_mas_barato(100, 100, {})
