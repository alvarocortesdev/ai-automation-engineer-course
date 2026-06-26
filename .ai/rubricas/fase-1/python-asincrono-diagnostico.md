---
ejercicio_id: fase-1/python-asincrono-diagnostico
fase: fase-1
sub_unidad: "1.3"
version: 1
---

# Rúbrica — Diagnostica el async roto

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector la usa con
> `INSTRUCCIONES-CORRECTOR.md`. Es un ejercicio **mixto**: pesa tanto el `diagnostico.md` (comprensión)
> como `solucion.py` (corrección). No premies un fix correcto si el diagnóstico no entiende por qué.

## Objetivos evaluados

- **O1:** Diagnosticar por qué una corutina llamada sin `await` nunca ejecuta su cuerpo, y nombrar la advertencia que produce Python.
- **O2:** Explicar por qué una llamada bloqueante (`time.sleep`) dentro de una corutina congela el event loop entero, y corregirla con `asyncio.sleep` / `to_thread`.
- **O3:** Reescribir un bucle de `await` secuenciales como ejecución concurrente con `gather`/`TaskGroup`.

## Criterios y niveles

### C1 — Diagnóstico (identifica los 3 bugs con su causa) · mapea: O1, O2, O3
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `diagnostico.md` falta o solo lista síntomas ("no anda", "es lento") sin causas; identifica menos de 2 bugs. |
| **en-progreso** | Identifica los 3 bugs pero confunde causa con síntoma en alguno (p. ej. dice "el time.sleep es lento" en vez de "bloquea el event loop"), o no nombra la advertencia del `await` faltante. |
| **competente** | Los 3 bugs con causa correcta: (1) corutina sin `await` → nunca corre + `RuntimeWarning: coroutine ... was never awaited`; (2) `time.sleep` síncrono **bloquea el loop** (solo cede en un `await`); (3) `await` en serie en el `for` → secuencial. |
| **excelente** | Lo anterior + nota que (2) y (3) **se suman**: arreglar solo uno deja el programa lento; y/o que la versión sync sería igual de lenta, evidenciando que entiende el modelo, no la receta. |

### C2 — Corrección (solucion.py concurrente, en orden, no bloquea) · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `NotImplementedError` sigue; o no corre. |
| **en-progreso** | Arregla algunos bugs pero `test_es_concurrente_y_no_bloquea` falla: dejó el `time.sleep`, o mantuvo el `await` en serie. |
| **competente** | Los tres tests pasan: `asyncio.sleep` en vez de `time.sleep`, descargas lanzadas con `gather`/`TaskGroup`, resultados en orden, log efectivamente `await`-eado. |
| **excelente** | Usa `TaskGroup` (3.11+) con manejo limpio, o justifica `gather`; explica cuándo usaría `to_thread` (librería bloqueante sin alternativa async). |

### C3 — Comprensión demostrada (el write-up calza con el fix) · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | El fix funciona pero el `diagnostico.md` no explica por qué cada cambio resuelve cada bug. |
| **en-progreso** | Explica dos de tres correcciones; la del bloqueo del loop queda vaga. |
| **competente** | Cada cambio del `solucion.py` está justificado en `diagnostico.md` contra su bug. |
| **excelente** | Conecta con el modelo del event loop ("el turno solo cambia en un `await`") sin que se lo pidan. |

## Errores típicos a marcar

- Confundir "lento" (síntoma) con "bloquea el event loop" (causa) en el `time.sleep`.
- Arreglar el `await` secuencial con `gather` pero **dejar el `time.sleep`**: el loop sigue bloqueado, no hay concurrencia (el test de tiempo lo delata).
- "Corregir" el bug (1) borrando la llamada a `registrar_inicio` en vez de `await`-earla (elimina el síntoma sin entenderlo).
- Capturar el `RuntimeWarning` con un `except` en vez de arreglar la causa.
- (transversales) no correr `roto.py` para confirmar la advertencia real; entregar `solucion.py` sin `diagnostico.md`.

## Señales de dependencia-IA

- `solucion.py` impecable pero `diagnostico.md` genérico/ausente → señal de fix copiado sin comprensión; pídele que explique por qué el `time.sleep` congela a las **otras** tareas.
- Diagnóstico que usa vocabulario avanzado ("starvation del scheduler", "GIL") sin poder aterrizarlo al ejemplo concreto → impropio del nivel; verifica con una pregunta simple sobre qué imprime `roto.py`.
- Nombra la advertencia exacta pero no puede decir qué línea la causa.

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Tienes el síntoma de uno de los bugs, pero `roto.py` esconde **tres**. Relee las líneas marcadas `(1) (2) (3)`: una corutina no se espera, una espera bloquea, y un bucle espera de a uno."
- **Pregunta socrática (nivel 2):** "El event loop solo puede cambiar de tarea en cierto momento. ¿En cuál? Si una corutina hace `time.sleep(5)`, ¿le da al loop esa oportunidad?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Cambia `time.sleep` por `await asyncio.sleep`, agrega el `await` que falta en el log, y reemplaza el `for` que espera de a uno por `gather`/`TaskGroup`. Necesitas los **tres**; con dos, el test de tiempo seguirá rojo."

## Conexión con el proyecto / capstone

- El bug del `time.sleep`/`requests.get` bloqueante dentro de una corutina es exactamente el que tumba el rendimiento de un endpoint FastAPI (Fase 3) o de un agente (Fase 6/7); olerlo aquí es lo que evita el incidente allá.
