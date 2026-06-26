---
ejercicio_id: fase-3/worker-reintentos-dlq
fase: fase-3
sub_unidad: "3.16"
version: 1
---

# Rúbrica — Implementa un worker con reintentos y DLQ (Python puro)

> Rúbrica **analítica** de un ejercicio de **código**. El test (`test_worker.py`) es el piso objetivo: o pasa en verde o no. Pero pasar el test no es suficiente — el corrector evalúa además si el alumno **entiende** el patrón (ciclo de vida, at-least-once, dedup) y si su código lo expresa con claridad. El corrector NUNCA pega la solución de referencia; guía con pistas graduadas y, si no hay intento real, pide que primero lo intente.

## Objetivos evaluados
- **O1** — Implementar la semántica de reintentos con tope: un job que falla se reencola hasta `max_attempts`, sin loop infinito.
- **O2** — Enrutar a la DLQ los jobs que agotan intentos (poison messages) y a `done` los que tienen éxito.
- **O3** — Deduplicar por `job.id` bajo entrega at-least-once (el handler corre una sola vez por id ya completado), entendiendo que es el equivalente de la idempotencia.

## Criterios y niveles

### C1 — Corrección (¿hace lo que el objetivo pide?) · mapea: O1, O2, O3
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `pytest` en rojo: o no reintenta, o reintenta sin tope (loop infinito / cuelga), o no separa `done` de `dlq`, o no deduplica. |
| **en-progreso** | Pasa algunos tests pero falla otros: típicamente reintentos OK pero **sin dedup** (el test at-least-once falla), o el conteo de llamadas no da exacto (incrementa `attempts` en el momento equivocado), o manda a DLQ con un intento de más/de menos. |
| **competente** | `pytest` en **verde** (los 5 tests): éxito al primer intento, flaky que se recupera dentro del tope (handler llamado exactamente `max_attempts`), siempre-falla → DLQ con `attempts == max_attempts`, dedup por id (handler una sola vez), mezcla done/dlq. |
| **excelente** | Además el código es **legible y honesto**: FIFO explícito (deque), la condición de DLQ es clara (`attempts >= max_attempts`), el set de ids hechos está bien nombrado, y el alumno explica en su `pista`/comentario por qué la dedup es la idempotencia bajo at-least-once. |

### C2 — Calidad de ingeniería (tests propios, claridad, sin trampas) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No agregó ningún test propio; o "pasó" el test hardcodeando resultados / detectando el id del test en vez de implementar la lógica. |
| **en-progreso** | Agregó un test trivial que no aporta (re-testea lo mismo), o el código funciona pero es enredado (banderas, estados redundantes) y difícil de defender. |
| **competente** | Agregó al menos un test propio que cubre un caso nuevo (p. ej. `max_attempts=1` → un solo intento, o varios ids mezclados con duplicados), y el código separa con claridad las cuatro transiciones (éxito, reintento, DLQ, skip por dedup). |
| **excelente** | El test propio cubre un borde real (p. ej. `max_attempts=1`, o un duplicado de un id que va a DLQ) y el alumno puede explicar, sin notas, cada rama del `while`. |

## Errores típicos a marcar
- **Reintentar sin tope** → loop infinito (el test de siempre-falla cuelga). Síntoma de no haber pensado el poison message.
- **Incrementar `attempts` en el momento equivocado**: si lo incrementas antes de llamar al handler o comparas mal, el conteo de llamadas y la entrada a DLQ se desfasan (handler llamado 2 o 4 veces en vez de 3).
- **No deduplicar** (ignorar el caso at-least-once): el test del id duplicado falla; el handler corre dos veces. Es el error conceptual central — bajo at-least-once, sin dedup hay doble efecto.
- **Deduplicar contra la cola en vez de contra `done`**: saltar un id que aún no se completó (p. ej. que está en reintento) rompería la semántica; la dedup correcta es "ya quedó hecho".
- **Mutar la lista de entrada** o usarla como cola sin copiar, con efectos raros.
- **Mezclar la responsabilidad del handler con la del dispatcher**: el handler solo hace el trabajo (y lanza si falla); la política de reintentos/DLQ/dedup es del dispatcher.
- (transversales) "pasó el test" como única evidencia sin poder explicar la reentrega tras un worker que muere antes del ack (señal de copiar sin entender); perseguir que pase sin entender por qué `attempts == max_attempts` en la DLQ.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Solución que pasa pero con estructuras innecesariamente sofisticadas para el nivel (un mini-framework, async, locks) que el alumno no puede justificar.
- Comentarios genéricos que no calzan con el código (habla de "broker" o "Redis" cuando el ejercicio es in-memory puro).
- **Verificación sugerida:** pedir que prediga, **sin ejecutar**, cuántas veces se llama el handler para un job con `max_attempts=4` que falla siempre, y dónde termina. Quien entendió dice "4 veces, termina en DLQ"; quien copió duda o da el número del test que vio.

## Feedback sugerido (graduado)
> **Nunca pegar la solución de referencia.**
- **Pista (nivel 1):** "¿Qué estructura te da FIFO de forma natural y te deja reencolar al final? ¿Y dónde guardas qué ids ya completaste para no repetirlos?"
- **Pregunta socrática (nivel 2):** "Cuando un job falla, ¿en qué orden haces tres cosas: incrementar attempts, comparar con max_attempts, y decidir reencolar o DLQ? Traza a mano un job que falla siempre con max_attempts=3 y cuenta las llamadas."
- **Dirección concreta (nivel 3, solo tras intento real):** "Tu bucle necesita, por cada job que sacas: (1) si su id ya está en el set de hechos, saltarlo; (2) llamar al handler; (3) en éxito, agregar el id a hechos y a done; (4) en excepción, `attempts += 1` y, si `attempts < max_attempts` reencolar, si no, a la DLQ. Revisa cuál de los cuatro te falta."

## Conexión con el proyecto / capstone
- Este dispatcher es la **maqueta mental** de Celery/BullMQ: cuando en el capstone (o en la Fase 7) configures `max_retries`/`attempts`, `backoff` y una DLQ, sabrás exactamente qué máquina de estados estás activando y por qué los handlers deben ser idempotentes. El patrón reintentos + DLQ + dedup es la columna de la confiabilidad de integración del capstone estrella de F7.
