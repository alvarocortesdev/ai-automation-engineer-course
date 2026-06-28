---
ejercicio_id: fase-7/capstone-automatizacion-agentica
fase: fase-7
sub_unidad: "7.P"
version: 1
---

# Rúbrica — Capstone Fase 7: Automatización end-to-end agéntica

> Rúbrica **analítica** del capstone estrella, atada a los `objetivos` del contrato y al **Definition of Done único completo (§B)**. El corrector la usa con `INSTRUCCIONES-CORRECTOR.md`. No es una nota: es un mapa de qué observar y cómo dar feedback. **El verde de los tests del plano de control es necesario, no suficiente** — un capstone que pasa esos tests pero no cumple el DoD (sin idempotencia real, sin durabilidad, sin eval gate, sin trazas) es `en-progreso`, no `competente`.

## Objetivos evaluados

- **O1:** Diseñar e implementar la automatización agéntica end-to-end de producción (input firmado → IA clasifica/extrae validado → plano de control decide → ejecución externa idempotente, orquestada con ejecución durable).
- **O2:** Instrumentar las garantías de producción y mapearlas 1:1 al Definition of Done (idempotency keys + DLQ, trazas OTel, eval gate con regresión, guardrails + least-privilege, techo de costo, HITL).
- **O3:** Comunicar como senior: demo que corre, README en inglés, write-up de trade-offs, historia de falla en producción.

## Criterios y niveles

### C1 — Arquitectura end-to-end y reparto cerebro/código · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No corre end-to-end, o el LLM ejecuta acciones directamente (sin plano de control intermedio). |
| **en-progreso** | Corre el camino feliz, pero el reparto está difuso: la salida del LLM se usa sin validar, o no hay separación clara entre propuesta y ejecución. |
| **competente** | Input → IA clasifica/extrae (salida validada) → plano de control determinista → ejecución externa. El reparto "el LLM propone, el código dispone" es nítido y defendible. |
| **excelente** | Además, el plano de control es una capa pura, testeada exhaustivamente, y el alumno articula por qué cada frontera está donde está (qué pasa si el LLM cae). |

### C2 — Plano de control: orden de chequeos y least-privilege · mapea: O1, O2 · DoD #6
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Tests del starter en rojo; o la confianza decide primero; o una acción sensible se auto-ejecuta. |
| **en-progreso** | Rutas básicas funcionan pero el orden falla en casos combinados (duplicado + schema inválido devuelve RECHAZO en vez de DUPLICADO), o el techo de costo es un parámetro muerto. |
| **competente** | Los 10 tests en verde; orden verificado (idempotencia → schema → costo → sensible → confianza); least-privilege explícito; HITL obligatorio para sensibles. |
| **excelente** | Caso propio significativo; motivos descriptivos que identifican la barrera; el `WRITE-UP` defiende el orden como defensa en profundidad. |

### C3 — Confiabilidad: idempotencia, DLQ, durabilidad · mapea: O2 · DoD #3, #6
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin idempotency key; un replay del webhook re-ejecuta la acción. Sin DLQ. |
| **en-progreso** | Idempotencia presente pero frágil (race, o key mal elegida); DLQ existe pero no se usa para poison messages; orquestación no es durable (cron + cola que pierde estado). |
| **competente** | Idempotency key por `message_id` consultada antes de ejecutar; DLQ para schema inválido; orquestación durable (Temporal) con HITL que sobrevive a un reinicio del worker. |
| **excelente** | Reconciliación demostrada; el HITL durable se prueba matando y reiniciando el worker a mitad de la espera; LLM en actividad (no en el cuerpo del workflow) con justificación de determinismo. |

### C4 — Eval gate del agente · mapea: O2 · DoD #5
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin evals, o evals que miden fluidez del texto en vez de la decisión. |
| **en-progreso** | Mide accuracy pero sin baseline versionado ni gate de regresión; no corre en CI. |
| **competente** | Golden set anotado; mide accuracy de routing/exactitud de extracción; gate que bloquea el deploy por umbral Y por regresión; corre en CI con baseline versionado. |
| **excelente** | Golden set derivado de trazas reales; distingue eval offline de monitoreo online; budget de costo/latencia como entregable. |

### C5 — Seguridad (OWASP web + LLM/Agentic) · mapea: O2 · DoD #3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Webhook sin verificar firma; salida del LLM ejecutada sin validar; tools sin restringir. |
| **en-progreso** | Verifica HMAC pero sin anti-replay; guardrail de schema presente pero confía en el contenido; falta secret/dependency scanning en CI. |
| **competente** | HMAC + anti-replay; guardrail de I/O (LLM05); least-privilege de tools y HITL (LLM06); contenido no confiable segregado como datos (LLM01); gitleaks + SCA en el pipeline. |
| **excelente** | Defense in depth articulada; un caso de prompt injection en el ticket que NO logra ejecutar acción gracias al plano de control. |

