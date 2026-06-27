"""Ejercicio 6.1 — Tokenización.

Completa `contar_tokens`. La función `ver_tokens` ya está implementada para que
puedas EXPLORAR cómo el tokenizer parte el texto (úsala en tu verificación).

Requisitos:
    pip install tiktoken     # o:  uv add tiktoken

Nota: la primera vez que se usa una codificación, tiktoken descarga su
vocabulario desde internet y lo cachea localmente. Después funciona offline.

Codificaciones útiles (nombre -> familia de modelos que la usa):
    "o200k_base"  -> GPT-4o y modelos OpenAI modernos  (usa esta por defecto)
    "cl100k_base" -> GPT-4 / GPT-3.5 clásicos

Recuerda: tiktoken es el tokenizer de OpenAI. Otras familias (Claude, Gemini,
open-source) tokenizan distinto. Para conteos exactos de Claude se usa la API de
token counting de Anthropic, no tiktoken. Aquí lo usamos para VER el concepto.
"""

from __future__ import annotations

import tiktoken


def contar_tokens(texto: str, codificacion: str = "o200k_base") -> int:
    """Devuelve cuántos tokens produce `texto` con la codificación dada.

    Pasos (piénsalos antes de mirar `ver_tokens`):
      1. Obtén el objeto de codificación a partir de su nombre.
      2. Codifica el texto en una lista de IDs de token.
      3. Devuelve cuántos IDs hay.

    El string vacío ("") debe devolver 0.
    """
    # TODO: implementa la función. Es de 1 a 2 líneas.
    raise NotImplementedError("Completa contar_tokens")


def ver_tokens(texto: str, codificacion: str = "o200k_base") -> list[str]:
    """Devuelve la lista de tokens como texto, para que VEAS cómo se parte.

    Ya implementada — úsala para explorar y construir tu `verificacion.md`.

    Ejemplo:
        >>> ver_tokens("El gato")
        ['El', ' gato']   # los valores reales dependen de la codificación
    """
    enc = tiktoken.get_encoding(codificacion)
    return [enc.decode([token_id]) for token_id in enc.encode(texto)]


if __name__ == "__main__":
    # Pequeño explorador manual. Ejecuta:  python tokenizador.py
    cadenas = [
        "hello world",
        "antidisestablishmentarianism",
        "  ",
        "def suma(a, b): return a + b",
        "El murciélago ñoño comió crème brûlée",
        "🎂🎂🎂",
    ]
    for s in cadenas:
        try:
            n = contar_tokens(s)
        except NotImplementedError:
            n = "?"
        print(f"{n!s:>3} tokens | {s!r}")
