"""Red de seguridad del ejercicio — NO la modifiques para hacerla pasar.

Estos tests pintan el comportamiento ACTUAL de `calc`. Tu refactoring es correcto
si y solo si TODOS siguen en verde después de cada paso. Los montos involucran
`float` (el descuento y el IVA), así que comparamos con `pytest.approx`: tolerancia
mínima, sin exigir igualdad bit a bit (lo viste en 1.6, sección 4.7).

Única edición permitida: si renombras la función pública `calc`, ajusta la línea
`from solucion import calc` (y solo esa). NO toques las aserciones ni los casos.

Corre:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""

import pytest

from solucion import calc


@pytest.mark.parametrize(
    "items, cliente, cupon, esperado",
    [
        # (subtotal, descuento, envío, IVA) -> total
        ([("pan", 10000, 2)], "normal", None, 27790.0),          # sin desc, envío 3990
        ([("tv", 60000, 1)], "vip", None, 64260.0),              # vip 10%, envío gratis (>50k)
        ([("tv", 100000, 2)], "vip", "ENVIOGRATIS", 190400.0),   # vip 20% (>100k) + cupón
        ([("zapato", 50000, 1)], "frecuente", None, 60515.0),    # frecuente 5%, envío 3990
        ([("tv", 120000, 1)], "frecuente", None, 128520.0),      # frecuente 10% (>100k)
        ([("a", 70000, 2)], "vip", "ENVIOGRATIS", 133280.0),     # vip 20% + cupón
        ([("a", 1000, 3), ("b", 2000, 1)], "normal", None, 9940.0),  # 2 ítems, normal
    ],
)
def test_total_orden_preserva_comportamiento(items, cliente, cupon, esperado):
    assert calc(items, cliente, cupon) == pytest.approx(esperado)


def test_cupon_envio_gratis_anula_el_envio():
    # Mismo carrito chico: con cupón el envío es 0; sin cupón, 3990.
    con_cupon = calc([("x", 10000, 1)], "normal", "ENVIOGRATIS")
    sin_cupon = calc([("x", 10000, 1)], "normal", None)
    assert sin_cupon - con_cupon == pytest.approx(3990.0)


def test_carrito_vacio_es_cero():
    # Sin ítems: subtotal 0, sin descuento, envío 3990 (0 no supera 50000), IVA 0.
    assert calc([], "normal", None) == pytest.approx(3990.0)
