"""Suite DÉBIL de partida — 100% de line coverage, y aun así llena de agujeros.

Estos cuatro tests pasan en VERDE y ejecutan TODAS las líneas de `descuento.py`
(coverage 100%). Pero ninguno pincha los BORDES exactos (puntos == 100, == 50),
así que varios mutantes de comparación sobreviven.

Tu tarea (ver README): predice a mano qué mutantes sobreviven, verifica con
`mutmut run`, y AGREGA aquí los tests de borde que los maten. NO debilites ni
borres estos tests; solo añade los que falten. NO toques `descuento.py`.

Corre:
    uv run pytest                 # confirma el verde de partida
    uv run pytest --cov=descuento # comprueba el 100% de coverage (engañoso)
    mutmut run                    # el mutation testing: la verdad real
"""

from descuento import descuento


def test_socio_con_muchos_puntos_obtiene_30():
    assert descuento(150, True) == 30


def test_no_socio_con_muchos_puntos_obtiene_20():
    assert descuento(150, False) == 20


def test_puntos_medios_obtiene_10():
    assert descuento(70, False) == 10


def test_pocos_puntos_obtiene_0():
    assert descuento(10, False) == 0


# TODO(estudiante): agrega aquí los tests de BORDE que matan a los sobrevivientes.
# Pista: ¿qué pasa EXACTAMENTE en puntos == 100 (socio y no socio) y en puntos == 50?
