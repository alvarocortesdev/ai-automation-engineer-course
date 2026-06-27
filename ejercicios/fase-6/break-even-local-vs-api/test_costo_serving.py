"""Tests del punto de equilibrio local vs API.

Todo el pricing se inyecta: los tests no dependen de ninguna API ni de precios reales.
Verifican la FÓRMULA y la lógica de equilibrio, no números mágicos de un proveedor.
"""

import pytest

from costo_serving import (
    costo_api_por_request,
    costo_api_mensual,
    punto_equilibrio_requests,
)


# Caso de referencia del README: 1000 tokens in + 1000 out, precios 0.20 / 0.80 por 1M.
# costo por request = 1000/1e6*0.20 + 1000/1e6*0.80 = 0.0002 + 0.0008 = 0.001 USD
IN, OUT = 1_000, 1_000
P_IN, P_OUT = 0.20, 0.80


def test_costo_por_request():
    assert costo_api_por_request(IN, OUT, P_IN, P_OUT) == pytest.approx(0.001)


def test_salida_pesa_mas_que_entrada():
    # mismos tokens en cada lado: el lado de salida cuesta más (precio out > in)
    solo_in = costo_api_por_request(1_000, 0, P_IN, P_OUT)
    solo_out = costo_api_por_request(0, 1_000, P_IN, P_OUT)
    assert solo_out > solo_in


def test_cero_tokens_cuesta_cero():
    assert costo_api_por_request(0, 0, P_IN, P_OUT) == 0.0


def test_costo_mensual_es_lineal():
    # mensual = por_request * requests
    por_req = costo_api_por_request(IN, OUT, P_IN, P_OUT)
    assert costo_api_mensual(50_000, IN, OUT, P_IN, P_OUT) == pytest.approx(por_req * 50_000)


def test_punto_equilibrio_del_readme():
    # GPU a 1 USD/h * 730 h = 730 USD/mes ; costo por request = 0.001
    # equilibrio = 730 / 0.001 = 730_000 requests/mes
    eq = punto_equilibrio_requests(730.0, IN, OUT, P_IN, P_OUT)
    assert eq == pytest.approx(730_000)


def test_en_el_equilibrio_ambos_cuestan_igual():
    costo_local = 730.0
    eq = punto_equilibrio_requests(costo_local, IN, OUT, P_IN, P_OUT)
    # a exactamente `eq` requests, la API cuesta lo mismo que el costo local fijo
    assert costo_api_mensual(round(eq), IN, OUT, P_IN, P_OUT) == pytest.approx(costo_local)


def test_por_debajo_gana_la_api():
    costo_local = 730.0
    eq = punto_equilibrio_requests(costo_local, IN, OUT, P_IN, P_OUT)
    requests_bajos = round(eq) // 2
    # con la mitad de los requests del equilibrio, la API cuesta menos que la GPU fija
    assert costo_api_mensual(requests_bajos, IN, OUT, P_IN, P_OUT) < costo_local


def test_por_encima_gana_local():
    costo_local = 730.0
    eq = punto_equilibrio_requests(costo_local, IN, OUT, P_IN, P_OUT)
    requests_altos = round(eq) * 2
    # al doble del equilibrio, la API cuesta más que la GPU fija -> local gana
    assert costo_api_mensual(requests_altos, IN, OUT, P_IN, P_OUT) > costo_local


def test_api_gratis_no_tiene_equilibrio():
    # costo por request = 0 -> no hay número de requests que iguale un costo local positivo
    with pytest.raises(ValueError):
        punto_equilibrio_requests(730.0, 0, 0, P_IN, P_OUT)
