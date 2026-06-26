"""Ejercicio 1.4 — Tipar un módulo y hacer pasar mypy --strict (Primero-Sin-IA).

Este módulo de la despensa de HomeHub está SIN TIPOS y esconde un bug latente:
trata un campo opcional ('descuento_pct') como si siempre estuviera presente.

Tu trabajo, EN ESTE ORDEN:
  1. Anota TODAS las funciones (parámetros y retorno) y el acumulador local.
     Recuerda: los precios son enteros (pesos chilenos), una lista de items es
     list[dict[str, int]], y la división `/` devuelve float.
  2. Corre la verificación estática:
         uv run mypy --strict despensa.py     # o:  mypy --strict despensa.py
     mypy te marcará el bug ANTES de ejecutar nada. Léelo: te dice exactamente
     qué tipo no calza con qué.
  3. Arregla el bug que mypy revela (un default para el campo opcional), NO con
     un `# type: ignore`. Deja mypy en 0 errores y los tests en verde:
         uv run pytest

No cambies los nombres ni las firmas de las funciones: los tests dependen de ellos.
"""


def descuento(precio, porcentaje):
    """Aplica un descuento porcentual (0..100) a un precio y devuelve el precio final."""
    return precio - (precio * porcentaje / 100)


def total_despensa(items):
    """Suma el precio final de cada item de la despensa.

    Cada item es un dict con la clave 'precio' y, OPCIONALMENTE, 'descuento_pct'.
    Un item sin 'descuento_pct' debe tratarse como 0% de descuento.
    """
    suma = 0
    for item in items:
        suma += descuento(item["precio"], item.get("descuento_pct"))
    return suma


if __name__ == "__main__":
    # Predict–Run: ¿qué crees que pasa con el segundo item, que no trae descuento?
    canasta = [{"precio": 1000, "descuento_pct": 10}, {"precio": 500}]
    print(total_despensa(canasta))
