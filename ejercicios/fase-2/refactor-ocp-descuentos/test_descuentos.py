"""Tests del ejercicio — son tu RED DE SEGURIDAD.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

Estos tests describen el comportamiento que tu refactor DEBE preservar. Pasan
en verde contra el `descuentos.py` original. Después de refactorizar a Open/Closed,
deben SEGUIR pasando SIN que los hayas modificado. Si necesitas cambiar un test
para que pase, cambiaste el comportamiento: revisa tu refactor.

Lo único que agregas a este archivo es:
  - el test del tipo "mayorista" (25%) que prueba tu extensión (TODO al final).
  - al menos un caso borde tuyo.
"""

import pytest

from descuentos import calcular_descuento


@pytest.mark.parametrize(
    "cliente_tipo, monto, esperado",
    [
        ("regular", 10_000, 0),
        ("vip", 10_000, 1_000),
        ("empleado", 10_000, 3_000),
        ("estudiante", 10_000, 1_500),
        ("jubilado", 10_000, 2_000),
    ],
)
def test_descuento_por_tipo(cliente_tipo, monto, esperado):
    assert calcular_descuento(cliente_tipo, monto) == esperado


def test_tipo_desconocido_no_da_descuento():
    assert calcular_descuento("fantasma", 10_000) == 0


def test_monto_cero_da_descuento_cero():
    # Caso borde: sin monto no hay descuento, sea cual sea el tipo.
    assert calcular_descuento("vip", 0) == 0


def test_redondeo_a_entero():
    # 10% de 999 = 99.9 → debe truncar a 99 (pesos enteros, sin float).
    assert calcular_descuento("vip", 999) == 99


# TODO(estudiante): tras agregar la clase del tipo "mayorista" (25%) en
# descuentos.py, escribe aquí su test. Debe pasar SIN tocar las clases existentes.
# def test_descuento_mayorista():
#     assert calcular_descuento("mayorista", 10_000) == 2_500
