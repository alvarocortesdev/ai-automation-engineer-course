"""TUS tests — este archivo es el entregable principal del ejercicio.

La gracia de este ejercicio es que TÚ escribes la suite, dirigida por tests:
1. Escribe el test (abajo hay UNA semilla para arrancar).
2. Córrelo y míralo en ROJO  ->  `uv run pytest`  (o  `pytest`).
3. Implementa el mínimo en solucion.py para ponerlo en VERDE.
4. Refactoriza. Repite por cada punto del contrato (ver README / solucion.py).

Cubre, como mínimo:
  - camino feliz con @pytest.mark.parametrize (varios montos y pct),
  - pct_propina == 0  -> total == monto,
  - monto negativo    -> ValueError   (pytest.raises),
  - pct fuera de [0,100] -> ValueError (pytest.raises),
  - al menos UN caso borde tuyo.
"""

import pytest

from solucion import total_con_propina


# --- Semilla: el test más simple posible. Míralo en ROJO antes de implementar. ---
def test_propina_10_pct_de_10000():
    # Arrange / Act / Assert
    assert total_con_propina(10000, 10) == 11000


# TODO(estudiante): agrega un test parametrizado para el camino feliz.
# @pytest.mark.parametrize("monto, pct, esperado", [
#     (10000, 10, 11000),
#     ( 5000,  0,  5000),
#     ( 8000, 100, 16000),
# ])
# def test_total_camino_feliz(monto, pct, esperado):
#     assert total_con_propina(monto, pct) == esperado


# TODO(estudiante): agrega los tests de error con pytest.raises (monto negativo,
# pct fuera de rango) y al menos un caso borde propio.
