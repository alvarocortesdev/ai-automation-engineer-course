"""Tests del ejercicio 6.0 — Similitud coseno desde cero.

Estos tests definen el CONTRATO. Hazlos pasar todos en verde. Luego AÑADE al
menos un caso borde tuyo (pensar en casos borde es parte del Primero-Sin-IA).

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""

import pytest

from similitud import producto_punto, magnitud, similitud_coseno, rankear


def test_producto_punto_basico():
    assert producto_punto([1, 2, 3], [4, 5, 6]) == 32


def test_producto_punto_con_ceros():
    assert producto_punto([2, 0, 3], [1, 5, 1]) == 5


def test_producto_punto_distinto_largo_lanza():
    with pytest.raises(ValueError):
        producto_punto([1, 2], [1, 2, 3])


def test_magnitud_triangulo_3_4_5():
    assert magnitud([3, 4]) == pytest.approx(5.0)


def test_coseno_vectores_iguales_es_uno():
    assert similitud_coseno([1, 2, 3], [1, 2, 3]) == pytest.approx(1.0)


def test_coseno_ignora_la_magnitud():
    # b es 2*a: misma dirección, distinta longitud -> coseno debe seguir siendo 1.
    assert similitud_coseno([1, 2, 3], [2, 4, 6]) == pytest.approx(1.0)


def test_coseno_perpendiculares_es_cero():
    assert similitud_coseno([1, 0], [0, 1]) == pytest.approx(0.0)


def test_coseno_caso_de_la_leccion():
    # Q=[7,1] contra D1=[9,1] ~0.999 ; contra D3=[1,9] ~0.250
    assert similitud_coseno([7, 1], [9, 1]) == pytest.approx(0.999, abs=1e-3)
    assert similitud_coseno([7, 1], [1, 9]) == pytest.approx(0.250, abs=1e-3)


def test_coseno_vector_cero_lanza():
    with pytest.raises(ValueError):
        similitud_coseno([0, 0], [1, 2])


def test_rankear_ordena_de_mayor_a_menor():
    q = [7, 1]
    # A propósito desordenado: finanzas primero, mascotas después.
    docs = [[1, 9], [9, 1], [8, 0]]
    ranking = rankear(q, docs)

    indices = [i for (i, _sim) in ranking]
    sims = [s for (_i, s) in ranking]

    # El documento de finanzas (índice 0) es el menos parecido -> queda último.
    assert indices[-1] == 0
    # Los dos de mascotas (índices 1 y 2) quedan arriba.
    assert indices[0] in (1, 2)
    # Las similitudes vienen en orden descendente.
    assert sims == sorted(sims, reverse=True)


# TODO(estudiante): añade aquí al menos un caso borde tuyo.
# ¿Qué pasa si dos documentos tienen exactamente la misma similitud?
# ¿Y con vectores de 3 o más dimensiones?
