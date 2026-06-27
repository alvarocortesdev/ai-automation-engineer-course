"""Tests del estimador de costos — definen el contrato.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

No edites estos tests para "hacerlos pasar" cambiando el contrato: implementa
`estimador.py` hasta que pasen en verde. Sí AÑADE al menos un caso tuyo al final
(pensar en casos borde es parte del Primero-Sin-IA).
"""

import pytest

from estimador import estimar_costo_mensual

PRECIOS = {
    "storage_usd_por_gb_mes": 0.023,
    "egress_usd_por_gb": 0.09,
    "egress_gratis_gb": 100.0,
    "usd_por_millon_requests": 0.20,
}


def _arq(**overrides):
    """Arquitectura base; se sobreescribe lo que cada test necesite."""
    base = {
        "compute": [],
        "storage_gb": 0.0,
        "egress_gb": 0.0,
        "requests_millones": 0.0,
    }
    base.update(overrides)
    return base


def test_devuelve_desglose_con_todas_las_claves():
    out = estimar_costo_mensual(_arq(), PRECIOS)
    assert set(out.keys()) == {"compute", "storage", "egress", "requests", "total"}


def test_compute_suma_horas_por_recurso():
    arq = _arq(compute=[
        {"nombre": "api", "usd_por_hora": 0.02, "horas_encendido": 100},   # 2.00
        {"nombre": "nat", "usd_por_hora": 0.045, "horas_encendido": 730},  # 32.85
    ])
    out = estimar_costo_mensual(arq, PRECIOS)
    assert out["compute"] == pytest.approx(34.85)


def test_always_on_cuesta_mas_que_scale_to_zero():
    always_on = _arq(compute=[{"nombre": "vm", "usd_por_hora": 0.02, "horas_encendido": 730}])
    scale_zero = _arq(compute=[{"nombre": "fn", "usd_por_hora": 0.02, "horas_encendido": 50}])
    assert (estimar_costo_mensual(always_on, PRECIOS)["compute"]
            > estimar_costo_mensual(scale_zero, PRECIOS)["compute"])


def test_storage_por_gb_mes():
    out = estimar_costo_mensual(_arq(storage_gb=10.0), PRECIOS)
    assert out["storage"] == pytest.approx(0.23)


def test_egress_por_debajo_del_tramo_gratis_es_cero():
    out = estimar_costo_mensual(_arq(egress_gb=80.0), PRECIOS)
    assert out["egress"] == pytest.approx(0.0)


def test_egress_exacto_en_el_tramo_gratis_es_cero():
    out = estimar_costo_mensual(_arq(egress_gb=100.0), PRECIOS)
    assert out["egress"] == pytest.approx(0.0)


def test_egress_por_encima_del_tramo_gratis():
    # (150 - 100) * 0.09 = 4.5
    out = estimar_costo_mensual(_arq(egress_gb=150.0), PRECIOS)
    assert out["egress"] == pytest.approx(4.5)


def test_egress_nunca_es_negativo():
    out = estimar_costo_mensual(_arq(egress_gb=5.0), PRECIOS)
    assert out["egress"] >= 0.0


def test_requests_por_millon():
    out = estimar_costo_mensual(_arq(requests_millones=2.0), PRECIOS)
    assert out["requests"] == pytest.approx(0.40)


def test_total_es_la_suma_de_los_cuatro_drivers():
    arq = _arq(
        compute=[
            {"nombre": "api", "usd_por_hora": 0.02, "horas_encendido": 100},
            {"nombre": "nat", "usd_por_hora": 0.045, "horas_encendido": 730},
        ],
        storage_gb=10.0,
        egress_gb=80.0,
        requests_millones=2.0,
    )
    out = estimar_costo_mensual(arq, PRECIOS)
    # 34.85 + 0.23 + 0.0 + 0.40 = 35.48  (el NAT always-on domina el total)
    assert out["total"] == pytest.approx(35.48)
    assert out["total"] == pytest.approx(
        out["compute"] + out["storage"] + out["egress"] + out["requests"]
    )


# TODO(estudiante): añade al menos un caso borde tuyo. Sugerencia: un escenario
# "viral" donde el egress (no el storage) domina el total, o uno donde quitar el
# NAT Gateway always-on cambia el total drásticamente.
# def test_mi_caso_borde():
#     ...
