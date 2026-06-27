"""Tests del eval harness. Verifican la POLÍTICA del harness, no detalles internos.

Todo es determinista: el "sistema" (retriever) es falso y no se llama a ninguna API.
Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""

import pytest

from harness import CasoRAG, correr_eval, gate_de_regresion, precision_recall_at_k


# --- precision@k y recall@k ------------------------------------------------
def test_precision_recall_basico():
    # top-4 = ["c1","c2","c3","c4"], relevantes {c1,c3} -> hits=2
    p, r = precision_recall_at_k(["c1", "c2", "c3", "c4"], {"c1", "c3"}, k=4)
    assert p == pytest.approx(0.5)   # 2 / 4
    assert r == pytest.approx(1.0)   # 2 / 2 (se trajeron ambos relevantes)


def test_recall_parcial():
    # top-4 = ["c1","c5","c6","c7"], relevantes {c1,c3} -> hits=1 (falta c3)
    p, r = precision_recall_at_k(["c1", "c5", "c6", "c7"], {"c1", "c3"}, k=4)
    assert p == pytest.approx(0.25)  # 1 / 4
    assert r == pytest.approx(0.5)   # 1 / 2 (se dejó fuera c3)


def test_k_trunca_la_lista():
    # k=2 -> solo se miran ["c1","c2"]; el relevante c3 queda fuera del top-k
    p, r = precision_recall_at_k(["c1", "c2", "c3"], {"c3"}, k=2)
    assert p == pytest.approx(0.0)   # 0 / 2
    assert r == pytest.approx(0.0)   # 0 / 1


def test_relevantes_vacio_no_castiga_recall():
    # No hay nada que recuperar: recall = 1.0 por convención; precision = 0/k.
    p, r = precision_recall_at_k(["c1", "c2", "c3"], set(), k=3)
    assert r == pytest.approx(1.0)
    assert p == pytest.approx(0.0)


# --- correr_eval: agrega y guarda los casos malos --------------------------
def _sistema_falso(pregunta: str) -> list[str]:
    guion = {
        "q1": ["c1", "c2", "c3", "c4"],   # relevantes {c1,c3} -> recall 1.0
        "q2": ["c5", "c6", "c1", "c7"],   # relevante {c9} -> recall 0.0 (fallo)
    }
    return guion[pregunta]


def test_correr_eval_agrega_y_guarda_fallos():
    dataset = [CasoRAG("q1", {"c1", "c3"}), CasoRAG("q2", {"c9"})]
    resumen = correr_eval(_sistema_falso, dataset, k=4)

    # recall: (1.0 + 0.0) / 2 = 0.5 ; precision: (0.5 + 0.0) / 2 = 0.25
    assert resumen["recall"] == pytest.approx(0.5)
    assert resumen["precision"] == pytest.approx(0.25)
    assert resumen["n"] == 2

    # Solo q2 tiene recall < 1.0 -> es el único fallo registrado.
    assert len(resumen["fallos"]) == 1
    assert resumen["fallos"][0]["pregunta"] == "q2"
    assert resumen["fallos"][0]["recall"] == pytest.approx(0.0)
    assert resumen["fallos"][0]["recuperados"] == ["c5", "c6", "c1", "c7"]


# --- gate_de_regresion -----------------------------------------------------
def test_gate_bloquea_por_umbral():
    r = gate_de_regresion({"recall": 0.5}, umbral=0.85)
    assert r.pasa is False


def test_gate_bloquea_por_regresion_aunque_supere_umbral():
    # 0.86 >= umbral 0.85, PERO 0.86 < baseline 0.90 - 0.02 = 0.88 -> regresión.
    r = gate_de_regresion({"recall": 0.86}, umbral=0.85, baseline=0.90, tolerancia=0.02)
    assert r.pasa is False
    assert "regres" in r.razon.lower()


def test_gate_pasa():
    r = gate_de_regresion({"recall": 0.91}, umbral=0.85, baseline=0.90, tolerancia=0.02)
    assert r.pasa is True


# TODO(estudiante): añade aquí al menos un test propio.
# Idea: k mayor que la cantidad de chunks recuperados, o un golden con 2 relevantes
# de los que solo se recupera 1.
