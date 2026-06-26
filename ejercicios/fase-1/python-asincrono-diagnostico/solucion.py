"""Starter — escribe aquí la versión CORREGIDA de roto.py.

Orden Primero-Sin-IA:
  1. Lee roto.py y escribe tu `diagnostico.md` ANTES de tocar este archivo.
  2. Ejecuta roto.py para confirmar tus hipótesis.
  3. Corrige aquí los tres bugs. La firma pública que usan los tests es
     `descargar_todo(recursos)`.

Contrato de `descargar_todo`:
    entrada: list[dict]; cada dict tiene "nombre" (str) y "demora" (float, segundos).
    cada descarga se simula esperando `demora` segundos SIN bloquear el event loop,
        y devuelve f"datos de {nombre}".
    salida:  list[str] EN ORDEN DE ENTRADA, con las descargas corriendo CONCURRENTEMENTE.
"""

import asyncio


async def registrar_inicio(nombre):
    await asyncio.sleep(0.01)
    print(f"[log] empezando {nombre}")


async def descargar_todo(recursos: list[dict]) -> list[str]:
    """Versión corregida: concurrente, sin bloquear el loop, en orden."""
    raise NotImplementedError("Corrige los tres bugs a mano, sin IA.")


if __name__ == "__main__":
    import time

    recursos = [
        {"nombre": "A", "demora": 0.3},
        {"nombre": "B", "demora": 0.3},
        {"nombre": "C", "demora": 0.3},
    ]
    inicio = time.perf_counter()
    print(asyncio.run(descargar_todo(recursos)))
    print(f"tardó {time.perf_counter() - inicio:.2f}s")  # objetivo: ~0.3s, no ~0.9s
