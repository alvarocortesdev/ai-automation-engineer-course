"""Reintentos con backoff exponencial + jitter, A MANO (sin tenacity).

Implementa `reintentar` SIN usar ninguna librería de retry: la gracia del
ejercicio es entender la mecánica (qué se reintenta, cuánto se espera, cuándo
se rinde). En producción usarías tenacity; aquí lo haces tú una vez.

Corre el test:
    uv run pytest        # o: pytest

Anota en bitacora.md por qué el jitter evita la "retry storm" y por qué NO se
reintentan los errores permanentes (4xx).
"""

import random
import time
from typing import Callable, TypeVar

T = TypeVar("T")


class ErrorTransitorio(Exception):
    """Falla pasajera que probablemente se resuelva al reintentar.

    (Equivalente conceptual a un timeout, un 503 o un rechazo de conexión.)
    """


class ErrorPermanente(Exception):
    """Falla que NO se arregla reintentando (equivalente a un 400/401/422)."""


def reintentar(
    fn: Callable[[], T],
    *,
    max_intentos: int = 5,
    base: float = 0.5,
    tope: float = 10.0,
    transitorias: tuple[type[Exception], ...] = (ErrorTransitorio,),
    dormir: Callable[[float], None] = time.sleep,
    aleatorio: Callable[[], float] = random.random,
) -> T:
    """Llama a `fn` reintentando SOLO las excepciones `transitorias`.

    Reglas (impleméntalas):
      - Si `fn()` devuelve, devolver su valor.
      - Si `fn()` lanza algo que NO está en `transitorias`, propagarlo de
        inmediato (sin reintentar, sin dormir).
      - Si lanza una transitoria, reintentar hasta `max_intentos` intentos
        TOTALES. Antes de cada reintento, esperar con backoff + jitter:
            espera del intento n (n empieza en 0) = aleatorio() * min(tope, base * 2**n)
        y llamar a `dormir(espera)`.
      - Si se agotan los intentos, RELANZAR la última excepción transitoria.

    `dormir` y `aleatorio` se inyectan para poder testear sin esperar de verdad
    y de forma determinista. No cambies la firma: los tests dependen de ella.
    """
    raise NotImplementedError("implementa el reintento con backoff + jitter")


if __name__ == "__main__":
    # Prueba manual rápida (Predict-Run): ¿qué crees que pasa ANTES de correrlo?
    intentos = {"n": 0}

    def flaky() -> str:
        intentos["n"] += 1
        if intentos["n"] < 3:
            raise ErrorTransitorio("la red parpadeó")
        return "ok"

    print(reintentar(flaky, dormir=lambda s: None))  # esperado: "ok" en el 3er intento
