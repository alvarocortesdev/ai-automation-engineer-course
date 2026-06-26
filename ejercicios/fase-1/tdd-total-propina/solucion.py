"""Starter del ejercicio — Primero-Sin-IA, dirigido por tests (TDD).

NO empieces escribiendo esta función. Empieza por el test (en test_solucion.py),
míralo en ROJO, y recién entonces escribe aquí el mínimo código para ponerlo en
VERDE. Repite por cada punto del contrato. Refactoriza al final.

Contrato de `total_con_propina(monto, pct_propina)` (la spec; tradúcela a tests):
  - Devuelve `monto + propina`, con `propina = round(monto * pct_propina / 100)`.
    Todo en PESOS ENTEROS (sin float en el resultado).
  - `monto` negativo            -> lanza ValueError
  - `pct_propina` fuera de [0,100] -> lanza ValueError
  - `pct_propina == 0`          -> el total es el monto (propina cero)

Lee la sección 4 de la lección 1.6 si te trabas. Trabaja en pasos chicos.
"""

from __future__ import annotations


def total_con_propina(monto: int, pct_propina: int) -> int:
    """Total de la cuenta con propina incluida. Ver contrato arriba."""
    raise NotImplementedError("Escribe el test primero (rojo). Luego implementa esto (verde).")


if __name__ == "__main__":
    # Predice qué imprime ANTES de correr. (Fallará hasta que implementes la función.)
    print(total_con_propina(10000, 10))   # esperado tras implementar: 11000
