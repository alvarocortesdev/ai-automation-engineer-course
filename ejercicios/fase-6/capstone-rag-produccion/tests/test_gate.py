"""Tests del gate de regresion y de las metricas deterministas del eval harness.

Estos tests fijan el comportamiento del DoD-5: el gate debe bloquear por umbral Y por
regresion. Si los rompes mientras refactorizas, rompiste el ship-gate.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from evals.run_evals import gate_de_regresion, precision_recall_at_k  # noqa: E402


def test_pasa_cuando_supera_umbral_sin_baseline():
    pasa, _ = gate_de_regresion(0.90, umbral=0.75)
    assert pasa


def test_bloquea_bajo_umbral_absoluto():
    pasa, razon = gate_de_regresion(0.70, umbral=0.75)
    assert not pasa
    assert "umbral" in razon


def test_bloquea_por_regresion_aunque_supere_umbral():
    # 0.86 supera el umbral 0.85, pero regreso vs baseline 0.90 con tolerancia 0.02
    pasa, razon = gate_de_regresion(0.86, umbral=0.85, baseline=0.90, tolerancia=0.02)
    assert not pasa
    assert "regresion" in razon


def test_pasa_dentro_de_la_tolerancia():
    pasa, _ = gate_de_regresion(0.89, umbral=0.85, baseline=0.90, tolerancia=0.02)
    assert pasa


def test_precision_recall_truncan_a_k():
    # relevantes = {c3}; con k=2 sobre [c1,c2,c3], c3 queda fuera del top-k
    p, r = precision_recall_at_k(["c1", "c2", "c3"], {"c3"}, k=2)
    assert p == 0.0
    assert r == 0.0


def test_precision_recall_denominadores_distintos():
    # 2 relevantes, ambos en el top-3: recall=1.0, precision=2/3
    p, r = precision_recall_at_k(["c1", "c2", "c9"], {"c1", "c2"}, k=3)
    assert abs(p - (2 / 3)) < 1e-9
    assert r == 1.0


def test_recall_uno_cuando_no_hay_relevantes():
    p, r = precision_recall_at_k(["c1"], set(), k=1)
    assert r == 1.0
