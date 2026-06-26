"""Tests del ejercicio 1.2 — Decorador de reintento y context manager.

Estos tests definen el CONTRATO. Hazlos pasar todos en verde. Luego AÑADE al menos
un caso borde tuyo.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""

import pytest

from robustez import conexion, reintentar


# --- reintentar (decorador parametrizado) ---

def test_exito_inmediato_devuelve_resultado():
    @reintentar(veces=3)
    def siempre_ok():
        return 42

    assert siempre_ok() == 42


def test_reintenta_hasta_acertar():
    llamadas = {"n": 0}

    @reintentar(veces=3)
    def falla_y_luego_acierta():
        llamadas["n"] += 1
        if llamadas["n"] < 3:
            raise ValueError("aún no")
        return "ok"

    assert falla_y_luego_acierta() == "ok"
    assert llamadas["n"] == 3  # falló 2 veces, acertó a la tercera


def test_relanza_la_ultima_excepcion_si_todas_fallan():
    llamadas = {"n": 0}

    @reintentar(veces=3)
    def siempre_falla():
        llamadas["n"] += 1
        raise RuntimeError(f"fallo #{llamadas['n']}")

    with pytest.raises(RuntimeError):
        siempre_falla()
    assert llamadas["n"] == 3  # se intentó exactamente `veces` veces


def test_preserva_el_nombre_de_la_funcion():
    @reintentar(veces=2)
    def descargar_datos():
        return None

    # functools.wraps mantiene la identidad de la función original.
    assert descargar_datos.__name__ == "descargar_datos"


# --- conexion (context manager) ---

def test_conexion_registra_apertura_y_cierre():
    log: list = []
    with conexion(log) as recurso:
        assert recurso is log          # entrega la misma lista
        recurso.append("trabajando")
    assert log == ["conectado", "trabajando", "desconectado"]


def test_conexion_cierra_aunque_el_bloque_lance_excepcion():
    log: list = []
    with pytest.raises(ValueError):
        with conexion(log) as recurso:
            recurso.append("trabajando")
            raise ValueError("boom")     # la excepción debe propagarse
    # ...y aun así el recurso se cerró:
    assert log == ["conectado", "trabajando", "desconectado"]


# TODO(estudiante): añade aquí al menos un caso borde tuyo.
# def test_mi_caso_borde():
#     assert ...
