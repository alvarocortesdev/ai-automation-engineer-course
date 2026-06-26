"""Tests del ejercicio 1.1 — Inventario idiomático, empaquetado.

Estos tests definen el CONTRATO. Hazlos pasar todos en verde. Luego AÑADE al
menos un caso borde tuyo (pensar en casos borde es parte del Primero-Sin-IA).

Ejecuta desde la carpeta del ejercicio:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""

import pytest

# Import desde el MÓDULO (despensa/inventario.py)
from despensa.inventario import resumen_inventario, formatear_lineas

# Import desde el PAQUETE (requiere que __init__.py re-exporte)
import despensa


PRODUCTOS = [
    {"nombre": "café", "precio": 2500, "stock": 3},
    {"nombre": "té", "precio": 1800, "stock": 0},
    {"nombre": "azúcar", "precio": 1200, "stock": 5},
]


# ── resumen_inventario ─────────────────────────────────────────────────────


def test_lista_vacia():
    assert resumen_inventario([]) == {"unidades": 0, "valor": 0, "agotados": []}


def test_resumen_completo():
    assert resumen_inventario(PRODUCTOS) == {
        "unidades": 8,
        "valor": 13500,
        "agotados": ["té"],
    }


def test_sin_agotados():
    productos = [{"nombre": "café", "precio": 2500, "stock": 3}]
    assert resumen_inventario(productos)["agotados"] == []


def test_acepta_precio_float():
    productos = [{"nombre": "café", "precio": 2.5, "stock": 2}]
    assert resumen_inventario(productos)["valor"] == 5.0


def test_stock_negativo_lanza_valueerror():
    with pytest.raises(ValueError):
        resumen_inventario([{"nombre": "x", "precio": 10, "stock": -1}])


def test_precio_negativo_lanza_valueerror():
    with pytest.raises(ValueError):
        resumen_inventario([{"nombre": "x", "precio": -10, "stock": 1}])


# ── formatear_lineas ───────────────────────────────────────────────────────


def test_formatear_lista_vacia():
    assert formatear_lineas([]) == []


def test_formatear_numera_desde_uno():
    assert formatear_lineas(PRODUCTOS) == [
        "1. café — $2500 (x3)",
        "2. té — $1800 (x0)",
        "3. azúcar — $1200 (x5)",
    ]


# ── empaquetado ────────────────────────────────────────────────────────────


def test_import_desde_paquete():
    # Si esto falla con ImportError/AttributeError, tu __init__.py no re-exporta.
    assert despensa.resumen_inventario(PRODUCTOS)["unidades"] == 8
    assert despensa.formatear_lineas([])[:] == []


# TODO(estudiante): añade aquí al menos un caso borde tuyo.
# def test_mi_caso_borde():
#     assert resumen_inventario(...) == ...
