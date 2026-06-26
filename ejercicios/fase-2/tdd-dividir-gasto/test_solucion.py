"""Tus tests — uno por comportamiento, escritos por TI.

El andamiaje se desvanece: te dejamos escrito SOLO el primer test (comportamiento 1).
Tú escribes los demás, en orden, viendo el ROJO antes del VERDE en cada ciclo. NO
escribas implementación en solucion.py sin un test rojo que la exija.

Corre:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

Recuerda anotar cada ciclo en bitacora.md (🔴 -> 🟢 -> 🔵).
"""

import pytest

from solucion import dividir_gasto


# --- Comportamiento 1 (te lo damos como molde) -------------------------------
def test_division_exacta():
    assert dividir_gasto(100, 2) == [50, 50]


# --- Comportamiento 2: dividir_gasto(100, 3) == [34, 33, 33] -----------------
# TODO(estudiante): este test ROMPE la división entera simple. Velo en ROJO primero.


# --- Comportamiento 3: dividir_gasto(10, 4) == [3, 3, 2, 2] ------------------
# TODO(estudiante)


# --- Comportamiento 4: dividir_gasto(0, 3) == [0, 0, 0] ----------------------
# TODO(estudiante)


# --- Comportamiento 5: dividir_gasto(100, 1) == [100] ------------------------
# TODO(estudiante)


# --- Comportamiento 6: dividir_gasto(100, 0) lanza ValueError ----------------
# TODO(estudiante)  — usa: with pytest.raises(ValueError): ...


# --- Comportamiento 7: dividir_gasto(-100, 2) lanza ValueError ---------------
# TODO(estudiante)


# --- Comportamiento 8 (INVARIANTE): la suma debe dar el monto ----------------
# TODO(estudiante): para algún caso no exacto, assert sum(dividir_gasto(m, p)) == m
