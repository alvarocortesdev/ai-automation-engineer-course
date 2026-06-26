"""Tests del ejercicio 1.4 — Validar la salida de un LLM con pydantic.

Estos tests son el CONTRATO. Cada uno corresponde a una forma en que un LLM puede
darte una salida buena... o mala. Hazlos pasar todos y luego AÑADE un caso borde tuyo.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest + pydantic en el entorno
"""

import json
from datetime import date

import pytest
from pydantic import ValidationError

from compra import Compra, parsear_compra

VALIDO = json.dumps(
    {
        "comercio": "Lider",
        "monto": 12990,
        "categoria": "supermercado",
        "fecha": "2026-06-20",
        "items": ["leche", "pan"],
    }
)


def _con(**cambios):
    """Devuelve el JSON válido con algunos campos cambiados/añadidos (para los casos malos)."""
    base = {
        "comercio": "Lider",
        "monto": 100,
        "categoria": "supermercado",
        "fecha": "2026-06-20",
        "items": ["leche"],
    }
    base.update(cambios)
    return json.dumps(base)


def test_parsea_json_valido():
    c = parsear_compra(VALIDO)
    assert isinstance(c, Compra)
    assert c.comercio == "Lider"
    assert c.monto == 12990
    assert c.categoria == "supermercado"
    assert c.fecha == date(2026, 6, 20)
    assert c.items == ["leche", "pan"]


def test_coerciona_monto_string_a_int():
    c = parsear_compra(_con(monto="12990"))
    assert c.monto == 12990
    assert isinstance(c.monto, int)


def test_monto_negativo_es_rechazado():
    with pytest.raises(ValidationError):
        parsear_compra(_con(monto=-5))


def test_monto_cero_es_rechazado():
    with pytest.raises(ValidationError):
        parsear_compra(_con(monto=0))


def test_comercio_solo_espacios_es_rechazado():
    with pytest.raises(ValidationError):
        parsear_compra(_con(comercio="   "))


def test_categoria_vacia_es_rechazada():
    with pytest.raises(ValidationError):
        parsear_compra(_con(categoria=""))


def test_items_vacio_es_rechazado():
    with pytest.raises(ValidationError):
        parsear_compra(_con(items=[]))


def test_fecha_invalida_es_rechazada():
    with pytest.raises(ValidationError):
        parsear_compra(_con(fecha="ayer"))


def test_campo_alucinado_es_rechazado():
    # El LLM inventó un campo "confianza" que nunca pedimos: debe fallar, no pasar en silencio.
    with pytest.raises(ValidationError):
        parsear_compra(_con(confianza=0.99))


# TODO(estudiante): añade aquí al menos un caso borde tuyo que un LLM podría producir.
# Ideas: monto como float "12990.5", items con un string vacío, comercio faltante.