### C6 — Observabilidad · mapea: O2 · DoD #4
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Solo `print`; sin trazas ni correlation id. |
| **en-progreso** | Logs estructurados pero sin trazas, o sin correlation id propagado por el call-chain. |
| **competente** | Trazas OTel con `message_id` como correlation id; span por paso; tokens/latencia/costo por paso visibles. |
| **excelente** | Las trazas son las que cuentan la historia de falla del POST-MORTEM (se ve el fallo en la traza). |

### C7 — Comunicación: demo, README inglés, write-up, post-mortem · mapea: O3 · DoD #8, Track-0
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No corre, o README ausente/en español, o sin write-up. |
| **en-progreso** | Corre pero la demo es frágil; README incompleto; write-up sin números (eval, costo). |
| **competente** | Demo que corre (`docker compose up` + script); README en inglés claro; `WRITE-UP.md` con trade-offs + número del eval + baseline + costo/latencia; `POST-MORTEM.md` honesto. |
| **excelente** | El alumno explica la arquitectura completa en inglés en menos de 5 min sin notas; el post-mortem cuenta una reconciliación real (ni se perdió ni se duplicó nada). |

## Errores típicos a marcar

- Confianza como primer chequeo → cortocircuita idempotencia, schema, costo y la regla de acción sensible.
- Auto-ejecutar una acción sensible porque la confianza es alta (viola LLM06; la confianza no está calibrada).
- Actuar sobre una salida con schema inválido (LLM05).
- Recibir `techo_costo_usd` y no usarlo (Unbounded Consumption sin circuit-breaker).
- Meter la llamada al LLM (o `time`/`random`/HTTP) en el cuerpo del workflow Temporal → rompe el replay determinista.
- "La parte nueva es la IA, así que la idempotencia no aplica" → reembolso duplicado por reintento.
- Eval que mide fluidez en vez de tasa de decisión correcta; sin gate de regresión (solo umbral fijo).
- Webhook que verifica firma pero no anti-replay; o no verifica nada.
- README en español o ausente (DoD #8 exige inglés); commits sin Conventional Commits (DoD #9).
- (transversales) persigue coverage% en vez de aserciones; agente con exceso de tools/permisos; falta un trade-off defendible en el write-up.

## Señales de dependencia-IA

- Sistema sofisticado (Temporal + OTel + eval gate) pero el alumno no puede explicar por qué el LLM va en una actividad y no en el workflow, ni qué pasa con un duplicado que además es sensible.
- Write-up con el vocabulario exacto de la lección (LLM05/LLM06, "el LLM propone, el código dispone") sin poder dar un ejemplo propio de salida válida pero incorrecta, o sin un trade-off defendible que él haya medido.
- Post-mortem genérico/inventado: no hay traza que respalde la falla, ni reconciliación concreta (señal de que no hubo usuarios reales ni se rompió nada de verdad).
- **Verificación sugerida:** pedir que prediga, sin ejecutar, la ruta de un duplicado con schema inválido y acción sensible (debe decir `DUPLICADO`); y que explique en inglés, en 60 segundos, por qué el HITL sobrevive a un reinicio. Si entendió, responde al instante.

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Corre mentalmente un caso que dispare DOS barreras a la vez en tu plano de control (duplicado + acción sensible). ¿Cuál gana en tu código? ¿Cuál debería ganar? Y por separado: si matas el worker mientras esperas la aprobación HITL, ¿tu sistema retoma o pierde el estado?"
- **Pregunta socrática (nivel 2):** "Si el modelo reporta 0.99 de confianza en un reembolso de 10 millones, ¿qué te garantiza ese número? ¿De dónde sale realmente la garantía de que la acción es correcta? ¿Y por qué la llamada al LLM no puede vivir en el cuerpo del workflow?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Ordena los chequeos como cadena de `if` con `return` temprano: idempotencia → schema → costo → sensible → confianza; la confianza es el ÚLTIMO y solo para no-sensibles. Mueve toda I/O (LLM, HTTP, DB) a actividades; el cuerpo del workflow solo orquesta y llama funciones puras. El HITL es `workflow.wait_condition` con timeout (patrón de 7.3). El eval gate va en CI con un baseline versionado, midiendo accuracy de routing, no fluidez."

## Conexión con el proyecto / capstone

- **Este ES el capstone estrella de la fase y del portafolio (Track-0).** Cierra el constructive alignment de toda la Fase 7: 7.2 (idempotencia/DLQ), 7.3 (durabilidad/HITL), 7.7 (plano de control + eval gate), 7.5d (data contracts), más Fase 6 (estructura/agentes/evals/seguridad/costo) y Fase 5 (observabilidad/CI). El `POST-MORTEM.md` alimenta directamente la historia de falla en producción de Track-0 (T0.4) y la grabación en inglés alimenta los mock interviews (T0.3).
