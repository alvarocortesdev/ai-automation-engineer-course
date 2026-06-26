"""Starter del ejercicio — Primero-Sin-IA.

Implementa las funciones a mano, sin IA. NO cambies sus firmas: los tests de
`test_solucion.py` dependen de ellas. Las excepciones de dominio ya están
definidas; las constantes MODELO y MAX_TOKENS también.

Ideas clave (todas vienen de 1.5 y 0.5):
  - La API key es un SECRETO: se lee del entorno, nunca se hardcodea ni se imprime.
  - `responder` recibe `preguntar_al_modelo` INYECTADO: no sabe de dónde viene la
    respuesta. Eso lo hace testeable sin red ni tokens (igual que `fetch` en 1.5).
  - La traducción de errores del SDK vive en el ADAPTADOR (`preguntar_a_claude`),
    no en la lógica (`responder`).

Lee la sección 4 de la lección si te trabas.
"""

from __future__ import annotations

import os
import sys
from typing import Callable, Mapping

# Modelo más barato y rápido: ideal para aprender y experimentar.
MODELO = "claude-haiku-4-5"
MAX_TOKENS = 1024

# `preguntar_al_modelo` recibe un prompt (str) y devuelve el texto del modelo (str).
Preguntar = Callable[[str], str]


class PromptVacio(ValueError):
    """El prompt está vacío o es solo espacios: no hay nada que preguntar."""


class FaltaApiKey(RuntimeError):
    """No hay API key en el entorno, o el servidor la rechazó."""


class ModeloInalcanzable(RuntimeError):
    """La llamada al modelo falló (red, rate limit, 5xx, etc.)."""


def leer_api_key(entorno: Mapping[str, str]) -> str:
    """Devuelve la API key desde `entorno` (p. ej. os.environ) o lanza FaltaApiKey.

    Contrato:
        entrada: un mapping de variables de entorno.
        salida:  el valor de "ANTHROPIC_API_KEY" si existe y no está vacío.
                 Si falta o es solo espacios -> lanza FaltaApiKey con un mensaje claro.
        NUNCA imprime ni registra el valor de la key.
    """
    raise NotImplementedError("Implementa esta función a mano, sin IA.")


def responder(prompt: str, preguntar_al_modelo: Preguntar) -> str:
    """Valida el prompt y delega en el modelo inyectado.

    Contrato:
        - prompt vacío o solo espacios -> lanza PromptVacio ANTES de llamar al modelo.
        - en otro caso: devuelve `preguntar_al_modelo(prompt)` sin espacios sobrantes.
        - NO atrapa los errores del modelo: que se propaguen (los mapea el adaptador).
    """
    raise NotImplementedError("Implementa esta función a mano, sin IA.")


def preguntar_a_claude(prompt: str) -> str:
    """Adaptador REAL: llama al LLM con el SDK oficial y devuelve el texto.

    No se testea offline (toca la red). Se ejercita al correr la CLI con una key real.
    Importa `anthropic` DENTRO de la función para que los tests corran sin el paquete.

    Mapea:
        anthropic.AuthenticationError -> FaltaApiKey
        anthropic.APIError            -> ModeloInalcanzable
    Devuelve `mensaje.content[0].text`.
    """
    raise NotImplementedError("Implementa esta función a mano, sin IA.")


def main(argv: list[str], entorno: Mapping[str, str], preguntar: Preguntar = preguntar_a_claude) -> int:
    """Punto de entrada de la mini-CLI. Devuelve un código de salida.

    Contrato:
        - arma el prompt uniendo `argv` con espacios.
        - sin prompt (o solo espacios) -> imprime el uso en stderr y devuelve 2.
        - si falta la API key (leer_api_key lanza FaltaApiKey) -> stderr y devuelve 3.
        - si el modelo falla (ModeloInalcanzable) -> stderr y devuelve 4.
        - en éxito -> imprime la respuesta en stdout y devuelve 0.
        `preguntar` está inyectado (default: preguntar_a_claude) para poder testear main.
    """
    raise NotImplementedError("Implementa esta función a mano, sin IA.")


if __name__ == "__main__":
    # Uso real:  export ANTHROPIC_API_KEY="sk-ant-..."  &&  python solucion.py "tu pregunta"
    raise SystemExit(main(sys.argv[1:], os.environ))
