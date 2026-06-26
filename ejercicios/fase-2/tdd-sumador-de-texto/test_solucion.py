"""Tus tests — uno por comportamiento, escritos por TI.

El andamiaje se desvanece: te dejamos escrito SOLO el primer test (comportamiento 1)
como molde del estilo. Tú escribes los demás, en orden, viendo el ROJO antes del
VERDE en cada ciclo. NO escribas implementación en solucion.py sin un test rojo.

Corre:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

Recuerda anotar cada ciclo en bitacora.md (🔴 -> 🟢 -> 🔵).
"""

import pytest

from solucion import sumar


# --- Comportamiento 1 (te lo damos como molde) -------------------------------
def test_cadena_vacia_suma_cero():
    assert sumar("") == 0


# --- Comportamiento 2: sumar("1") == 1 ---------------------------------------
# TODO(estudiante): escribe el test. Córrelo, ve el ROJO, recién entonces el código.


# --- Comportamiento 3: sumar("1,2") == 3 -------------------------------------
# TODO(estudiante)


# --- Comportamiento 4: sumar("1,2,3,4") == 10 (cualquier cantidad) -----------
# TODO(estudiante)


# --- Comportamiento 5: sumar("1\n2,3") == 6 (el \n también separa) -----------
# TODO(estudiante)  — aquí probablemente tengas que REFACTORIZAR (en verde).


# --- Comportamiento 6: sumar(" 1 , 2 ") == 3 (ignora espacios) ---------------
# TODO(estudiante)


# --- Comportamiento 7: sumar("1,-2,3") lanza ValueError con el negativo ------
# TODO(estudiante)  — usa: with pytest.raises(ValueError, match="-2"): ...
