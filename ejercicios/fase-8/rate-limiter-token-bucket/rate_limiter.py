"""Rate limiter — token bucket (esqueleto del ejercicio 8.1).

Completa los TODO. Regla de oro de testabilidad: NO llames a time.monotonic() ni
time.time() DENTRO de la clase. El reloj se INYECTA como parámetro `ahora`, así los
tests son deterministas (mismo input -> mismo output, sin sleep, sin flakiness).
"""

from __future__ import annotations


class TokenBucket:
    """Token bucket rate limiter.

    Args:
        capacity:    número máximo de tokens que caben en el bucket.
        refill_rate: tokens que se reponen por segundo.
        ahora:       marca de tiempo inicial en segundos (p. ej. de time.monotonic()).
                     Se inyecta para poder testear sin esperar tiempo real.

    El bucket arranca LLENO (con `capacity` tokens).
    """

    def __init__(self, capacity: float, refill_rate: float, ahora: float) -> None:
        self.capacity = capacity
        self.refill_rate = refill_rate
        # TODO: inicializa los tokens (bucket lleno) y guarda la marca de tiempo
        #       de la última recarga (= ahora).
        ...

    def allow(self, ahora: float, cost: float = 1.0) -> bool:
        """¿Se permite un request de costo `cost` en el instante `ahora`?

        Pasos (en este orden):
          1. Recarga: suma los tokens generados desde la última recarga
             (tiempo transcurrido * refill_rate), SIN superar la capacidad.
             Si `ahora` no avanzó (o retrocedió), no recargues nada.
          2. Decisión: si hay al menos `cost` tokens, consúmelos y devuelve True.
             Si no, NO consumas nada y devuelve False.
        """
        # TODO: implementa la recarga y la decisión.
        raise NotImplementedError
