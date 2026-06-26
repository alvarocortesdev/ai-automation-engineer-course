"""Tests del ejercicio 1.2 — Procesar transacciones con comprehensions y un generador.

Estos tests definen el CONTRATO. Hazlos pasar todos en verde. Luego AÑADE al menos
un caso borde tuyo (pensar en casos borde es parte del Primero-Sin-IA).

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""

import inspect

import pytest

from transacciones import categorias_unicas, indexar_por_id, stream_montos

DATOS = [
    {"id": 1, "categoria": "comida", "monto": 5000},
    {"id": 2, "categoria": "comida", "monto": 12000},
    {"id": 3, "categoria": "ocio", "monto": 800},
    {"id": 4, "categoria": "transporte", "monto": 4000},
]


# --- categorias_unicas (set comprehension) ---

def test_categorias_unicas_sin_repetidos():
    assert categorias_unicas(DATOS) == {"comida", "ocio", "transporte"}


def test_categorias_unicas_devuelve_set():
    assert isinstance(categorias_unicas(DATOS), set)


def test_categorias_unicas_lista_vacia():
    assert categorias_unicas([]) == set()


# --- indexar_por_id (dict comprehension) ---

def test_indexar_por_id_mapea_id_a_transaccion():
    indice = indexar_por_id(DATOS)
    assert indice[2] == {"id": 2, "categoria": "comida", "monto": 12000}
    assert set(indice.keys()) == {1, 2, 3, 4}


def test_indexar_por_id_lista_vacia():
    assert indexar_por_id([]) == {}


# --- stream_montos (generador) ---

def test_stream_montos_es_un_generador():
    # No basta con que devuelva los valores: debe ser un GENERADOR (lazy).
    resultado = stream_montos(DATOS, minimo=4000)
    assert inspect.isgenerator(resultado), "stream_montos debe usar yield, no devolver una lista"


def test_stream_montos_filtra_y_conserva_orden():
    assert list(stream_montos(DATOS, minimo=4000)) == [5000, 12000, 4000]


def test_stream_montos_incluye_el_limite():
    # >= minimo: el monto igual al mínimo SÍ entra.
    assert list(stream_montos(DATOS, minimo=12000)) == [12000]


def test_stream_montos_lista_vacia_no_produce_nada():
    assert list(stream_montos([], minimo=0)) == []


def test_stream_montos_se_consume_de_a_uno():
    gen = stream_montos(DATOS, minimo=4000)
    assert next(gen) == 5000
    assert next(gen) == 12000
    assert next(gen) == 4000
    with pytest.raises(StopIteration):
        next(gen)


# TODO(estudiante): añade aquí al menos un caso borde tuyo.
# def test_mi_caso_borde():
#     assert ...
