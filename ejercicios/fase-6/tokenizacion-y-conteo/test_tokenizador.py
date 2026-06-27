"""Tests para contar_tokens.

Estrategia: en vez de fijar números mágicos (que cambian entre versiones del
tokenizer), comparamos contra lo que tiktoken mismo produce. Así el test verifica
que TU función cuenta bien, sin amarrarse a un conteo exacto.

Nota: la primera ejecución descarga el vocabulario (necesita internet una vez).
"""

import tiktoken

from tokenizador import contar_tokens


def _referencia(texto: str, codificacion: str = "o200k_base") -> int:
    """Conteo de referencia, calculado directamente con tiktoken."""
    return len(tiktoken.get_encoding(codificacion).encode(texto))


def test_vacio_es_cero():
    assert contar_tokens("") == 0


def test_coincide_con_tiktoken_o200k():
    for s in ["hello world", "antidisestablishmentarianism", "  ", "🎂🎂🎂"]:
        assert contar_tokens(s) == _referencia(s), f"falla en {s!r}"


def test_coincide_con_tiktoken_codigo():
    s = "def suma(a, b): return a + b"
    assert contar_tokens(s) == _referencia(s)


def test_funciona_con_otra_codificacion():
    s = "El murciélago ñoño comió crème brûlée"
    assert contar_tokens(s, "cl100k_base") == _referencia(s, "cl100k_base")


def test_espanol_con_acentos_cuesta_mas_que_ingles_corto():
    # No es un número exacto: es la INTUICIÓN que el ejercicio quiere romper.
    # El español acentuado cuesta más tokens que un inglés corto equivalente.
    assert contar_tokens("El murciélago ñoño") > contar_tokens("the bat")
