"""Red de caracterización — el PRIMER artefacto del capstone.

Un test de caracterización (a.k.a. "golden master") NO comprueba lo que el código
*debería* hacer: fija lo que el código **hace hoy**, para que cualquier refactor
que cambie el comportamiento te grite al instante. Es tu permiso para tocar
producción sin romper nada a ciegas.

Fíjate que pasamos `hoy=date(2026, 6, 26)` para que el test sea DETERMINISTA: un
test que dependa de `date.today()` real pasaría hoy y fallaría mañana solo.

Corre:
    uv run pytest -q
"""

from datetime import date
from pathlib import Path

from despensa import run

DATOS = Path(__file__).parent / "datos" / "despensa-ejemplo.json"


def test_caracterizacion_alertas():
    """Pin del comportamiento actual de `despensa.run` con datos fijos."""
    resultado = run(str(DATOS), hoy=date(2026, 6, 26))
    assert resultado == [
        "Leche: STOCK BAJO + POR VENCER",
        "Arroz: VENCIDO",
        "Huevos: STOCK BAJO",
    ]


# TODO(estudiante): cuando extraigas el núcleo puro (p. ej. una función
# `evaluar(item, hoy)`), muévete a tests UNITARIOS sobre ella y agrega los tests
# de BORDE que mutmut te exija (cantidad == 2, días == 0, días == 3). Mantén este
# test de caracterización verde durante todo el refactor: es tu red de seguridad.
