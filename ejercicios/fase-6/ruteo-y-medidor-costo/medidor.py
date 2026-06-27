"""Medidor de costo en vivo + router de modelos — Primero-Sin-IA.

Implementa las tres funciones a mano, sin IA. NO cambies sus firmas: los tests de
`test_medidor.py` dependen de ellas. NO hardcodees precios reales dentro de las
funciones — el pricing se INYECTA como parámetro, así tu lógica no depende de la red
ni de precios que cambian cada par de meses.

Recordatorio de las tres tarifas de input (multiplicador sobre el precio de input):
    input_tokens (fresco)          -> 1.00x
    cache_read_input_tokens        -> 0.10x   (servido del cache, baratísimo)
    cache_creation_input_tokens    -> 1.25x   (escrito al cache, premium de escritura)
y el output a su propio precio.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Usage:
    """Forma mínima del objeto `usage` que devuelve un provider de LLM.

    Los campos por defecto en 0 dejan escribir tests cortos: una request sin cache
    solo setea input_tokens y output_tokens.
    """
    input_tokens: int = 0
    cache_read_input_tokens: int = 0
    cache_creation_input_tokens: int = 0
    output_tokens: int = 0


@dataclass
class Request:
    """Una request del tráfico mensual: su dificultad estimada y su usage real."""
    dificultad: float
    usage: Usage = field(default_factory=Usage)


def costo_usd(usage: Usage, precio_in: float, precio_out: float) -> float:
    """Costo en USD de UNA llamada.

    Suma las CUATRO componentes por separado:
      input fresco  -> (input_tokens / 1e6) * precio_in * 1.00
      cache read    -> (cache_read   / 1e6) * precio_in * 0.10
      cache write   -> (cache_write  / 1e6) * precio_in * 1.25
      output        -> (output       / 1e6) * precio_out

    `precio_in` / `precio_out` son USD por MILLÓN de tokens.
    """
    raise NotImplementedError("implementa costo_usd")


def rutear_modelo(dificultad: float, escalones: list[tuple[float, str]]) -> str:
    """Devuelve el NOMBRE del modelo más barato cuyo techo cubre la dificultad.

    `escalones` va de menor a mayor capacidad, p. ej.:
        [(0.3, "haiku"), (0.7, "sonnet"), (1.0, "opus")]
    Devuelve el PRIMER modelo cuyo techo >= dificultad (el borde exacto entra).
    Si ninguno cubre (dificultad fuera de rango), devuelve el último (más capaz).
    Lanza ValueError si `escalones` está vacío.
    """
    raise NotImplementedError("implementa rutear_modelo")


def costo_mensual(
    trafico: list[Request],
    escalones: list[tuple[float, str]],
    precios: dict,
) -> dict:
    """Costo mensual sobre una mezcla de tráfico.

    Por cada request: rutea con `rutear_modelo`, busca su precio en `precios`,
    y suma su `costo_usd`. REUSA las dos funciones de arriba (no dupliques la lógica).

    `precios`: {modelo: {"in": $/1M, "out": $/1M}, ...}
    Devuelve: {"total": float, "por_modelo": {modelo: float_acumulado, ...}}
    """
    raise NotImplementedError("implementa costo_mensual")


if __name__ == "__main__":
    # Prueba rápida manual (Predict–Run): ¿qué crees que imprime ANTES de correrlo?
    u = Usage(input_tokens=2_000, cache_read_input_tokens=10_000, output_tokens=500)
    print(costo_usd(u, 5.0, 25.0))
