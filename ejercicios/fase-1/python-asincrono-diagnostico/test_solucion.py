"""Tests de la versión CORREGIDA (solucion.py).

Ejecuta:
    uv run pytest        # recomendado
    pytest

Corren tu corutina con asyncio.run(...), sin necesidad de pytest-asyncio. El test
de tiempo solo pasa si corregiste BOTH el `time.sleep` (que bloqueaba el loop) Y el
`await` secuencial del bucle: con uno solo de los dos arreglos, sigue siendo lento.
"""

import asyncio
import time

from solucion import descargar_todo


def test_resultados_en_orden():
    recursos = [
        {"nombre": "A", "demora": 0.05},
        {"nombre": "B", "demora": 0.01},
        {"nombre": "C", "demora": 0.03},
    ]
    assert asyncio.run(descargar_todo(recursos)) == [
        "datos de A",
        "datos de B",
        "datos de C",
    ]


def test_lista_vacia():
    assert asyncio.run(descargar_todo([])) == []


def test_es_concurrente_y_no_bloquea():
    # Tres descargas de 0.2s. Roto (time.sleep + await en serie) tarda ~0.6s.
    # Corregido (asyncio.sleep + gather/TaskGroup) tarda ~0.2s.
    recursos = [
        {"nombre": "x", "demora": 0.2},
        {"nombre": "y", "demora": 0.2},
        {"nombre": "z", "demora": 0.2},
    ]
    inicio = time.perf_counter()
    resultado = asyncio.run(descargar_todo(recursos))
    transcurrido = time.perf_counter() - inicio

    assert resultado == ["datos de x", "datos de y", "datos de z"]
    assert transcurrido < 0.45, (
        f"tardó {transcurrido:.2f}s — sigue siendo secuencial. ¿Cambiaste time.sleep "
        "por asyncio.sleep Y lanzaste las descargas con gather/TaskGroup?"
    )
