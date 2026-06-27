"""Reintentos con backoff exponencial + jitter.

Completa `reintentar_con_backoff`. El reloj (`dormir`) y el jitter (`aleatorio`) se
INYECTAN como parámetros: por eso los tests son deterministas y NO necesitan red,
ni dormir de verdad, ni ningún tiempo real.

Idea del patrón:
  - Una `operacion()` puede fallar de forma TRANSITORIA (rate limit, 5xx) -> reintentar.
  - O fallar de forma DEFINITIVA (request inválido, key mala) -> NO reintentar, propagar.
  - Entre reintentos esperas cada vez más (backoff exponencial), con un componente
    aleatorio (jitter) para no sincronizarte con otros clientes (thundering herd).
  - Si el servidor dijo "vuelve en N segundos" (Retry-After), ese número gana.
"""
from __future__ import annotations

from typing import Callable


class ErrorReintentable(Exception):
    """Error transitorio: hay que reintentar.

    retry_after: float | None -> segundos sugeridos por el servidor (header Retry-After).
                 Si no es None, esa espera EXACTA gana sobre el backoff calculado.
    """

    def __init__(self, mensaje: str = "", retry_after: float | None = None):
        super().__init__(mensaje)
        self.retry_after = retry_after


def reintentar_con_backoff(
    operacion: Callable[[], object],
    *,
    max_intentos: int = 5,
    base: float = 1.0,
    tope: float = 60.0,
    dormir: Callable[[float], None],
    aleatorio: Callable[[float], float],
) -> object:
    """Ejecuta `operacion` con reintentos.

    operacion: callable de 0 args. Devuelve un resultado, o lanza:
        - ErrorReintentable -> reintentar (respetando .retry_after si no es None).
        - cualquier OTRA excepción -> NO reintentar; se propaga de inmediato.
    max_intentos: número TOTAL de intentos, incluido el primero (>= 1).
    base, tope: en el intento i (0-indexado) que falla y NO es el último, la espera base
        es min(tope, base * 2 ** i); se le suma el jitter. EXCEPCIÓN: si el error trae
        retry_after, la espera es ESE valor exacto (sin jitter, sin tope).
    dormir: callable[[float], None] inyectado -> en tests, registra la espera.
    aleatorio: callable[[float], float] inyectado -> recibe la espera base y devuelve el
        JITTER a sumar. En producción: lambda b: random.uniform(0, b).

    Devuelve el resultado de `operacion` en el primer éxito.
    Si se agotan los intentos sin éxito, RE-LANZA la última ErrorReintentable.
    """
    raise NotImplementedError("implementa reintentar_con_backoff")
