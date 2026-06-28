---
ejercicio_id: fase-7/saga-pago-durable
fase: fase-7
sub_unidad: "7.3"
version: 1
---

# Rúbrica — Mini-proyecto: saga de checkout durable

> Rúbrica **analítica** para un ejercicio de **código**. Los tests dan el piso (verde/rojo), pero la
> rúbrica mira *cómo* se llegó al verde: ¿respeta el determinismo? ¿la saga compensa de verdad o el
> test pasa por accidente? El corrector evalúa el código contra los objetivos, no solo el exit code.

## Objetivos evaluados

- **O1** — Workflow durable con frontera workflow/activity correcta (cero I/O en el workflow) + RetryPolicy.
- **O2** — Saga: compensa el inventario al fallar el cobro y deja el sistema consistente antes de propagar.
- **O3** — Espera durable (`workflow.sleep`) y verificación con el time-skipping environment.

## Criterios y niveles

### C1 — Corrección: ¿hace lo que el objetivo pide? · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Tests en rojo, o `run` sin implementar; o el "workflow" hace el trabajo sin activities. |
| **en-progreso** | Happy path pasa, pero la saga no compensa (el test de tarjeta rechazada falla) o no propaga el error. |
| **competente** | Ambos tests verdes: orden reservar→cobrar→confirmar; al fallar el cobro libera inventario, no confirma envío, y el workflow falla. |
| **excelente** | Además agregó un test propio significativo (idempotencia por `workflow_id`, o reintento de fallo transitorio) y lo dejó verde. |

### C2 — Determinismo y frontera workflow/activity · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Hay `requests`/`datetime.now()`/`random`/`time.sleep` **dentro** del workflow. |
| **en-progreso** | Sin I/O crudo, pero usa `asyncio.sleep`/`time.sleep` en vez de `workflow.sleep`, o mete lógica de negocio en el workflow que debería ser activity. |
| **competente** | El workflow solo orquesta; toda interacción con el mundo pasa por `execute_activity`; la espera es `workflow.sleep`. |
| **excelente** | Articula (en comentario o write-up) por qué cada activity debe ser idempotente dado el at-least-once, y por qué el cobro no puede ir inline. |

### C3 — Calidad de ingeniería (RetryPolicy, manejo de errores, tests) · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin `retry_policy`; o atrapa el error y lo silencia (no propaga) dejando un workflow "exitoso" con estado roto. |
| **en-progreso** | RetryPolicy presente pero el `except` es demasiado amplio/confuso, o el test propio es trivial (no asegura nada). |
| **competente** | RetryPolicy pasada a las activities; `try/except` que compensa y re-lanza; test propio con una aserción real. |
| **excelente** | Distingue error de negocio (non_retryable, no se reintenta) de transitorio (se reintenta); el test propio lo demuestra. |

## Errores típicos a marcar

- **`time.sleep`/`asyncio.sleep` en el workflow** en vez de `workflow.sleep` → rompe la espera durable.
- **`requests`/HTTP/DB dentro del `run`** "porque es una línea" → la falla #1; va en una activity.
- **Compensar DESPUÉS del `raise`** (código muerto) o **no propagar** el error tras compensar (el
  workflow "termina bien" con un cobro a medias).
- **Saga al revés**: liberar inventario que no se reservó, o confirmar envío tras un cobro fallido.
- **No pasar `retry_policy`** → un timeout transitorio mata el workflow sin reintentar.
- **Editar los tests o `actividades.py`** para forzar el verde, en vez de arreglar el workflow.
- (transversales) Activity no idempotente; ignorar que at-least-once implica posible doble ejecución.

## Señales de dependencia-IA

> Describir sin acusar; proponer verificación.

- `run` impecable y idiomático pero el alumno **no sabe explicar** por qué el `sleep` no bloquea un
  proceso, o por qué la compensación va antes del `raise`.
- Uso de APIs avanzadas no vistas en la lección (señales, child workflows, `wait_condition`) sin
  motivo y sin poder justificarlas.
- Un test propio "decorativo" que no aserta nada del comportamiento (p. ej. `assert True`).
- **Verificación sugerida:** pedir que, sin ejecutar, prediga el orden de `llamadas` si la activity
  `cobrar_pago` fallara con un error **transitorio** (no non_retryable) en los 2 primeros intentos y
  acertara al tercero. Si entendió la RetryPolicy + la saga, lo resuelve.

## Feedback sugerido (graduado)

> Nunca pegar el `run` completo de la solución antes de que el alumno cierre su intento.

- **Pista (nivel 1):** "Tu happy path pasa pero el de tarjeta rechazada no. Mira qué ocurre con el
  inventario cuando el cobro lanza: ¿hay algún `liberar_inventario` en tu camino de error?"
- **Pregunta socrática (nivel 2):** "Cuando `execute_activity(cobrar_pago)` lanza, ¿qué debe pasar
  *antes* de que el workflow termine para que el mundo quede consistente? ¿Dónde, exactamente,
  colocas ese paso respecto al `raise`?"
- **Dirección concreta (nivel 3, solo tras intento real):** "El patrón es: `try:` cobrar; `except
  Exception:` → `await execute_activity(liberar_inventario, reserva_id, ...)` y luego `raise`. La
  compensación va **dentro** del except y **antes** del raise; el raise hace fallar el workflow con el
  mundo ya limpio. No silencies la excepción."

## Conexión con el proyecto / capstone

Este workflow es el molde directo del [capstone de la fase](../../../src/content/docs/fase-7-automatizacion/proyecto):
el agent loop será un workflow, cada llamada al LLM/acción externa una activity, el HITL un
`wait_condition` sobre una señal, y la saga el modo de dejar el mundo consistente cuando una acción
ejecutada falla. "Durable" es un requisito explícito del Definition of Done del capstone.
