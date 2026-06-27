"""Tests del ejercicio 6.5 — Buscador semántico desde cero.

Estos tests definen el CONTRATO. Hazlos pasar todos en verde. Luego AÑADE al
menos un caso borde tuyo (pensar en casos borde es parte del Primero-Sin-IA).

Los vectores son pequeños y elegidos a mano para que los cosenos sean obvios y
los tests deterministas (sin API ni modelos descargados).

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""

import pytest

from buscador import chunk_texto, similitud_coseno, buscar, deduplicar


# ---------- similitud_coseno ----------

def test_coseno_vectores_iguales_es_uno():
    assert similitud_coseno([1, 2, 3], [1, 2, 3]) == pytest.approx(1.0)


def test_coseno_ignora_la_magnitud():
    # b = 2*a: misma dirección, distinta longitud -> coseno sigue siendo 1.
    assert similitud_coseno([1, 2, 3], [2, 4, 6]) == pytest.approx(1.0)


def test_coseno_perpendiculares_es_cero():
    assert similitud_coseno([1, 0], [0, 1]) == pytest.approx(0.0)


# ---------- chunk_texto ----------

def test_chunk_avanza_tam_menos_solape():
    # 6 palabras, tam=4, solape=2 -> paso=2 -> empieza en 0, 2, 4
    texto = "uno dos tres cuatro cinco seis"
    chunks = chunk_texto(texto, tam=4, solape=2)
    assert chunks == [
        "uno dos tres cuatro",
        "tres cuatro cinco seis",
    ]


def test_chunk_texto_mas_corto_que_tam_es_un_solo_chunk():
    texto = "solo tres palabras"
    assert chunk_texto(texto, tam=10, solape=2) == ["solo tres palabras"]


def test_chunk_texto_vacio_es_lista_vacia():
    assert chunk_texto("", tam=4, solape=1) == []


def test_chunk_solape_mayor_o_igual_que_tam_lanza():
    with pytest.raises(ValueError):
        chunk_texto("uno dos tres cuatro", tam=3, solape=3)


# ---------- buscar ----------

def test_buscar_rankea_de_mayor_a_menor():
    consulta = [1, 0]
    # idx0 idéntico (cos 1), idx1 perpendicular (cos 0), idx2 diagonal (~0.707),
    # idx3 opuesto (cos -1).
    corpus = [[1, 0], [0, 1], [1, 1], [-1, 0]]
    resultado = buscar(consulta, corpus, k=2)

    indices = [i for (i, _s) in resultado]
    scores = [s for (_i, s) in resultado]

    assert len(resultado) == 2
    assert indices == [0, 2]                       # los dos más parecidos, en orden
    assert scores[0] == pytest.approx(1.0)
    assert scores[1] == pytest.approx(0.7071, abs=1e-3)
    assert scores == sorted(scores, reverse=True)  # descendente


def test_buscar_k_mayor_que_el_corpus_devuelve_todos():
    consulta = [1, 0]
    corpus = [[1, 0], [0, 1]]
    resultado = buscar(consulta, corpus, k=10)
    assert len(resultado) == 2


# ---------- deduplicar ----------

def test_deduplicar_descarta_casi_iguales():
    # v0 y v1 idénticos (cos 1); v2 perpendicular; v3 diagonal (cos ~0.707 con v0).
    vecs = [[1, 0], [1, 0], [0, 1], [1, 1]]
    assert deduplicar(vecs, umbral=0.95) == [0, 2, 3]


def test_deduplicar_umbral_alto_conserva_todo():
    vecs = [[1, 0], [1, 0], [0, 1]]
    # Con umbral 1.01 nada llega al umbral (el coseno máximo es 1.0) -> conserva todo.
    assert deduplicar(vecs, umbral=1.01) == [0, 1, 2]


# TODO(estudiante): añade aquí al menos un caso borde tuyo.
# Ideas: ¿buscar con k=0? ¿chunk_texto con solape=0? ¿deduplicar de lista vacía?
