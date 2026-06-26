---
ejercicio_id: fase-3/worker-reintentos-dlq
fase: fase-3
sub_unidad: "3.16"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Pasar el test es el piso; el corrector evalúa además si el alumno **entiende** el ciclo de vida y la idempotencia bajo at-least-once.

# Solución de referencia — Worker con reintentos y DLQ

## Implementación canónica

```python
import collections
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class Job:
    id: str
    payload: dict[str, Any] | None = None
    max_attempts: int = 3
    attempts: int = 0


def procesar_cola(
    jobs: list[Job],
    handler: Callable[[Job], None],
) -> dict[str, list]:
    cola = collections.deque(jobs)   # FIFO: encolado a la derecha, procesado por la izquierda
    done: list[str] = []
    dlq: list[Job] = []
    hechos: set[str] = set()         # ids ya completados (idempotencia bajo at-least-once)

    while cola:
        job = cola.popleft()

        # at-least-once: si este id ya quedó hecho, NO lo reprocesamos (dedup).
        if job.id in hechos:
            continue

        try:
            handler(job)
        except Exception:
            # fallo: contamos el intento y decidimos reintento o DLQ.
            job.attempts += 1
            if job.attempts < job.max_attempts:
                cola.append(job)      # reintento (al final de la cola)
            else:
                dlq.append(job)       # poison message: agotó intentos -> DLQ
        else:
            # éxito: el job queda hecho (ack). Registramos para dedup y resultado.
            hechos.add(job.id)
            done.append(job.id)

    return {"done": done, "dlq": dlq}
```

## Por qué cada decisión

- **`deque` + `popleft`/`append`** = cola FIFO real: reintentar = volver al final, no reintentar de inmediato (en una cola de verdad, eso da espacio al backoff y a otros jobs).
- **`hechos: set[str]`** es la idempotencia del ejercicio. Bajo **at-least-once**, el broker puede reentregar un job ya procesado (un worker que murió antes del ack); el set evita el **doble efecto** saltando el id ya completado. Este es el concepto central: sin esta línea, el test del id duplicado falla y, en producción, el usuario recibiría el email dos veces.
- **`attempts += 1` *después* del fallo, comparado con `< max_attempts`**: garantiza que con `max_attempts=3` el handler se llama exactamente 3 veces (intentos 1, 2, 3) y, si los tres fallan, el job va a la DLQ con `attempts == 3`. Incrementar antes de llamar al handler, o comparar con `<=`, desfasa el conteo (error típico).
- **`else` del `try`** (éxito) separado del `except` (fallo): expresa las dos transiciones del ciclo de vida sin banderas.

## Traza de validación (lo que el corrector confirma)

| Caso | max_attempts | comportamiento del handler | llamadas | resultado |
|---|---|---|---|---|
| éxito directo | 3 | nunca falla | 1 | `done` |
| flaky | 3 | falla 2, luego ok | 3 | `done` |
| siempre falla | 3 | falla siempre | 3 | `dlq` (attempts=3) |
| duplicado | 3 | nunca falla, id repetido | 1 | `done` (una vez) |
| mezcla | 3 | ok1 / bad-siempre / ok2 | 1/3/1 | done={ok1,ok2}, dlq=[bad] |

## Variantes aceptables
- Usar una **lista con índice** en vez de `deque` (mientras sea FIFO y no cuelgue).
- Llevar el set de hechos como `dict` id→resultado (sobra para el ejercicio, pero es válido).
- Nombrar `done`/`dlq` distinto, **mientras el dict devuelto tenga las claves `"done"` y `"dlq"`** que el test espera.

## Errores a marcar (resumen)
- Reintentar sin tope (loop infinito; el test de siempre-falla cuelga).
- No deduplicar (test at-least-once falla; doble efecto).
- Conteo de intentos desfasado (handler llamado 2 o 4 veces en vez de 3).
- Mezclar la lógica del handler con la del dispatcher.
- "Pasa el test" sin poder explicar por qué la dedup es la idempotencia.

## Variante de control anti-IA
Pedir que prediga **sin ejecutar**: "un job con `max_attempts=4` que falla siempre: ¿cuántas veces se llama el handler y dónde termina?". Respuesta correcta razonada: **4 llamadas, termina en la DLQ** (intentos 1–4, al cuarto `attempts==max_attempts` → DLQ). Quien copió duda o responde con el número de algún test que vio.
