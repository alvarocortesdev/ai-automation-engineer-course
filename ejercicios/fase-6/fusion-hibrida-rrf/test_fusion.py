"""Tests del ejercicio 6.7 — Retrieval híbrido: RRF + metadata filtering.

Estos tests definen el CONTRATO. Hazlos pasar todos en verde. Luego AÑADE al menos
un caso borde tuyo (pensar en casos borde es parte del Primero-Sin-IA).

Los rankings y la metadata son pequeños y elegidos a mano para que los números sean
verificables y los tests deterministas (sin API ni modelos).

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""

import pytest

from fusion import rrf_fusion, filtrar_por_metadata, recuperar_hibrido


# ---------- rrf_fusion ----------

def test_rrf_primer_puesto_usa_rank_1_based():
    # Una sola lista, k=1: el primer puesto es 1/(1+1)=0.5, el segundo 1/(1+2)=0.333
    resultado = dict(rrf_fusion([["a", "b"]], k=1))
    assert resultado["a"] == pytest.approx(0.5)
    assert resultado["b"] == pytest.approx(1 / 3)


def test_rrf_doc_en_ambas_listas_acumula_y_gana():
    # b aparece arriba en las dos listas -> debe quedar primero.
    resultado = rrf_fusion([["a", "b", "c"], ["b", "c", "a"]])  # k=60 por defecto
    ids = [d for d, _ in resultado]
    assert ids == ["b", "a", "c"]
    # Verificación numérica del ganador: 1/62 + 1/61
    puntajes = dict(resultado)
    assert puntajes["b"] == pytest.approx(1 / 62 + 1 / 61)


def test_rrf_ordena_descendente_por_score():
    resultado = rrf_fusion([["a", "b", "c"], ["b", "c", "a"]])
    scores = [s for _, s in resultado]
    assert scores == sorted(scores, reverse=True)


def test_rrf_empate_se_rompe_por_doc_id_ascendente():
    # x e y empatan (cada uno primero en una lista) -> orden determinista por id.
    resultado = rrf_fusion([["x"], ["y"]])
    ids = [d for d, _ in resultado]
    assert ids == ["x", "y"]


def test_rrf_doc_en_una_sola_lista_tambien_cuenta():
    resultado = dict(rrf_fusion([["a", "b"], ["a"]]))
    assert resultado["b"] == pytest.approx(1 / 62)            # solo en la 1a lista, rank 2
    assert resultado["a"] == pytest.approx(1 / 61 + 1 / 61)   # 1o en ambas


# ---------- filtrar_por_metadata ----------

def test_filtrar_conserva_solo_los_que_cumplen():
    doc_ids = ["d1", "d2", "d3"]
    metadata = {"d1": {"tenant": "A"}, "d2": {"tenant": "B"}, "d3": {"tenant": "A"}}
    assert filtrar_por_metadata(doc_ids, metadata, {"tenant": "A"}) == ["d1", "d3"]


def test_filtrar_es_fail_closed_si_falta_la_clave():
    doc_ids = ["d1", "d2"]
    metadata = {"d1": {"tenant": "A"}, "d2": {}}  # d2 no tiene 'tenant'
    assert filtrar_por_metadata(doc_ids, metadata, {"tenant": "A"}) == ["d1"]


def test_filtrar_es_fail_closed_si_el_doc_no_esta_en_metadata():
    doc_ids = ["d1", "dX"]
    metadata = {"d1": {"tenant": "A"}}  # dX no existe en metadata
    assert filtrar_por_metadata(doc_ids, metadata, {"tenant": "A"}) == ["d1"]


def test_filtrar_filtro_vacio_deja_pasar_todo():
    doc_ids = ["d1", "d2"]
    metadata = {"d1": {"tenant": "A"}, "d2": {"tenant": "B"}}
    assert filtrar_por_metadata(doc_ids, metadata, {}) == ["d1", "d2"]


def test_filtrar_exige_todas_las_claves():
    doc_ids = ["d1", "d2"]
    metadata = {
        "d1": {"tenant": "A", "year": 2026},
        "d2": {"tenant": "A", "year": 2024},
    }
    assert filtrar_por_metadata(doc_ids, metadata, {"tenant": "A", "year": 2026}) == ["d1"]


# ---------- recuperar_hibrido ----------

def test_recuperar_hibrido_fusiona_filtra_y_recorta():
    vect = ["d1", "d2", "d3"]
    bm25 = ["d2", "d4", "d1"]
    metadata = {
        "d1": {"tenant": "A"},
        "d2": {"tenant": "A"},
        "d3": {"tenant": "B"},  # debe quedar fuera por el filtro
        "d4": {"tenant": "A"},
    }
    resultado = recuperar_hibrido(vect, bm25, metadata, {"tenant": "A"}, k_final=2)

    ids = [d for d, _ in resultado]
    assert ids == ["d2", "d1"]              # fusionado, filtrado (sin d3), top-2
    assert len(resultado) == 2
    puntajes = dict(resultado)
    assert puntajes["d2"] == pytest.approx(1 / 62 + 1 / 61)
    assert puntajes["d1"] == pytest.approx(1 / 61 + 1 / 63)


def test_recuperar_hibrido_k_final_mayor_devuelve_todos_los_que_pasan():
    vect = ["d1", "d2"]
    bm25 = ["d2", "d1"]
    metadata = {"d1": {"tenant": "A"}, "d2": {"tenant": "B"}}
    resultado = recuperar_hibrido(vect, bm25, metadata, {"tenant": "A"}, k_final=10)
    assert [d for d, _ in resultado] == ["d1"]  # solo d1 pasa el filtro


# TODO(estudiante): añade aquí al menos un caso borde tuyo.
# Ideas: ¿recuperar_hibrido con k_final=0? ¿rrf_fusion de lista de listas vacía?
# ¿filtrar con un filtro de dos claves donde el doc cumple solo una?
