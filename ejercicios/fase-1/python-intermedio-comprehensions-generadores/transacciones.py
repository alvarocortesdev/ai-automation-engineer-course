"""Ejercicio 1.2 — Procesar transacciones (Primero-Sin-IA).

Completa las tres funciones. NO cambies sus firmas: los tests dependen de ellas.

Cada transacción es un dict con las claves:
  - "id": int único
  - "categoria": str
  - "monto": int o float

Corre los tests con:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""

from collections.abc import Iterator


def categorias_unicas(transacciones: list[dict]) -> set[str]:
    """Devuelve un set con las categorías DISTINTAS de las transacciones.

    Usa una SET comprehension. Una lista vacía devuelve set().

    Ejemplo:
        >>> categorias_unicas([
        ...     {"id": 1, "categoria": "comida", "monto": 10},
        ...     {"id": 2, "categoria": "comida", "monto": 20},
        ...     {"id": 3, "categoria": "ocio", "monto": 5},
        ... ])
        {'comida', 'ocio'}
    """
    # TODO(estudiante): borra esta línea y escribe tu solución a mano, sin IA.
    raise NotImplementedError("Implementa categorias_unicas con una set comprehension")


def indexar_por_id(transacciones: list[dict]) -> dict[int, dict]:
    """Devuelve un dict {id: transacción} para buscar por id en tiempo constante.

    Usa una DICT comprehension. Una lista vacía devuelve {}.

    Ejemplo:
        >>> indexar_por_id([{"id": 7, "categoria": "x", "monto": 1}])
        {7: {'id': 7, 'categoria': 'x', 'monto': 1}}
    """
    # TODO(estudiante): borra esta línea y escribe tu solución a mano, sin IA.
    raise NotImplementedError("Implementa indexar_por_id con una dict comprehension")


def stream_montos(transacciones: list[dict], minimo: float) -> Iterator[float]:
    """GENERADOR: produce, de a uno y EN ORDEN, los montos >= minimo.

    Debe usar `yield` (NO construyas ni devuelvas una lista). Si ninguna
    transacción cumple, no produce nada. Una lista vacía no produce nada.

    Ejemplo:
        >>> list(stream_montos([
        ...     {"id": 1, "categoria": "x", "monto": 5},
        ...     {"id": 2, "categoria": "y", "monto": 100},
        ...     {"id": 3, "categoria": "z", "monto": 50},
        ... ], minimo=50))
        [100, 50]
    """
    # TODO(estudiante): borra esta línea y escribe tu solución a mano, sin IA.
    raise NotImplementedError("Implementa stream_montos como GENERADOR (yield)")


if __name__ == "__main__":
    datos = [
        {"id": 1, "categoria": "comida", "monto": 5000},
        {"id": 2, "categoria": "comida", "monto": 12000},
        {"id": 3, "categoria": "ocio", "monto": 800},
    ]
    # Predict–Run: ¿qué crees que imprime cada línea ANTES de correrlo?
    print(categorias_unicas(datos))
    print(indexar_por_id(datos))
    print(list(stream_montos(datos, minimo=4000)))
