"""Suite de tests para el extractor de pedidos (Ejercicio 2.11).

Escribe los tests donde dice TODO. NO modifiques `solucion.py`.

Idea central: la frontera (el LLM) se INYECTA como un callable. En los tests la
reemplazas por un "fake": una función determinista que devuelve lo que tú
decidas. Así pruebas TU código sin red, sin costo y sin no-determinismo.

Lo que NO pruebas aquí: si el modelo "extrae bien". Eso es un eval (Fase 6). Tus
fakes devuelven respuestas que TÚ escribes; el assert verifica que tu código las
parsea y valida, no que el modelo acierte.
"""

import pytest
from unittest.mock import Mock

# Autochequeo: para cazar el mutante, cambia SOLO esta línea a
#   from mutantes.mutante_a import (...)
# corre pytest (debe quedar ROJA), y luego REVIERTE a `solucion`.
from solucion import (
    Pedido,
    ExtraccionInvalida,
    extraer_pedido,
    construir_prompt,
    INSTRUCCION,
)


def fake_llm(respuesta):
    """Devuelve un callable `generar(prompt) -> str` que SIEMPRE responde `respuesta`.

    Es un STUB: ignora el prompt y entrega una respuesta fija que tú controlas.
    Recuerda: la frontera real devuelve TEXTO (un string), no un dict ya parseado.
    """
    def generar(prompt):
        return respuesta
    return generar


# --- TODO 1: happy path -------------------------------------------------------
# Con una respuesta JSON válida del modelo, extraer_pedido devuelve el Pedido
# correcto. Usa fake_llm('{"producto": "café", "cantidad": 2}') y afirma el Pedido.
# def test_extrae_pedido_valido():
#     ...


# --- TODO 2: construcción del prompt (usa un Mock como spy) -------------------
# Verifica que el prompt enviado al modelo CONTIENE el mensaje del cliente.
# Pista: generar = Mock(return_value='{"producto": "café", "cantidad": 2}')
#        prompt_enviado = generar.call_args.args[0]
# def test_el_prompt_incluye_el_mensaje():
#     ...


# --- TODO 3: el modelo no devuelve JSON -> ExtraccionInvalida -----------------
# Pista: fake_llm("Claro, el cliente quiere 2 cafés :)")
# def test_respuesta_no_json_lanza_error():
#     ...


# --- TODO 4: cantidad inválida -> ExtraccionInvalida (caza al mutante_a) ------
# Una cantidad ≤ 0 (o no entera) debe ser rechazada. Este test es el que pone
# ROJA tu suite contra mutantes.mutante_a.
# def test_cantidad_no_positiva_lanza_error():
#     ...


# --- TODO 5: mensaje vacío -> ExtraccionInvalida SIN llamar al modelo ---------
# El mensaje vacío ni siquiera debe gastar una llamada al LLM.
# Pista: usa un Mock como `generar` y afirma generar.assert_not_called().
# def test_mensaje_vacio_no_llama_al_modelo():
#     ...
