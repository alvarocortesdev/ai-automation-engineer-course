"""Circuit breaker: la máquina de estados, A MANO.

Implementa la clase `CircuitBreaker` con sus tres estados (closed / open /
half-open). El reloj se INYECTA (default time.monotonic) para que los tests
puedan avanzar el tiempo sin esperar de verdad.

Corre el test:
    uv run pytest        # o: pytest

Anota en bitacora.md la diferencia entre el breaker y un retry, y para qué
sirve el estado half-open.
"""

import time
from typing import Callable, TypeVar

T = TypeVar("T")


class CircuitoAbierto(Exception):
    """Se lanza cuando el circuito está abierto: rechaza la llamada sin intentarla."""


class CircuitBreaker:
    """Cortacircuitos con estados closed / open / half-open.

    Implementa (no cambies las firmas: los tests dependen de ellas):

      - __init__(self, *, umbral_fallos=3, espera_apertura=30.0, reloj=time.monotonic)
      - propiedad `estado` -> "closed" | "open" | "half-open"
      - llamar(self, fn) -> el resultado de fn(), o lanza CircuitoAbierto

    Reglas:
      closed:    ejecuta fn(); un éxito reinicia el contador de fallos; al
                 alcanzar `umbral_fallos` fallos CONSECUTIVOS pasa a open y
                 marca el instante de apertura.
      open:      mientras no pase `espera_apertura`, `llamar` lanza
                 CircuitoAbierto SIN invocar fn.
      half-open: pasada la ventana, se permite UNA llamada de prueba. Si tiene
                 éxito -> closed; si falla -> open con el temporizador reiniciado.

    Pista para `estado`: si el estado interno es "open" pero ya pasó la ventana
    de espera, repórtalo como "half-open" (así es observable desde fuera y
    `llamar` puede usar la misma condición para permitir la prueba).
    """

    def __init__(
        self,
        *,
        umbral_fallos: int = 3,
        espera_apertura: float = 30.0,
        reloj: Callable[[], float] = time.monotonic,
    ) -> None:
        raise NotImplementedError("inicializa el estado del breaker")

    @property
    def estado(self) -> str:
        raise NotImplementedError("reporta closed / open / half-open")

    def llamar(self, fn: Callable[[], T]) -> T:
        raise NotImplementedError("aplica la máquina de estados alrededor de fn()")
