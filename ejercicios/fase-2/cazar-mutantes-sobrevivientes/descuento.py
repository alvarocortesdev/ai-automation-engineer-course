"""Ejercicio 2.9 — CÓDIGO BAJO PRUEBA (no lo modifiques).

`descuento(puntos, es_socio)` devuelve el porcentaje de descuento (0..30) de un
cliente según sus puntos de fidelidad y si es socio. La función está CORRECTA y
la suite de `test_descuento.py` pasa en VERDE con 100% de line coverage.

Tu trabajo NO es cambiar esta función. Es demostrar que la suite, pese a su 100%
de coverage, es DÉBIL: hay mutantes (cambios pequeños) que sobreviven sin que
ningún test se entere. Caza esos mutantes y fortalece los tests.

⚠️ NO edites este archivo. Si lo cambias, dejas de probar el código real.
"""


def descuento(puntos: int, es_socio: bool) -> int:
    """Porcentaje de descuento según puntos y membresía.

    Reglas (umbrales que importan: 100 y 50):
        - 100 puntos o más Y socio  -> 30%
        - 100 puntos o más (no socio) -> 20%
        - 50 puntos o más           -> 10%
        - menos de 50 puntos        -> 0%
    """
    if puntos >= 100 and es_socio:
        return 30
    if puntos >= 100:
        return 20
    if puntos >= 50:
        return 10
    return 0


if __name__ == "__main__":
    # Prueba rápida manual (Predict–Run): ¿qué crees que imprime ANTES de correrlo?
    print(descuento(100, True), descuento(100, False), descuento(50, False), descuento(10, False))
