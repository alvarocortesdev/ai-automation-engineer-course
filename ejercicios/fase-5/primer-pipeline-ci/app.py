"""Módulo de ejemplo del ejercicio.

NO necesitas tocar este archivo: ya está implementado y sus tests pasan.
Existe solo para que tu pipeline de CI tenga *algo real* que lintear y testear.
El ejercicio es escribir el workflow `.github/workflows/ci.yml`, no esta función.
"""


def es_palindromo(texto: str) -> bool:
    """Devuelve True si `texto` es un palíndromo, ignorando mayúsculas y espacios.

    Contrato:
        entrada: un string cualquiera (puede estar vacío).
        salida:  True si se lee igual al derecho y al revés tras normalizar
                 (minúsculas, sin espacios); el string vacío es palíndromo.
    """
    normalizado = "".join(c.lower() for c in texto if not c.isspace())
    return normalizado == normalizado[::-1]
