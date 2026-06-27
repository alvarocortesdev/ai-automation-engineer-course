"""Tests del gate de confianza + validación cruzada de un IDP.

Los datos extraídos se inyectan: los tests no dependen de ninguna API ni de un
servicio real. Verifican la LÓGICA de decisión (gate + validación + combinación).
"""

import pytest

from idp import clasificar_campos, total_cuadra, decidir_procesamiento

UMBRAL = 0.90

CAMPOS_OK = {
    "Proveedor": {"value": "ACME SpA", "confidence": 0.99},
    "Fecha": {"value": "2026-06-01", "confidence": 0.93},
    "Total": {"value": 90000, "confidence": 0.97},
}

ITEMS_90K = [
    {"descripcion": "Servicio A", "monto": 60000},
    {"descripcion": "Servicio B", "monto": 30000},
]


# ----- clasificar_campos -----

def test_clasificar_todos_auto():
    r = clasificar_campos(CAMPOS_OK, UMBRAL)
    assert r["auto"] == ["Proveedor", "Fecha", "Total"]
    assert r["revisar"] == []


def test_clasificar_uno_a_revisar():
    campos = {
        "Proveedor": {"value": "ACME", "confidence": 0.99},
        "Total": {"value": 90000, "confidence": 0.71},
    }
    r = clasificar_campos(campos, UMBRAL)
    assert r["auto"] == ["Proveedor"]
    assert r["revisar"] == ["Total"]


def test_clasificar_confidence_none_va_a_revisar():
    campos = {"RUT": {"value": "76.123.456-7", "confidence": None}}
    r = clasificar_campos(campos, UMBRAL)
    assert r["revisar"] == ["RUT"]
    assert r["auto"] == []


def test_clasificar_en_el_umbral_se_acepta():
    # confidence == umbral -> auto (la regla es >= umbral)
    campos = {"Fecha": {"value": "x", "confidence": 0.90}}
    r = clasificar_campos(campos, UMBRAL)
    assert r["auto"] == ["Fecha"]
    assert r["revisar"] == []


def test_clasificar_preserva_orden_de_entrada():
    campos = {
        "C": {"value": 1, "confidence": 0.99},
        "A": {"value": 2, "confidence": 0.50},
        "B": {"value": 3, "confidence": 0.99},
    }
    r = clasificar_campos(campos, UMBRAL)
    assert r["auto"] == ["C", "B"]
    assert r["revisar"] == ["A"]


def test_clasificar_vacio():
    assert clasificar_campos({}, UMBRAL) == {"auto": [], "revisar": []}


# ----- total_cuadra -----

def test_total_cuadra_exacto():
    assert total_cuadra(ITEMS_90K, 90000) is True


def test_total_no_cuadra():
    assert total_cuadra(ITEMS_90K, 100000) is False


def test_total_cuadra_con_tolerancia_de_floats():
    # 0.1 + 0.2 == 0.30000000000000004 ; un == directo fallaría, la tolerancia no
    items = [{"descripcion": "a", "monto": 0.1}, {"descripcion": "b", "monto": 0.2}]
    assert total_cuadra(items, 0.3) is True


def test_total_lista_vacia_y_cero():
    assert total_cuadra([], 0) is True


def test_total_tolerancia_personalizada():
    items = [{"descripcion": "a", "monto": 100.0}]
    assert total_cuadra(items, 100.5, tolerancia=1.0) is True
    assert total_cuadra(items, 102.0, tolerancia=1.0) is False


# ----- decidir_procesamiento -----

def test_decidir_auto_todo_limpio():
    doc = {"campos": CAMPOS_OK, "items": ITEMS_90K, "total_declarado": 90000}
    r = decidir_procesamiento(doc, UMBRAL)
    assert r["accion"] == "auto"
    assert r["motivos"] == []


def test_decidir_hitl_por_campo_dudoso():
    doc = {
        "campos": {
            "Proveedor": {"value": "ACME", "confidence": 0.99},
            "Total": {"value": 90000, "confidence": 0.71},
        },
        "items": ITEMS_90K,
        "total_declarado": 90000,
    }
    r = decidir_procesamiento(doc, UMBRAL)
    assert r["accion"] == "revision_humana"
    assert any("Total" in m for m in r["motivos"])


def test_decidir_hitl_por_total_descuadrado():
    # todos los campos pasan el gate, pero la aritmética no cuadra
    doc = {"campos": CAMPOS_OK, "items": ITEMS_90K, "total_declarado": 100000}
    r = decidir_procesamiento(doc, UMBRAL)
    assert r["accion"] == "revision_humana"
    assert any("total" in m.lower() for m in r["motivos"])


def test_decidir_acumula_ambos_motivos():
    doc = {
        "campos": {"Total": {"value": 100000, "confidence": 0.50}},
        "items": [{"descripcion": "a", "monto": 60000}],
        "total_declarado": 100000,
    }
    r = decidir_procesamiento(doc, UMBRAL)
    assert r["accion"] == "revision_humana"
    # un motivo por el campo dudoso + un motivo por el total descuadrado
    assert len(r["motivos"]) >= 2
