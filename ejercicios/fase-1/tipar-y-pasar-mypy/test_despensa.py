"""Tests del ejercicio 1.4 — Tipar un módulo y hacer pasar mypy --strict.

Estos tests son el CONTRATO de comportamiento. En el starter SIN arreglar,
los tres primeros pasan y el último (item sin descuento) revienta en runtime
con un TypeError: ese es justamente el bug que mypy --strict te avisa antes.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

Y la verificación estática (parte central del ejercicio):
    uv run mypy --strict despensa.py
"""

from despensa import descuento, total_despensa


def test_descuento_sin_rebaja():
    assert descuento(1000, 0) == 1000


def test_descuento_aplica_porcentaje():
    assert descuento(1000, 25) == 750


def test_total_suma_items_con_descuento():
    items = [{"precio": 1000, "descuento_pct": 10}, {"precio": 500, "descuento_pct": 0}]
    assert total_despensa(items) == 1400  # 900 + 500


def test_item_sin_descuento_se_trata_como_cero():
    # El item sin 'descuento_pct' debe contar como 0% de descuento, no reventar.
    # En el starter sin arreglar, item.get("descuento_pct") devuelve None y
    # `precio * None` lanza TypeError. mypy --strict lo predijo: int | None vs int.
    items = [{"precio": 1000}, {"precio": 500, "descuento_pct": 20}]
    assert total_despensa(items) == 1400  # 1000 + 400


# TODO(estudiante): añade aquí al menos un caso borde tuyo (p. ej. lista vacía).
