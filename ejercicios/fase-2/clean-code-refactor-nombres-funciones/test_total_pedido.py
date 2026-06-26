"""Tests del ejercicio 2.2 — Refactor de `total_pedido`.

Estos tests definen el COMPORTAMIENTO que tu refactor debe PRESERVAR. Ya pasan en
verde con el código original. Deben seguir verdes después de cada paso de tu refactor:
si alguno se pone rojo, cambiaste comportamiento (y eso ya no es refactorizar).

Luego AÑADE al menos un caso borde tuyo.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""

from total_pedido import total_pedido

# (producto, precio, cantidad, activo)
PEDIDO = [
    ("pan", 1500, 2, True),       # 3000, activo
    ("leche", 1200, 1, False),    # inactivo: NO suma
    ("café", 8000, 1, True),      # 8000, activo
]


def test_pedido_vacio_da_cero():
    assert total_pedido([]) == 0


def test_suma_solo_lineas_activas():
    # 1500*2 + 8000*1 = 11000 (la leche inactiva no entra)
    assert total_pedido(PEDIDO) == 11000


def test_sin_descuento_bajo_el_umbral():
    # subtotal 11000 <= 100000 -> sin descuento
    assert total_pedido(PEDIDO) == 11000


def test_con_descuento_sobre_el_umbral():
    # 120000 > 100000 -> 120000 - 12000 = 108000
    assert total_pedido([("notebook", 120000, 1, True)]) == 108000


def test_en_el_umbral_exacto_no_hay_descuento():
    # 100000 NO es > 100000 -> sin descuento
    assert total_pedido([("monitor", 100000, 1, True)]) == 100000


def test_justo_sobre_el_umbral_si_hay_descuento():
    # 100001 > 100000 -> 100001 - int(100001*0.1) = 100001 - 10000 = 90001
    assert total_pedido([("equipo", 100001, 1, True)]) == 90001


def test_todas_inactivas_da_cero():
    assert total_pedido([("a", 5000, 3, False), ("b", 9000, 1, False)]) == 0


# TODO(estudiante): añade aquí al menos un caso borde tuyo.
# def test_mi_caso_borde():
#     assert total_pedido(...) == ...
