"""Mini-dispatcher de cola con reintentos, DLQ e idempotencia (Python puro).

Sin broker, sin Redis, sin Celery: captura la SEMÁNTICA de una cola para que
entiendas el patrón antes de tocar una herramienta. Implementa `procesar_cola`
respetando el contrato del docstring. Corre el test:

    uv run pytest        # o simplemente:  pytest

NO uses IA para generarla: primero a mano (timebox 40-45 min). La idea es que
el ciclo de vida encolado -> en proceso -> (hecho | reintento -> DLQ) y la
deduplicación por job.id se te queden en el cuerpo, no en un copy-paste.
"""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class Job:
    """Unidad de trabajo encolada.

    - id: identificador del job (la idempotency key de este ejercicio).
    - payload: datos del trabajo (no se usan en la mecánica; ilustran que un job
      es DATOS, no código).
    - max_attempts: tope de intentos antes de mandarlo a la DLQ.
    - attempts: cuántas veces se ha INTENTADO (lo lleva el dispatcher; empieza en 0).
    """

    id: str
    payload: dict[str, Any] | None = None
    max_attempts: int = 3
    attempts: int = 0


def procesar_cola(
    jobs: list[Job],
    handler: Callable[[Job], None],
) -> dict[str, list]:
    """Procesa una cola de jobs con reintentos, DLQ e idempotencia.

    Reglas (contrato — los tests las verifican):

    1. FIFO: procesa los jobs en orden; al fallar, el job se REENCOLA al final.
    2. Ejecutar el handler:
       - éxito (no lanza excepción)  -> el job queda HECHO: agrega su id a `done`.
       - falla (lanza una excepción) -> incrementa `job.attempts`; si todavía
         quedan intentos (`attempts < max_attempts`), REENCOLA el job; si los
         agotó, va a la DLQ (no se reintenta más: es un poison message).
    3. Idempotencia / at-least-once: la cola puede traer el MISMO `job.id` más de
       una vez (entrega at-least-once). Si un id YA quedó en `done`, NO vuelvas a
       ejecutar el handler para él ni lo dupliques en `done` (deduplicación).

    Devuelve un dict:
        {
          "done": [ids de jobs completados, únicos, en orden de completado],
          "dlq":  [los Job que agotaron sus intentos],
        }
    """
    raise NotImplementedError("implementa procesar_cola según el contrato del docstring")
