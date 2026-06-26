"""Tests del ejercicio 1.9 — Excepciones de dominio en Python.

Estos tests son el CONTRATO. Cada uno fija una decisión de diseño:
la unidad LANZA, el lote DEVUELVE los errores como datos, y el monto no-entero
ENCADENA su causa. Hazlos pasar todos y luego AÑADE un caso borde tuyo.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""

import pytest

from gastos import ErrorLinea, Gasto, LineaInvalida, parsear_archivo, parsear_linea


# --- parsear_linea: la unidad LANZA ---

def test_linea_valida_devuelve_gasto():
    g = parsear_linea("Lider;12990;supermercado")
    assert g == Gasto(comercio="Lider", monto=12990, categoria="supermercado")


def test_linea_valida_hace_strip():
    g = parsear_linea("  Lider ; 12990 ; supermercado ")
    assert g.comercio == "Lider"
    assert g.categoria == "supermercado"


def test_campos_de_mas_o_de_menos_lanza():
    with pytest.raises(LineaInvalida):
        parsear_linea("Lider;12990")            # solo 2 campos
    with pytest.raises(LineaInvalida):
        parsear_linea("Lider;12990;super;extra")  # 4 campos


def test_monto_no_entero_lanza():
    with pytest.raises(LineaInvalida):
        parsear_linea("Lider;abc;supermercado")


def test_monto_no_entero_encadena_la_causa():
    # El `from e` debe preservar el ValueError original en __cause__.
    with pytest.raises(LineaInvalida) as exc_info:
        parsear_linea("Lider;abc;supermercado")
    assert isinstance(exc_info.value.__cause__, ValueError)


def test_monto_negativo_o_cero_lanza():
    with pytest.raises(LineaInvalida):
        parsear_linea("Lider;-5;supermercado")
    with pytest.raises(LineaInvalida):
        parsear_linea("Lider;0;supermercado")


def test_comercio_o_categoria_vacios_lanza():
    with pytest.raises(LineaInvalida):
        parsear_linea(";12990;supermercado")
    with pytest.raises(LineaInvalida):
        parsear_linea("Lider;12990;   ")        # solo espacios -> vacío tras strip


# --- parsear_archivo: el lote DEVUELVE los errores como datos ---

def test_archivo_separa_validos_y_errores():
    texto = "Lider;12990;supermercado\n\nbasura\nKfc;-5;comida\n"
    #         linea 1: válida        ^l2 blanca  ^l3 mala  ^l4 mala
    gastos, errores = parsear_archivo(texto)

    assert len(gastos) == 1
    assert gastos[0].comercio == "Lider"

    assert len(errores) == 2
    assert all(isinstance(e, ErrorLinea) for e in errores)
    assert {e.numero for e in errores} == {3, 4}   # la blanca (2) NO es error


def test_archivo_no_se_cae_con_linea_mala():
    # Aunque la primera línea sea inválida, debe seguir procesando.
    texto = "rota\nLider;12990;supermercado\n"
    gastos, errores = parsear_archivo(texto)
    assert len(gastos) == 1
    assert len(errores) == 1


def test_archivo_vacio_devuelve_listas_vacias():
    gastos, errores = parsear_archivo("")
    assert gastos == []
    assert errores == []


# TODO(estudiante): añade aquí al menos un caso borde tuyo.
# Ideas: un archivo de puras líneas en blanco; una línea con monto "12.5";
# verificar que ErrorLinea.contenido guarda la línea original tal cual.
