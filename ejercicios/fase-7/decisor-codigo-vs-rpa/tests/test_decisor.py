"""Tests del decisor de estrategia de automatización.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

Estos tests definen el contrato de la escalera de integración. Cada caso fija una
combinación de flags y la estrategia esperada. AÑADE al menos un caso tuyo al final:
pensar en combinaciones borde es parte del Primero-Sin-IA.
"""

import sys
from pathlib import Path

import pytest

# Permite `from decisor import ...` aunque corras pytest desde la raíz del repo.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from decisor import Caso, Recomendacion, recomendar_automatizacion


def _caso(**kwargs) -> Caso:
    """Crea un Caso con defaults razonables; sobreescribe solo lo relevante."""
    base = dict(
        tiene_api=False,
        es_web=False,
        volumen_alto=False,
        critico=False,
        ui_cambia_seguido=False,
    )
    base.update(kwargs)
    return Caso(**base)


def test_api_gana_siempre():
    r = recomendar_automatizacion(_caso(tiene_api=True))
    assert r.estrategia == "api"


def test_api_gana_aunque_haya_otras_flags():
    # Aunque sea web, crítico, alto volumen y la UI cambie: si hay API, es "api".
    r = recomendar_automatizacion(
        _caso(tiene_api=True, es_web=True, volumen_alto=True, critico=True, ui_cambia_seguido=True)
    )
    assert r.estrategia == "api"


def test_web_sin_api_no_critico_es_navegador():
    r = recomendar_automatizacion(_caso(es_web=True))
    assert r.estrategia == "navegador"


def test_ni_api_ni_web_no_critico_es_rpa_ui():
    r = recomendar_automatizacion(_caso(es_web=False))
    assert r.estrategia == "rpa-ui"


def test_sin_api_y_critico_se_rediseña():
    # Crítico sin API: la UI-automation no es base aceptable.
    r = recomendar_automatizacion(_caso(es_web=True, critico=True))
    assert r.estrategia == "rediseñar-proceso"


def test_sin_api_y_alto_volumen_se_rediseña():
    r = recomendar_automatizacion(_caso(es_web=False, volumen_alto=True))
    assert r.estrategia == "rediseñar-proceso"


def test_motivo_no_esta_vacio_y_no_es_solo_la_estrategia():
    r = recomendar_automatizacion(_caso(es_web=True))
    assert isinstance(r, Recomendacion)
    assert r.motivo.strip() != ""
    # El motivo debe EXPLICAR, no solo repetir la palabra de la estrategia.
    assert r.motivo.strip().lower() != r.estrategia.lower()


@pytest.mark.parametrize(
    "kwargs,esperado",
    [
        (dict(tiene_api=True), "api"),
        (dict(es_web=True), "navegador"),
        (dict(es_web=False), "rpa-ui"),
        (dict(es_web=True, critico=True), "rediseñar-proceso"),
        (dict(es_web=False, volumen_alto=True), "rediseñar-proceso"),
    ],
)
def test_tabla_de_decision(kwargs, esperado):
    assert recomendar_automatizacion(_caso(**kwargs)).estrategia == esperado


# TODO(estudiante): añade al menos un caso borde tuyo.
# Idea: ¿qué pasa si ui_cambia_seguido=True con es_web=True (no crítico)?
# ¿Tu motivo debería advertir sobre el costo de mantención? Decídelo y testéalo.
