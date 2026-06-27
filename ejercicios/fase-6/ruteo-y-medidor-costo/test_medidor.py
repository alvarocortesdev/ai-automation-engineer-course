"""Tests del medidor de costo + router.

Los precios se inyectan: los tests no dependen de ninguna API ni de precios reales.
Verifican la FÓRMULA (con las tres tarifas de input) y la política de ruteo, no
números mágicos de un proveedor.

Ejecuta:
    pytest
"""
import pytest

from medidor import Request, Usage, costo_mensual, costo_usd, rutear_modelo

# Precios de referencia (USD por millón, in / out). Solo para los tests.
PRECIOS = {
    "haiku": {"in": 1, "out": 5},
    "sonnet": {"in": 3, "out": 15},
    "opus": {"in": 5, "out": 25},
}
ESCALONES = [(0.3, "haiku"), (0.7, "sonnet"), (1.0, "opus")]


# ── costo_usd ──────────────────────────────────────────────────────────────

def test_costo_solo_input_y_output():
    # 10000/1e6*5 + 2000/1e6*25 = 0.05 + 0.05 = 0.10  (igual que el caso de 6.3)
    u = Usage(input_tokens=10_000, output_tokens=2_000)
    assert costo_usd(u, 5.0, 25.0) == pytest.approx(0.10)


def test_cache_read_cuesta_un_decimo():
    # input fresco 2000 + cache_read 10000 (a 0.1x) + output 500, en opus 5/25
    # = 2000/1e6*5 + 10000/1e6*5*0.1 + 500/1e6*25 = 0.010 + 0.005 + 0.0125 = 0.0275
    u = Usage(input_tokens=2_000, cache_read_input_tokens=10_000, output_tokens=500)
    assert costo_usd(u, 5.0, 25.0) == pytest.approx(0.0275)


def test_cache_read_es_mas_barato_que_input_fresco():
    # los MISMOS tokens como cache read deben costar menos que como input fresco
    fresco = costo_usd(Usage(input_tokens=10_000), 5.0, 25.0)
    cacheado = costo_usd(Usage(cache_read_input_tokens=10_000), 5.0, 25.0)
    assert cacheado < fresco
    assert cacheado == pytest.approx(fresco * 0.1)


def test_cache_write_tiene_premium():
    # cache write cuesta 1.25x: más caro que el mismo volumen como input fresco
    fresco = costo_usd(Usage(input_tokens=10_000), 5.0, 25.0)
    escrito = costo_usd(Usage(cache_creation_input_tokens=10_000), 5.0, 25.0)
    assert escrito == pytest.approx(fresco * 1.25)
    assert escrito > fresco


def test_cero_tokens_cuesta_cero():
    assert costo_usd(Usage(), 5.0, 25.0) == 0.0


# ── rutear_modelo ──────────────────────────────────────────────────────────

def test_ruteo_facil_va_a_haiku():
    assert rutear_modelo(0.2, ESCALONES) == "haiku"


def test_ruteo_borde_exacto_entra_en_el_escalon():
    # 0.3 exacto debe caer en haiku (techo >= dificultad incluye el igual)
    assert rutear_modelo(0.3, ESCALONES) == "haiku"


def test_ruteo_medio_va_a_sonnet():
    assert rutear_modelo(0.5, ESCALONES) == "sonnet"


def test_ruteo_dificil_va_a_opus():
    assert rutear_modelo(0.9, ESCALONES) == "opus"


def test_ruteo_fuera_de_rango_usa_el_mas_capaz():
    assert rutear_modelo(1.4, ESCALONES) == "opus"


def test_ruteo_escalones_vacio_falla():
    with pytest.raises(ValueError):
        rutear_modelo(0.5, [])


# ── costo_mensual ──────────────────────────────────────────────────────────

def test_costo_mensual_total_y_desglose():
    trafico = [
        Request(dificultad=0.2, usage=Usage(input_tokens=1_000, output_tokens=100)),  # haiku
        Request(dificultad=0.5, usage=Usage(input_tokens=1_000, output_tokens=100)),  # sonnet
        Request(dificultad=0.9, usage=Usage(input_tokens=1_000, output_tokens=100)),  # opus
    ]
    r = costo_mensual(trafico, ESCALONES, PRECIOS)

    # costos individuales (1000 in / 100 out por modelo)
    c_haiku = 1_000 / 1e6 * 1 + 100 / 1e6 * 5      # 0.001 + 0.0005 = 0.0015
    c_sonnet = 1_000 / 1e6 * 3 + 100 / 1e6 * 15    # 0.003 + 0.0015 = 0.0045
    c_opus = 1_000 / 1e6 * 5 + 100 / 1e6 * 25      # 0.005 + 0.0025 = 0.0075

    assert r["por_modelo"]["haiku"] == pytest.approx(c_haiku)
    assert r["por_modelo"]["sonnet"] == pytest.approx(c_sonnet)
    assert r["por_modelo"]["opus"] == pytest.approx(c_opus)
    assert r["total"] == pytest.approx(c_haiku + c_sonnet + c_opus)


def test_costo_mensual_agrega_requests_del_mismo_modelo():
    # dos requests fáciles -> ambas a haiku -> el desglose suma las dos
    trafico = [
        Request(dificultad=0.1, usage=Usage(input_tokens=1_000)),
        Request(dificultad=0.2, usage=Usage(input_tokens=1_000)),
    ]
    r = costo_mensual(trafico, ESCALONES, PRECIOS)
    assert r["por_modelo"]["haiku"] == pytest.approx(2 * (1_000 / 1e6 * 1))
    assert r["total"] == pytest.approx(r["por_modelo"]["haiku"])


# TODO(estudiante): añade aquí al menos un caso borde tuyo.
# def test_mi_caso_borde():
#     ...
