"""Ejercicio 1.1 — módulo de inventario (Primero-Sin-IA).

Completa las dos funciones. NO cambies sus firmas: los tests de
`test_inventario.py` dependen de ellas.

Corre los tests desde la carpeta del ejercicio:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""


def resumen_inventario(productos):
    """Resume una lista de productos de la despensa.

    Cada producto es un dict con las claves:
      - "nombre": str no vacío
      - "precio": int o float, mayor o igual a 0
      - "stock":  int, mayor o igual a 0

    Devuelve un dict:
      - "unidades": suma de los stock
      - "valor":    suma de precio * stock de cada producto
      - "agotados": lista de los nombre cuyo stock es 0

    Lista vacía devuelve {"unidades": 0, "valor": 0, "agotados": []}.

    Validación (lanza ValueError con un mensaje claro):
      - precio negativo -> ValueError
      - stock negativo  -> ValueError

    Ejemplo:
        >>> resumen_inventario([
        ...     {"nombre": "café",   "precio": 2500, "stock": 3},
        ...     {"nombre": "té",     "precio": 1800, "stock": 0},
        ...     {"nombre": "azúcar", "precio": 1200, "stock": 5},
        ... ])
        {'unidades': 8, 'valor': 13500, 'agotados': ['té']}
    """
    # TODO(estudiante): borra esta línea y escribe tu solución idiomática, sin IA.
    raise NotImplementedError("Implementa resumen_inventario")


def formatear_lineas(productos):
    """Devuelve una lista de líneas numeradas desde 1, una por producto.

    Formato EXACTO de cada línea (usa f-string y enumerate):
        "1. café — $2500 (x3)"

    Lista vacía devuelve [].

    Ejemplo:
        >>> formatear_lineas([{"nombre": "café", "precio": 2500, "stock": 3}])
        ['1. café — $2500 (x3)']
    """
    # TODO(estudiante): borra esta línea y escribe tu solución idiomática, sin IA.
    raise NotImplementedError("Implementa formatear_lineas")


if __name__ == "__main__":
    # Prueba rápida manual: SOLO corre si ejecutas este archivo directo
    # (python despensa/inventario.py), NO cuando alguien importa el módulo.
    demo = [
        {"nombre": "café", "precio": 2500, "stock": 3},
        {"nombre": "té", "precio": 1800, "stock": 0},
    ]
    print(resumen_inventario(demo))
    print(formatear_lineas(demo))
