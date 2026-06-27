"""Punto de equilibrio de costo: servir un LLM local vs llamar a una API.

Idea central:
  - Una API se paga POR REQUEST (costo VARIABLE: sube con el uso).
  - Servir local se paga POR HORA de GPU (costo FIJO: la pagas esté ociosa o llena).

El "punto de equilibrio" es el número de requests al mes donde ambos cuestan lo mismo.
Por debajo gana la API; por encima (volumen alto y sostenido) gana local.

Completa las tres funciones. NO uses precios hardcodeados ni red: todo se INYECTA como
parámetros, así tu lógica es pura, determinista y testeable.

Pricing de la API en USD por MILLÓN de tokens (1M = 1_000_000), distinto para
entrada (in) y salida (out); casi siempre la salida cuesta más.
"""
from __future__ import annotations


def costo_api_por_request(
    tokens_in: int,
    tokens_out: int,
    precio_in: float,
    precio_out: float,
) -> float:
    """Costo en USD de UN request a la API.

    Fórmula: (tokens_in / 1e6) * precio_in + (tokens_out / 1e6) * precio_out
    (precio_in y precio_out vienen dados POR MILLÓN de tokens).
    """
    raise NotImplementedError("implementa costo_api_por_request")


def costo_api_mensual(
    requests_mes: int,
    tokens_in: int,
    tokens_out: int,
    precio_in: float,
    precio_out: float,
) -> float:
    """Costo en USD al mes de la API: requests_mes * costo por request.

    Reusa costo_api_por_request (no reimplementes la fórmula).
    """
    raise NotImplementedError("implementa costo_api_mensual")


def punto_equilibrio_requests(
    costo_local_mensual: float,
    tokens_in: int,
    tokens_out: int,
    precio_in: float,
    precio_out: float,
) -> float:
    """Número de requests/mes donde la API iguala al costo fijo de servir local.

    equilibrio = costo_local_mensual / costo_api_por_request(...)

    Por debajo de ese número la API es más barata; por encima, local.
    Lanza ValueError si el costo por request es 0 (no hay punto de equilibrio:
    una API gratis siempre gana, no hay número de requests que la empate).
    """
    raise NotImplementedError("implementa punto_equilibrio_requests")
