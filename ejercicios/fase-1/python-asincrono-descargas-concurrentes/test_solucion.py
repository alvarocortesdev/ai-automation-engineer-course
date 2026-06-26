"""Tests del ejercicio.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

Estos tests definen el contrato. Corren tu corutina con asyncio.run(...), así que
NO necesitas el plugin pytest-asyncio. El test clave es `test_es_concurrente`:
mide el tiempo y solo pasa si tus descargas corren solapadas (no en serie).
"""

import asyncio
import time

from solucion import obtener_todos


def test_resultados_en_orden_de_entrada():
    recursos = [
        {"nombre": "A", "demora": 0.05},
        {"nombre": "B", "demora": 0.01},  # termina antes, pero NO debe salir primero
        {"nombre": "C", "demora": 0.03},
    ]
    resultado = asyncio.run(obtener_todos(recursos))
    assert resultado == ["datos de A", "datos de B", "datos de C"]


def test_lista_vacia():
    assert asyncio.run(obtener_todos([])) == []


def test_un_solo_recurso():
    recursos = [{"nombre": "solo", "demora": 0.01}]
    assert asyncio.run(obtener_todos(recursos)) == ["datos de solo"]


def test_es_concurrente():
    # Tres descargas de 0.2s. En serie tardarían ~0.6s; concurrentes, ~0.2s.
    # Umbral generoso (0.45s) que deja pasar lo concurrente y bloquea lo secuencial.
    recursos = [
        {"nombre": "x", "demora": 0.2},
        {"nombre": "y", "demora": 0.2},
        {"nombre": "z", "demora": 0.2},
    ]
    inicio = time.perf_counter()
    resultado = asyncio.run(obtener_todos(recursos))
    transcurrido = time.perf_counter() - inicio

    assert resultado == ["datos de x", "datos de y", "datos de z"]
    assert transcurrido < 0.45, (
        f"tardó {transcurrido:.2f}s — parece secuencial (suma de demoras), "
        "no concurrente. Lanza todas las descargas y espéralas juntas."
    )


# TODO(estudiante): añade aquí al menos un caso borde tuyo.
# def test_mi_caso_borde():
#     ...
