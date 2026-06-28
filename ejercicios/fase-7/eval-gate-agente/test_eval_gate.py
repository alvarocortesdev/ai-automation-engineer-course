"""Tests del eval gate — definen el contrato.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

No edites estos tests para "hacerlos pasar" cambiando el contrato: implementa
`eval_gate.py` hasta que pasen en verde.
"""

import pytest

from eval_gate import evaluar, gate


def test_evaluar_caso_perfecto():
    preds = [
        {"input_id": "1", "categoria": "reembolso", "campos": {"monto": 100, "id": "A"}},
        {"input_id": "2", "categoria": "consulta", "campos": {}},
    ]
    esperado = {
        "1": {"categoria": "reembolso", "campos": {"monto": 100, "id": "A"}},
        "2": {"categoria": "consulta", "campos": {}},
    }
    m = evaluar(preds, esperado)
    assert m["accuracy_categoria"] == pytest.approx(1.0)
    assert m["exactitud_campos"] == pytest.approx(1.0)
    assert m["n"] == 2


def test_evaluar_caso_mixto():
    preds = [
        {"input_id": "1", "categoria": "reembolso", "campos": {"monto": 100, "id": "A"}},
        {"input_id": "2", "categoria": "otro", "campos": {"x": 1}},      # cat mal, campo mal
        {"input_id": "3", "categoria": "consulta", "campos": {"y": 5}},  # cat bien, campo bien
    ]
    esperado = {
        "1": {"categoria": "reembolso", "campos": {"monto": 100, "id": "A"}},  # 2 campos
        "2": {"categoria": "consulta", "campos": {"x": 2}},                    # 1 campo
        "3": {"categoria": "consulta", "campos": {"y": 5}},                    # 1 campo
    }
    m = evaluar(preds, esperado)
    # 2 de 3 categorias correctas
    assert m["accuracy_categoria"] == pytest.approx(2 / 3)
    # campos correctos: input1 (2) + input2 (0) + input3 (1) = 3 de 4 esperados
    assert m["exactitud_campos"] == pytest.approx(0.75)
    assert m["n"] == 3


def test_evaluar_lista_vacia_no_revienta():
    m = evaluar([], {})
    assert m["n"] == 0
    # convención de verdad vacua: sin items, nada falló
    assert m["accuracy_categoria"] == pytest.approx(1.0)
    assert m["exactitud_campos"] == pytest.approx(1.0)


def test_gate_pasa_sobre_umbral_sin_baseline():
    m = {"accuracy_categoria": 0.95, "exactitud_campos": 0.9, "n": 100}
    out = gate(m, umbral_categoria=0.90)
    assert out["pasa"] is True


def test_gate_bloquea_bajo_umbral():
    m = {"accuracy_categoria": 0.85, "exactitud_campos": 0.9, "n": 100}
    out = gate(m, umbral_categoria=0.90)
    assert out["pasa"] is False
    assert "umbral" in out["motivo"]            # el motivo identifica que fue por el umbral


def test_gate_bloquea_por_regresion_aunque_supere_umbral():
    # 0.92 supera el umbral 0.90, pero ES una regresión vs baseline 0.95 -> bloquea
    m = {"accuracy_categoria": 0.92, "exactitud_campos": 0.9, "n": 100}
    baseline = {"accuracy_categoria": 0.95}
    out = gate(m, umbral_categoria=0.90, baseline=baseline)
    assert out["pasa"] is False
    assert "regres" in out["motivo"].lower()    # el motivo identifica que fue regresión


def test_gate_pasa_si_iguala_o_mejora_el_baseline():
    m = {"accuracy_categoria": 0.96, "exactitud_campos": 0.9, "n": 100}
    baseline = {"accuracy_categoria": 0.95}
    out = gate(m, umbral_categoria=0.90, baseline=baseline)
    assert out["pasa"] is True


def test_gate_frontera_igual_al_umbral_pasa():
    m = {"accuracy_categoria": 0.90, "exactitud_campos": 0.9, "n": 100}
    out = gate(m, umbral_categoria=0.90)
    assert out["pasa"] is True


# TODO(estudiante): añade un caso tuyo. Sugerencia: bajo el umbral Y además
# regresión — el motivo debería poder reportar ambos, o al menos el más grave.
# def test_gate_bajo_umbral_y_regresion():
#     ...
