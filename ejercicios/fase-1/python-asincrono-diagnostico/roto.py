"""Programa con TRES bugs clásicos de async. NO lo edites: estúdialo.

Tu tarea (ver README.md): leerlo, diagnosticar los tres bugs en `diagnostico.md`
SIN ejecutar, después ejecutarlo para confirmar, y escribir la versión corregida
en `solucion.py`.

Pista de lectura: el programa "corre" pero (a) imprime una advertencia, (b) no es
concurrente aunque lo parezca, y (c) tarda la suma de las demoras, no la mayor.
"""

import asyncio
import time


async def registrar_inicio(nombre):
    # Imagina que esto escribe un log de forma asíncrona.
    await asyncio.sleep(0.01)
    print(f"[log] empezando {nombre}")


async def descargar(recurso):
    nombre = recurso["nombre"]
    registrar_inicio(nombre)            # (1)
    time.sleep(recurso["demora"])       # (2)  simula la "descarga"
    return f"datos de {nombre}"


async def descargar_todo(recursos):
    resultados = []
    for recurso in recursos:
        datos = await descargar(recurso)   # (3)
        resultados.append(datos)
    return resultados


if __name__ == "__main__":
    recursos = [
        {"nombre": "A", "demora": 0.3},
        {"nombre": "B", "demora": 0.3},
        {"nombre": "C", "demora": 0.3},
    ]
    inicio = time.perf_counter()
    print(asyncio.run(descargar_todo(recursos)))
    print(f"tardó {time.perf_counter() - inicio:.2f}s")
