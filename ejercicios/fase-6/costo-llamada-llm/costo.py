"""Calculadora de costo de una llamada a un LLM.

Completa las dos funciones. NO uses precios hardcodeados dentro de las funciones:
el pricing se INYECTA como parámetro `precios` (un dict), así tu lógica no depende
de la red ni de precios que cambian cada par de meses.

Forma de `precios`:
    {
        "opus":   {"in": 5, "out": 25},   # USD por MILLÓN de tokens (entrada / salida)
        "sonnet": {"in": 3, "out": 15},
        "haiku":  {"in": 1, "out": 5},
    }
"""
from __future__ import annotations


def calcular_costo(
    tokens_entrada: int,
    tokens_salida: int,
    modelo: str,
    precios: dict,
) -> float:
    """Costo en USD de una llamada.

    Fórmula: (tokens_entrada / 1e6) * precio_in + (tokens_salida / 1e6) * precio_out
    donde precio_in / precio_out vienen de precios[modelo]["in"] / ["out"].

    Lanza KeyError o ValueError si `modelo` no está en `precios`
    (un modelo desconocido debe fallar fuerte, no devolver 0 en silencio).
    """
    raise NotImplementedError("implementa calcular_costo")


def modelo_mas_barato(
    tokens_entrada: int,
    tokens_salida: int,
    precios: dict,
) -> str:
    """Devuelve el NOMBRE del modelo más barato de `precios` para esa carga.

    Si hay empate, devolver cualquiera de los empatados está bien.
    Lanza ValueError si `precios` está vacío.
    """
    raise NotImplementedError("implementa modelo_mas_barato")
