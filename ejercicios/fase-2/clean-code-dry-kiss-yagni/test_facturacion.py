"""Tests del ejercicio 2.2 — DRY/KISS/YAGNI con criterio.

Estos tests definen el COMPORTAMIENTO que tu refactor debe PRESERVAR. Ya pasan en verde
con el código original y deben seguir verdes después de tu refactor.

Nota deliberada: los tests llaman a `formatear_precio` SOLO con un argumento (`formatear_precio(monto)`).
Eso es justo lo que de verdad se usa: si tu refactor simplifica la firma (YAGNI), los tests
siguen pasando. Los tests tampoco te obligan a unir ni a separar los validadores: esa
decisión de criterio la justificas en `decisiones.md` y la juzga la rúbrica.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""

from facturacion import (
    es_rut_valido,
    es_sku_valido,
    formatear_precio,
    precio_con_iva,
    precio_con_iva_descuento,
)


# --- IVA (duplicación REAL: debe quedar en un solo lugar) ---

def test_precio_con_iva():
    assert precio_con_iva(10000) == 11900


def test_precio_con_iva_cero():
    assert precio_con_iva(0) == 0


def test_precio_con_iva_descuento():
    # 10000 - 1000 = 9000; 9000 + int(9000*0.19) = 9000 + 1710 = 10710
    assert precio_con_iva_descuento(10000, 0.10) == 10710


def test_precio_con_iva_descuento_cero_equivale_a_solo_iva():
    assert precio_con_iva_descuento(10000, 0.0) == precio_con_iva(10000)


# --- validadores (duplicación INCIDENTAL: deben seguir funcionando por separado) ---

def test_rut_valido():
    assert es_rut_valido("12345678-9") is True


def test_rut_invalido_muy_corto():
    assert es_rut_valido("ab") is False


def test_rut_invalido_no_es_str():
    assert es_rut_valido(12345678) is False


def test_sku_valido():
    assert es_sku_valido("ABC-100") is True


def test_sku_invalido_muy_corto():
    assert es_sku_valido("XY") is False


# --- formateo (sobre-ingeniería: solo se usa formatear_precio(monto)) ---

def test_formatear_precio_separa_miles_con_punto():
    assert formatear_precio(1234) == "$1.234"


def test_formatear_precio_cero():
    assert formatear_precio(0) == "$0"


def test_formatear_precio_millon():
    assert formatear_precio(1000000) == "$1.000.000"


# TODO(estudiante): añade aquí al menos un caso borde tuyo.
# def test_mi_caso_borde():
#     assert ...
