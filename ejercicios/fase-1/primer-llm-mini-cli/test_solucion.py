"""Tests del ejercicio — definen el contrato.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

NINGÚN test toca la red ni usa una API key real. El "modelo" siempre es un fake
inyectado, y el "entorno" siempre es un dict que tú controlas. Ese es el punto
del ejercicio: testear código que llama a un LLM sin red ni tokens gastados.
"""

import pytest

from solucion import (
    FaltaApiKey,
    ModeloInalcanzable,
    PromptVacio,
    leer_api_key,
    main,
    responder,
)


# ---------- fakes (modelo inyectado, sin red) ----------

def modelo_que_devuelve(texto):
    """Crea un fake que ignora el prompt y siempre devuelve `texto`."""
    return lambda prompt: texto


def modelo_que_lanza(exc):
    """Crea un fake que siempre lanza `exc` (simula un fallo del servicio)."""
    def _fake(prompt):
        raise exc
    return _fake


def modelo_que_no_debe_correr(prompt):
    """Si esto se llama, el código gastó una llamada que no debía: falla el test."""
    raise AssertionError("preguntar_al_modelo NO debía llamarse para este input")


# ---------- leer_api_key ----------

def test_leer_api_key_presente():
    assert leer_api_key({"ANTHROPIC_API_KEY": "sk-ant-test"}) == "sk-ant-test"


def test_leer_api_key_ausente_lanza():
    with pytest.raises(FaltaApiKey):
        leer_api_key({})


def test_leer_api_key_vacia_lanza():
    with pytest.raises(FaltaApiKey):
        leer_api_key({"ANTHROPIC_API_KEY": "   "})


# ---------- responder ----------

def test_responder_devuelve_el_texto():
    fake = modelo_que_devuelve("Una API es un contrato entre programas.")
    assert responder("¿qué es una API?", fake) == "Una API es un contrato entre programas."


def test_responder_recorta_espacios():
    fake = modelo_que_devuelve("  hola  \n")
    assert responder("saluda", fake) == "hola"


def test_responder_prompt_vacio_no_llama_al_modelo():
    with pytest.raises(PromptVacio):
        responder("", modelo_que_no_debe_correr)


def test_responder_prompt_solo_espacios_lanza():
    with pytest.raises(PromptVacio):
        responder("    ", modelo_que_no_debe_correr)


def test_responder_propaga_error_del_modelo():
    fake = modelo_que_lanza(ModeloInalcanzable("servicio caído"))
    with pytest.raises(ModeloInalcanzable):
        responder("hola", fake)


# ---------- main (CLI) ----------

def test_main_exito_imprime_y_devuelve_0(capsys):
    fake = modelo_que_devuelve("respuesta del modelo")
    codigo = main(["¿qué", "es", "un", "embedding?"], {"ANTHROPIC_API_KEY": "sk-ant-x"}, preguntar=fake)
    salida = capsys.readouterr()
    assert codigo == 0
    assert "respuesta del modelo" in salida.out


def test_main_sin_prompt_devuelve_2():
    codigo = main([], {"ANTHROPIC_API_KEY": "sk-ant-x"}, preguntar=modelo_que_no_debe_correr)
    assert codigo == 2


def test_main_sin_api_key_devuelve_3():
    # Falta la key: no debe gastar una llamada al modelo.
    codigo = main(["hola"], {}, preguntar=modelo_que_no_debe_correr)
    assert codigo == 3


def test_main_modelo_inalcanzable_devuelve_4():
    fake = modelo_que_lanza(ModeloInalcanzable("timeout"))
    codigo = main(["hola"], {"ANTHROPIC_API_KEY": "sk-ant-x"}, preguntar=fake)
    assert codigo == 4


# TODO(estudiante): añade aquí al menos un caso borde tuyo.
# Ideas: ¿qué pasa con un prompt de un solo carácter? ¿Y si el modelo devuelve ""?
# def test_mi_caso_borde():
#     ...
