"""Starter del ejercicio — Primero-Sin-IA.

Implementa la corutina a mano, sin IA. Reemplaza el cuerpo de `obtener_todos` por
tu solución. NO cambies la firma (nombre, parámetro, que sea `async def`): los
tests de `test_solucion.py` dependen de ella.

Contrato:
    entrada: una list[dict]; cada dict tiene:
        - "nombre": str
        - "demora": float (segundos que tarda esa "descarga")
    cada descarga se simula con `await asyncio.sleep(demora)` y devuelve
        f"datos de {nombre}".
    salida:  list[str] con los resultados EN EL MISMO ORDEN DE ENTRADA.
    requisito clave: las descargas deben correr CONCURRENTEMENTE (solapadas),
        no una tras otra. La lista vacía devuelve [].
"""

import asyncio


async def obtener_todos(recursos: list[dict]) -> list[str]:
    """Descarga todos los recursos concurrentemente y devuelve sus resultados en orden."""
    raise NotImplementedError("Implementa esta corutina a mano, sin IA.")


if __name__ == "__main__":
    # Prueba rápida manual (Predict–Run): ¿qué crees que imprime y cuánto tarda
    # ANTES de correrlo?
    demo = [
        {"nombre": "A", "demora": 1.0},
        {"nombre": "B", "demora": 1.0},
        {"nombre": "C", "demora": 1.0},
    ]
    print(asyncio.run(obtener_todos(demo)))
