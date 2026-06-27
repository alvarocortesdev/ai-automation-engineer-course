"""Tests del ejercicio — verifican que usaste la API v1 VIGENTE de Azure OpenAI.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes el entorno

La mayoría son tests ESTRUCTURALES: parsean el texto de `solucion.py` (no llaman
a la red). El último construye el cliente de verdad y comprueba su `base_url`;
si el paquete `openai` no está instalado, se omite (no falla).
"""

import importlib.util
import os
from pathlib import Path

import pytest

SRC = Path(__file__).parent / "solucion.py"
CODE = SRC.read_text(encoding="utf-8")


def _sin_comentarios(texto: str) -> str:
    """Quita las líneas de comentario para no dar falsos positivos en los asserts."""
    lineas = []
    for linea in texto.splitlines():
        sin = linea.split("#", 1)[0]
        lineas.append(sin)
    return "\n".join(lineas)


CODIGO = _sin_comentarios(CODE)


def test_usa_cliente_openai_no_azureopenai():
    assert "OpenAI(" in CODIGO, "Debes construir un cliente con OpenAI(...)."
    assert "AzureOpenAI" not in CODIGO, (
        "La API v1 GA usa el cliente estándar OpenAI(), NO AzureOpenAI()."
    )


def test_base_url_apunta_a_v1():
    assert "/openai/v1" in CODIGO, (
        "base_url debe apuntar a <endpoint>/openai/v1/ : esa ruta activa la API v1."
    )


def test_sin_api_version():
    assert "api_version" not in CODIGO, (
        "La API v1 GA eliminó api_version. No lo pases."
    )


def test_config_desde_el_entorno():
    leído = ("os.environ" in CODIGO) or ("os.getenv" in CODIGO)
    assert leído, "El endpoint y la clave deben venir del entorno, no hardcodeados."
    assert "AZURE_OPENAI_ENDPOINT" in CODIGO, "Lee AZURE_OPENAI_ENDPOINT del entorno."
    assert "AZURE_OPENAI_API_KEY" in CODIGO, "Lee AZURE_OPENAI_API_KEY del entorno."


def test_sin_secretos_hardcodeados():
    # No debe aparecer una URL de recurso ni una clave pegada en el código.
    assert ".openai.azure.com\"" not in CODIGO and ".openai.azure.com'" not in CODIGO, (
        "No hardcodees el endpoint: arma base_url desde AZURE_OPENAI_ENDPOINT."
    )


def test_responder_usa_deployment_en_model():
    assert "chat.completions.create" in CODIGO, (
        "responder() debe llamar a client.chat.completions.create(...)."
    )
    assert "model=deployment" in CODIGO.replace(" ", "") or "model = deployment" in CODE, (
        "model= debe ser el parámetro `deployment` (el nombre del deployment de Azure)."
    )
    assert "choices[0].message.content" in CODIGO, (
        "Devuelve el texto: choices[0].message.content."
    )


def test_construye_cliente_real():
    """Si openai está instalado, construye el cliente y comprueba el base_url."""
    pytest.importorskip("openai")
    os.environ.setdefault("AZURE_OPENAI_ENDPOINT", "https://demo.openai.azure.com")
    os.environ.setdefault("AZURE_OPENAI_API_KEY", "clave-de-prueba")

    spec = importlib.util.spec_from_file_location("solucion", SRC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    client = mod.build_client()
    assert "/openai/v1" in str(client.base_url), (
        f"El base_url del cliente debe contener /openai/v1 (es: {client.base_url})."
    )


# TODO(estudiante): añade un test propio. Idea: que build_client() funcione
# tanto si AZURE_OPENAI_ENDPOINT termina en '/' como si no (sin // duplicada).
