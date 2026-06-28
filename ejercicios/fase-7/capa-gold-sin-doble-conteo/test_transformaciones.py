"""Tests de la capa gold — definen el contrato.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

No edites estos tests para "hacerlos pasar" cambiando el contrato: implementa
`transformaciones.py` hasta que pasen en verde. El test clave es
`test_envio_no_se_duplica_con_varias_lineas`: detecta el FAN-OUT (doble conteo)
que aparece si aplanas líneas con órdenes y sumas el envío por línea.
"""

from transformaciones import ingresos_por_categoria, valor_total_por_cliente

# ── Fixtures de datos (silver) ────────────────────────────────────────────────

PRODUCTOS = [
    {"producto_id": "P1", "categoria": "electro"},
    {"producto_id": "P2", "categoria": "hogar"},
    {"producto_id": "P3", "categoria": "electro"},
    {"producto_id": "P9", "categoria": "jardin"},  # existe en la dim pero SIN ventas
]

ORDENES = [
    {"orden_id": "O1", "cliente_id": "C1", "envio": 3000},
    {"orden_id": "O2", "cliente_id": "C2", "envio": 2000},
]

# O1 (de C1) tiene 3 líneas; O2 (de C2) tiene 1 línea.
LINEAS = [
    {"orden_id": "O1", "producto_id": "P1", "cantidad": 1, "monto": 10000},
    {"orden_id": "O1", "producto_id": "P2", "cantidad": 2, "monto": 5000},
    {"orden_id": "O1", "producto_id": "P1", "cantidad": 1, "monto": 10000},
    {"orden_id": "O2", "producto_id": "P3", "cantidad": 1, "monto": 8000},
]


# ── ingresos_por_categoria ────────────────────────────────────────────────────

def test_ingresos_por_categoria_suma_por_categoria():
    out = ingresos_por_categoria(LINEAS, PRODUCTOS)
    # electro = P1(10000) + P1(10000) + P3(8000) = 28000 ; hogar = P2(5000)
    assert out == {"electro": 28000, "hogar": 5000}


def test_categoria_sin_ventas_no_aparece():
    out = ingresos_por_categoria(LINEAS, PRODUCTOS)
    assert "jardin" not in out  # P9 está en la dim pero no tiene líneas


def test_ingresos_listas_vacias():
    assert ingresos_por_categoria([], PRODUCTOS) == {}


# ── valor_total_por_cliente ───────────────────────────────────────────────────

def test_valor_total_por_cliente_combina_lineas_y_envio():
    out = valor_total_por_cliente(LINEAS, ORDENES)
    # C1: líneas 10000+5000+10000=25000 + envío O1 (una vez) 3000 = 28000
    # C2: líneas 8000 + envío O2 2000 = 10000
    assert out == {"C1": 28000, "C2": 10000}


def test_envio_no_se_duplica_con_varias_lineas():
    """El test que caza el FAN-OUT.

    O1 tiene 3 líneas y envío 3000. Si sumas el envío por línea (aplanando), C1
    daría 25000 + 3000*3 = 34000 (INFLADO). El correcto cuenta el envío UNA vez:
    25000 + 3000 = 28000.
    """
    out = valor_total_por_cliente(LINEAS, ORDENES)
    assert out["C1"] == 28000, "El envío se está contando una vez por línea (fan-out)"
    assert out["C1"] != 34000


def test_cliente_con_multiples_ordenes_suma_cada_envio_una_vez():
    ordenes = [
        {"orden_id": "O1", "cliente_id": "C1", "envio": 3000},
        {"orden_id": "O3", "cliente_id": "C1", "envio": 1500},
    ]
    lineas = [
        {"orden_id": "O1", "producto_id": "P1", "cantidad": 1, "monto": 10000},
        {"orden_id": "O1", "producto_id": "P1", "cantidad": 1, "monto": 10000},
        {"orden_id": "O3", "producto_id": "P2", "cantidad": 1, "monto": 4000},
    ]
    out = valor_total_por_cliente(lineas, ordenes)
    # C1: líneas 24000 + envíos (3000 + 1500) = 28500
    assert out == {"C1": 28500}


def test_valor_listas_vacias():
    assert valor_total_por_cliente([], []) == {}


# TODO(estudiante): añade un caso tuyo. Sugerencia: dos clientes distintos, cada
# uno con su orden, para confirmar que los envíos no se mezclan entre clientes;
# o una orden sin líneas (solo costo de envío) y decide qué debería pasar.
# def test_mi_caso():
#     ...
