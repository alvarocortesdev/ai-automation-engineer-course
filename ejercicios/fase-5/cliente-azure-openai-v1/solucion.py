"""Starter del ejercicio — Primero-Sin-IA.

Implementa a mano, sin IA, el cliente VIGENTE (2026) para llamar a un modelo en
Azure OpenAI Service usando la API v1 GA. NO cambies las firmas: los tests de
`test_solucion.py` dependen de ellas.

Contrato (lee la sección 4.3–4.4 de la lección 5.6 si te trabas):

  build_client() -> OpenAI
    - Usa el cliente ESTÁNDAR `OpenAI()` (NO `AzureOpenAI()`).
    - base_url = <endpoint>/openai/v1/   (esa ruta activa la API v1)
    - endpoint y clave salen del ENTORNO:
        AZURE_OPENAI_ENDPOINT  -> p. ej. https://mi-recurso.openai.azure.com
        AZURE_OPENAI_API_KEY   -> tu clave
      Nunca los hardcodees (factor III, 12-factor).
    - NO pases `api_version` (la API v1 lo eliminó).

  responder(client, deployment, pregunta) -> str
    - Llama a client.chat.completions.create con model=<deployment>
      (¡el nombre del DEPLOYMENT, no del modelo base!) y un único mensaje
      de usuario con `pregunta`.
    - Devuelve el texto: choices[0].message.content
"""

import os

from openai import OpenAI


def build_client() -> OpenAI:
    """Devuelve un cliente OpenAI apuntado a tu recurso de Azure OpenAI (API v1)."""
    raise NotImplementedError("Implementa esta función a mano, sin IA.")


def responder(client: OpenAI, deployment: str, pregunta: str) -> str:
    """Hace una llamada de chat y devuelve el texto de la respuesta."""
    raise NotImplementedError("Implementa esta función a mano, sin IA.")


if __name__ == "__main__":
    # Prueba manual (necesita un recurso real + variables de entorno):
    #   export AZURE_OPENAI_ENDPOINT="https://mi-recurso.openai.azure.com"
    #   export AZURE_OPENAI_API_KEY="..."
    cliente = build_client()
    print(responder(cliente, "gpt-4.1-mini-prod", "Di 'hola' en una palabra."))
