"""Tests del ejercicio 6.0 — Precision, recall y F1 desde cero.

Estos tests definen el CONTRATO. Hazlos pasar todos en verde. Luego AÑADE al
menos un caso borde tuyo (pensar en casos borde es parte del Primero-Sin-IA).

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""

import pytest

from metricas import contar, precision, recall, f1, evaluar


def test_contar_basico():
    y_true = [1, 1, 0, 1, 0, 0]
    y_pred = [1, 0, 0, 1, 1, 0]
    # TP=2 (pos 0 y 3), FP=1 (pos 4), FN=1 (pos 1)
    assert contar(y_true, y_pred) == (2, 1, 1)


def test_contar_distinto_largo_lanza():
    with pytest.raises(ValueError):
        contar([1, 0], [1])


def test_metricas_ejemplo_rag_de_la_leccion():
    # El retriever de la lección: TP=6, FP=4, FN=2
    assert precision(6, 4) == pytest.approx(0.60)
    assert recall(6, 2) == pytest.approx(0.75)
    assert f1(0.60, 0.75) == pytest.approx(0.6667, abs=1e-4)


def test_precision_sin_positivos_predichos_es_cero():
    # No predijiste ningún positivo -> 0.0, no una excepción.
    assert precision(0, 0) == 0.0


def test_recall_sin_positivos_reales_es_cero():
    assert recall(0, 0) == 0.0


def test_f1_cuando_una_metrica_es_cero_es_cero():
    # Precision perfecta pero recall 0 => F1 = 0 (NO 0.5).
    assert f1(1.0, 0.0) == 0.0


def test_evaluar_devuelve_las_tres_metricas():
    y_true = [1, 1, 1, 0, 0]
    y_pred = [1, 1, 0, 0, 0]
    # TP=2, FP=0, FN=1 -> precision 1.0, recall 0.667, f1 0.8
    r = evaluar(y_true, y_pred)
    assert r["precision"] == pytest.approx(1.0)
    assert r["recall"] == pytest.approx(0.6667, abs=1e-4)
    assert r["f1"] == pytest.approx(0.8, abs=1e-4)


# TODO(estudiante): añade aquí al menos un caso borde tuyo.
# ¿Qué pasa si el modelo predice TODO positivo? ¿Y si el modelo es perfecto?
