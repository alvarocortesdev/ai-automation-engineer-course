"""Ejercicio 0.7 — Resumen de gastos por categoría (Primero-Sin-IA).

Completa la función `total_por_categoria`. NO cambies su firma.

Corre los tests con:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""


def total_por_categoria(gastos):
    """Suma los montos de una lista de gastos, agrupados por categoría.

    Cada gasto es un dict con las claves:
      - "categoria": str no vacío
      - "monto": int o float, mayor o igual a 0

    Devuelve un dict {categoria: total}. Una lista vacía devuelve {}.

    Validación (lanza ValueError con un mensaje claro):
      - monto negativo o ausente        -> ValueError
      - categoria vacía, None o ausente -> ValueError

    Ejemplo:
        >>> total_por_categoria([
        ...     {"categoria": "comida", "monto": 5000},
        ...     {"categoria": "comida", "monto": 3500},
        ...     {"categoria": "transporte", "monto": 1200},
        ... ])
        {'comida': 8500, 'transporte': 1200}
    """
    # TODO(estudiante): borra esta línea y escribe tu solución a mano, sin IA.
    raise NotImplementedError("Implementa total_por_categoria")
