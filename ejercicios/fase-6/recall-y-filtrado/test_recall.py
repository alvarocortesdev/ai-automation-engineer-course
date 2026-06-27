"""Tests del ejercicio 6.6 — Recall + filtrado por metadata.

Estos tests definen el CONTRATO. Hazlos pasar todos en verde. Luego AÑADE al
menos un caso borde tuyo (pensar en casos borde es parte del Primero-Sin-IA).

Los vectores son pequeños y elegidos a mano para que los cosenos sean obvios y
los tests deterministas (sin API ni servidor de base de datos).

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""

import pytest

from recall import similitud_coseno, buscar_exacto, recall_at_k, buscar_con_filtro


# ---------- similitud_coseno ----------

def test_coseno_vectores_iguales_es_uno():
    assert similitud_coseno([1, 2, 3], [1, 2, 3]) == pytest.approx(1.0)


def test_coseno_ignora_la_magnitud():
    assert similitud_coseno([1, 0], [2, 0]) == pytest.approx(1.0)


def test_coseno_opuestos_es_menos_uno():
    assert similitud_coseno([1, 0], [-1, 0]) == pytest.approx(-1.0)


# ---------- buscar_exacto (ground truth) ----------

def test_buscar_exacto_rankea_de_mayor_a_menor():
    consulta = [1, 0]
    # idx0 idéntico (cos 1), idx1 perpendicular (cos 0), idx2 diagonal (~0.707),
    # idx3 opuesto (cos -1).
    corpus = [[1, 0], [0, 1], [1, 1], [-1, 0]]
    resultado = buscar_exacto(consulta, corpus, k=2)

    indices = [i for (i, _s) in resultado]
    scores = [s for (_i, s) in resultado]

    assert indices == [0, 2]
    assert scores[0] == pytest.approx(1.0)
    assert scores[1] == pytest.approx(0.7071, abs=1e-3)


def test_buscar_exacto_k_mayor_que_corpus_devuelve_todos():
    resultado = buscar_exacto([1, 0], [[1, 0], [0, 1]], k=10)
    assert len(resultado) == 2


# ---------- recall_at_k ----------

def test_recall_parcial():
    # exactos = {0,2,5}; aprox encontró 0 y 2, pero no 5 -> 2/3
    assert recall_at_k([0, 2, 7], [0, 2, 5]) == pytest.approx(2 / 3)


def test_recall_perfecto():
    assert recall_at_k([0, 1, 2], [2, 1, 0]) == pytest.approx(1.0)


def test_recall_cero():
    assert recall_at_k([3, 4], [0, 1]) == pytest.approx(0.0)


def test_recall_ground_truth_vacio_no_divide_por_cero():
    assert recall_at_k([1, 2], []) == pytest.approx(1.0)


# ---------- buscar_con_filtro ----------

CONSULTA = [1, 0]
CORPUS = [[1, 0], [0, 1], [1, 1], [-1, 0]]
METADATAS = [
    {"categoria": "tech"},
    {"categoria": "gatos"},
    {"categoria": "gatos"},
    {"categoria": "tech"},
]


def test_prefilter_devuelve_los_mejores_que_cumplen():
    # tech = {idx0 (cos 1.0), idx3 (cos -1.0)}; rankeados -> [(0,1.0),(3,-1.0)]
    res = buscar_con_filtro(CONSULTA, CORPUS, METADATAS, {"categoria": "tech"}, k=2, modo="pre")
    assert [i for (i, _s) in res] == [0, 3]
    assert res[0][1] == pytest.approx(1.0)
    assert res[1][1] == pytest.approx(-1.0)


def test_postfilter_puede_devolver_menos_de_k():
    # top-2 global por coseno = [idx0 (1.0), idx2 (0.707)]; al filtrar tech,
    # idx2 es 'gatos' y cae -> queda solo idx0. MENOS de k=2. Ese es el bug.
    res = buscar_con_filtro(CONSULTA, CORPUS, METADATAS, {"categoria": "tech"}, k=2, modo="post")
    assert [i for (i, _s) in res] == [0]
    assert len(res) == 1


def test_prefilter_sin_coincidencias_es_vacio():
    res = buscar_con_filtro(CONSULTA, CORPUS, METADATAS, {"categoria": "nada"}, k=3, modo="pre")
    assert res == []


# TODO(estudiante): añade aquí al menos un caso borde tuyo.
# Ideas: ¿recall_at_k cuando el aprox acierta TODO y trae extras? ¿buscar_con_filtro
# con un `where` de dos claves? ¿post-filter donde NINGÚN top-k cumple el filtro?
