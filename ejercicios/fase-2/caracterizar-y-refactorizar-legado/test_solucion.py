"""TU red de seguridad — la construyes tú (este es el punto del ejercicio).

Un *characterization test* (o "golden master") NO afirma lo que la función
DEBERÍA hacer: afirma lo que la función HACE HOY. Lo obtienes leyendo el código
(o ejecutándolo una vez por caso y copiando el resultado) y lo congelas en un
assert. Esa red es lo que te permite refactorizar después sin romper nada.

Tu tarea (paso 1, ANTES de tocar `solucion.py`):
- Completa la tabla de `parametrize` con casos que cubran CADA rama y CADA borde:
  pesos 499/500, 1999/2000 (zonas 1 y 2) y 999/1000 (zona 3).
- Añade el caso raro: ¿qué devuelve una `zona` desconocida como 5? Píntalo tal
  cual es, no como crees que "debería" ser.
- Corre `pytest` hasta tener TODO en verde contra el código sin modificar.

    uv run pytest        # o:  pytest

Recién entonces refactoriza `solucion.py` (paso 2) y vuelve a correr esta suite:
debe seguir verde sin que cambies un solo `esperado`.
"""

import pytest

from solucion import etiqueta_envio


@pytest.mark.parametrize(
    "peso_gramos, zona, esperado",
    [
        (499, 1, "local-ligero"),   # ← ejemplo dado; COMPLETA el resto de los casos
        # TODO(estudiante): bordes de zona 1 (500, 1999, 2000)
        # TODO(estudiante): zona 2 completa (499, 500, 1999, 2000)
        # TODO(estudiante): zona 3 con su umbral distinto (999, 1000)
        # TODO(estudiante): zona desconocida (p. ej. 5) — pinta el comportamiento REAL
    ],
)
def test_caracteriza_etiqueta_envio(peso_gramos, zona, esperado):
    assert etiqueta_envio(peso_gramos, zona) == esperado
