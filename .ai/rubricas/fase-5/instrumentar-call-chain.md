---
ejercicio_id: fase-5/instrumentar-call-chain
fase: fase-5
sub_unidad: "5.10"
version: 1
---

# Rúbrica — Instrumenta el call-chain: trazas + correlation ID

> Rúbrica **analítica** atada a los `objetivos` del contrato. El test (`test_observabilidad.py`) da la señal objetiva de la estructura de spans; **la comprensión** (por qué se anidan, qué responde cada pilar, por qué los atributos del LLM importan) es lo que separa `competente` de `excelente` y se mide pidiendo al alumno que lo explique. El logging y la ausencia de secretos se verifican leyendo el código.

## Objetivos evaluados

- O1: Instrumentar el call-chain con spans de OpenTelemetry **anidados** que reflejen la estructura de la petición.
- O2: Propagar un `correlation_id` (contextvars) y emitir **structured logging** JSON que lo lleve en cada evento.
- O3: Adjuntar al span del LLM atributos de **tokens y costo** por paso (puente a los evals/costo de la Fase 6).

## Criterios y niveles

### C1 — Corrección de las trazas (¿se forma el árbol?) · mapea: O1, O3
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `test_observabilidad.py` falla: faltan spans, o los tres son raíces (sin anidar), o faltan los atributos `gen_ai.*`. |
| **en-progreso** | Pasa parcial: crea los spans pero alguno no queda anidado, o pone el `cost_usd` como int, o le falta un atributo del LLM. |
| **competente** | Test verde: 3 spans, los dos hijos colgando de `responder`, `correlation_id` en la raíz, `gen_ai.usage.{input_tokens,output_tokens,cost_usd}` con el tipo correcto. |
| **excelente** | Lo anterior + atributos extra con sentido (`db.system`, `gen_ai.request.model`), y articula que cada traza será un caso de dataset de evals y la base del budget de costo en la Fase 6. |

### C2 — Structured logging + correlation ID · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sigue usando `print()` o no hay logs; o el log no lleva el `correlation_id`. |
| **en-progreso** | Loguea con `structlog` pero con f-string (no consultable), o pasa el `correlation_id` a mano a cada función en vez de usar `contextvars`. |
| **competente** | `log.info("evento", campo=valor)` con `event` estable; `bind_contextvars` ata el `correlation_id` y aparece en cada log JSON. |
| **excelente** | Además limpia el contexto (`clear_contextvars`), o menciona/usa el `trace_id` como correlation ID para unir logs ⇄ trazas. |

### C3 — Seguridad (no filtrar secretos/PII) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Loguea un header de auth, un token, o vuelca la pregunta cruda "por si acaso" sin pensar en PII. |
| **en-progreso** | No filtra explícitamente, pero tampoco loguea nada sensible (suerte, no criterio). |
| **competente** | Logues con campos acotados; no aparece ningún secreto; nombra que un header de auth jamás se loguea. |
| **excelente** | Conecta con OWASP A09 (Security Logging Failures) y razona qué redactaría de un prompt real antes de emitirlo. |

### C4 — Comprensión demostrada (el "explícalo" calza con el código) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No puede explicar por qué los hijos se anidan; cree que pasó el padre a mano. |
| **en-progreso** | Explica el anidamiento pero confunde traza con log (cree que dan lo mismo). |
| **competente** | Explica que `start_as_current_span` activa el span actual y por eso los hijos cuelgan solos; distingue qué responde cada pilar. |
| **excelente** | Predice qué pasaría con `start_span` (sin activar) vs `start_as_current_span`, y por qué `BatchSpanProcessor` y no `Simple` en producción. |

## Errores típicos a marcar

- Tres spans como raíces (usar `start_span` sin activarlos, o cerrarlos antes de llamar al hijo) → no se forma el árbol; es el error conceptual central.
- `correlation_id` puesto solo como atributo del span pero **no** propagado a los logs (o al revés).
- `gen_ai.usage.cost_usd` como int → un costo lleva decimales; revela que copió para pasar el assert.
- Pasar el `correlation_id` como parámetro a cada función en vez de `contextvars` → no escala, se olvida.
- Log con f-string (`log.info(f"...")`) → vuelve el log no consultable; deshace el objetivo.
- (seguridad) loguear header de auth / token / PII.
- (transversal) cambiar la lógica de las funciones al instrumentar (el test de comportamiento lo atrapa).

## Señales de dependencia-IA

- Instrumentación perfecta pero no sabe explicar por qué los hijos se anidan sin pasar el padre.
- Usa términos que el código no implementa y no puede defender (sampling, baggage, tail-based, span links).
- "Entiendo las trazas" pero al pedir "¿qué responde una traza que mil logs no?" no puede contestar.
- Atributos `gen_ai.*` con nombres exactos del estándar pero sin poder decir para qué sirven en la Fase 6.

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Corre `uv run pytest` y atiende el primer assert que falla. Si te dice que un hijo no cuelga de `responder`, pregúntate: cuando abriste su span, ¿cuál era el span 'actual'?"
- **Pregunta socrática (nivel 2):** "No pasaste ningún 'padre' a `buscar_contexto` y aun así quedó anidado (o debería). ¿Qué hizo `start_as_current_span` además de crear el span? / Tienes 50 peticiones a la vez intercalando logs en stdout: ¿cómo reconstruyes la secuencia de UNA sola?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "`start_as_current_span` activa el span como el actual del contexto; por eso el hijo cuelga solo —no pases el padre. El `correlation_id` se ata una vez con `bind_contextvars` y el processor `merge_contextvars` lo inyecta en cada log. El `cost_usd` es float. Revisa las secciones 4.3 y 4.4 de la lección."

## Conexión con el proyecto / capstone

- Es el entregable de **observabilidad instrumentada** del DoD del Capstone F5 en miniatura: structured logs + correlation IDs + trazas. Lo que armas aquí se copia al servicio con usuarios reales del capstone, y la traza del call-chain con tokens/costo es exactamente el hilo que la Fase 6 explota para evals y budget de costo.
