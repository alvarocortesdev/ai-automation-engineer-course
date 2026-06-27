"""Tests del punto de equilibrio fine-tuning vs baseline (prompt largo).

Todo el pricing se inyecta: los tests no dependen de ninguna API ni de precios reales.
Verifican la FORMULA y la logica de equilibrio, no numeros magicos de un proveedor.
"""

import pytest

from costo_finetuning import (
    costo_por_request,
    costo_total,
    requests_equilibrio_finetuning,
)


# Caso de referencia del README.
# BASELINE: prompt largo de few-shot = 2000 tokens in + 200 out, precios 0.40 / 1.60 por 1M.
#   c_base = 2000/1e6*0.40 + 200/1e6*1.60 = 0.0008 + 0.00032 = 0.00112 USD
# FINE-TUNING: prompt corto = 200 in + 200 out, modelo mas caro por token: 0.60 / 2.40.
#   c_ft   = 200/1e6*0.60 + 200/1e6*2.40 = 0.00012 + 0.00048 = 0.0006 USD
#   ahorro por request = 0.00112 - 0.0006 = 0.00052 USD
#   costo de entrenamiento = 26 USD  ->  equilibrio = 26 / 0.00052 = 50_000 requests
BASE_IN, BASE_OUT = 2_000, 200
P_IN, P_OUT = 0.40, 1.60

FT_IN, FT_OUT = 200, 200
P_IN_FT, P_OUT_FT = 0.60, 2.40

COSTO_ENTRENAMIENTO = 26.0


def _c_base() -> float:
    return costo_por_request(BASE_IN, BASE_OUT, P_IN, P_OUT)


def _c_ft() -> float:
    return costo_por_request(FT_IN, FT_OUT, P_IN_FT, P_OUT_FT)


def test_costo_por_request_baseline():
    assert _c_base() == pytest.approx(0.00112)


def test_costo_por_request_fine_tuned():
    assert _c_ft() == pytest.approx(0.0006)


def test_prompt_corto_reduce_el_costo_de_entrada():
    # mismo modelo/precio, solo cambia el largo del prompt: menos tokens in -> mas barato
    largo = costo_por_request(2_000, 200, P_IN, P_OUT)
    corto = costo_por_request(200, 200, P_IN, P_OUT)
    assert corto < largo


def test_costo_total_baseline_sin_costo_fijo():
    # baseline no tiene entrenamiento: costo_fijo = 0
    assert costo_total(0.0, _c_base(), 50_000) == pytest.approx(56.0)


def test_costo_total_finetuning_incluye_entrenamiento():
    # 26 (entrenamiento) + 50_000 * 0.0006 = 26 + 30 = 56
    assert costo_total(COSTO_ENTRENAMIENTO, _c_ft(), 50_000) == pytest.approx(56.0)


def test_punto_equilibrio_del_readme():
    eq = requests_equilibrio_finetuning(COSTO_ENTRENAMIENTO, _c_base(), _c_ft())
    assert eq == pytest.approx(50_000)


def test_en_el_equilibrio_ambos_cuestan_igual():
    eq = requests_equilibrio_finetuning(COSTO_ENTRENAMIENTO, _c_base(), _c_ft())
    n = round(eq)
    total_base = costo_total(0.0, _c_base(), n)
    total_ft = costo_total(COSTO_ENTRENAMIENTO, _c_ft(), n)
    assert total_ft == pytest.approx(total_base)


def test_por_debajo_gana_el_baseline():
    eq = requests_equilibrio_finetuning(COSTO_ENTRENAMIENTO, _c_base(), _c_ft())
    n = round(eq) // 2
    # a la mitad del equilibrio, el costo fijo de entrenamiento no se amortizo: baseline gana
    assert costo_total(0.0, _c_base(), n) < costo_total(COSTO_ENTRENAMIENTO, _c_ft(), n)


def test_por_encima_gana_el_finetuning():
    eq = requests_equilibrio_finetuning(COSTO_ENTRENAMIENTO, _c_base(), _c_ft())
    n = round(eq) * 2
    # al doble del equilibrio, el prompt corto ya pago el entrenamiento: fine-tuning gana
    assert costo_total(COSTO_ENTRENAMIENTO, _c_ft(), n) < costo_total(0.0, _c_base(), n)


def test_si_el_finetuning_no_es_mas_barato_no_hay_equilibrio():
    # modelo fine-tuneado mas caro por request que el baseline -> ahorro <= 0 -> ValueError
    c_base = 0.0006
    c_ft_caro = 0.0008
    with pytest.raises(ValueError):
        requests_equilibrio_finetuning(COSTO_ENTRENAMIENTO, c_base, c_ft_caro)


def test_ahorro_cero_tampoco_tiene_equilibrio():
    # mismo costo por request -> nunca se recupera el costo fijo -> ValueError
    with pytest.raises(ValueError):
        requests_equilibrio_finetuning(COSTO_ENTRENAMIENTO, 0.001, 0.001)
