---
ejercicio_id: fase-6/decision-serving-stack
fase: fase-6
sub_unidad: "6.10"
version: 1
---

# Rúbrica — Decisión: stack de serving para tres escenarios

> Rúbrica **analítica** atada a los `objetivos` del contrato. Ejercicio de **diseño**: no
> hay respuesta única. El corrector evalúa la **calidad del trade-off**, no la coincidencia
> literal con la solución de referencia. El objetivo de fondo: que el alumno **derive** cada
> decisión de la restricción dominante y entienda por qué un runtime single-user no es un
> motor de serving.

## Objetivos evaluados

- **O1** — Decidir local vs API según la restricción dominante (costo, privacidad, latencia).
- **O2** — Elegir el motor por la concurrencia (single-user vs producción), nombrando KV cache y continuous batching.
- **O3** — Elegir la cuantización (GGUF vs AWQ) por dónde corre y reconocer una consideración de privacidad/seguridad.

## Criterios y niveles

### C1 — Local vs API derivado de la restricción · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Elige "lo mejor" o lo mismo para los tres sin restricción; o pone local "porque es más privado/barato" sin mirar el caso. |
| **en-progreso** | Nombra una restricción pero la elección no se deriva de ella (p. ej. startup de bajo volumen → propone local sin justificar el costo fijo). |
| **competente** | E1 local (privacidad + single-user), E2 local on-prem (privacidad legal), E3 API (volumen bajo/variable + sin ops) — cada uno derivado de su restricción. |
| **excelente** | Reconoce que en E3 la API gana **por costo** (volumen bajo) y que en E2 es la **ley** la que descarta la API (no el costo); separa los ejes con claridad. |

### C2 — Motor por concurrencia + mecanismos · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No distingue runtime single-user de motor de serving; propone Ollama para 500 usuarios. |
| **en-progreso** | Elige vLLM/TGI en E2 pero no explica por qué Ollama no sirve, o no nombra ningún mecanismo. |
| **competente** | E1 → Ollama o MLX (single-user); E2 → vLLM o TGI, nombrando **KV cache** y/o **continuous batching** y por qué habilitan alta concurrencia. |
| **excelente** | Explica el trade-off **throughput vs latencia** del batching, o por qué el KV cache (memoria de GPU) es el recurso que limita cuántos requests caben a la vez. |

### C3 — Cuantización por dónde corre · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No menciona cuantización, o la trata como "gratis"/intercambiable (GGUF en GPU de prod con vLLM). |
| **en-progreso** | Elige una pero sin ligarla a dónde corre, o sin decir qué se pierde. |
| **competente** | GGUF para E1 (Mac/CPU, llama.cpp/Ollama/MLX), AWQ para E2 (GPU + vLLM); menciona que cuantizar degrada algo de calidad. |
| **excelente** | Nota que un GGUF no lo carga vLLM (y al revés), o ubica el punto dulce (8 bits casi sin pérdida, 4 bits trade-off defendible, 2 bits degradación visible). |

### C4 — Privacidad/seguridad + comunicación (ADR-able) · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No menciona seguridad, o dice "local = privado" sin más. |
| **competente** | Cada escenario nombra una consideración concreta (datos que no salen, logs/PII, acceso al servidor) con una mitigación; se podría defender en entrevista. |
| **excelente** | Reconoce que "local habilita pero no garantiza privacidad" (faltan control de acceso, cifrado, retención de logs, KV cache en memoria); enlaza con 6.14. |

## Errores típicos a marcar

- "La mejor forma de correr un LLM es X" sin restricción → no entendió que es contextual.
- Proponer Ollama/MLX para 500 usuarios concurrentes (no escalan: single-stream).
- Proponer local en la startup de bajo volumen "porque es más barato" (ignora el costo fijo de la GPU ociosa).
- Tratar GGUF y AWQ como intercambiables, o cuantizar como si fuera gratis.
- Confundir "local" con "privado y seguro" automáticamente.
- (transversal) ningún trade-off defendible; "depende" sin comprometerse a una decisión.

## Señales de dependencia-IA

- Tres escenarios con prosa pulida e idéntica estructura retórica pero **sin** comprometerse
  a una decisión (hedging tipo "podrías usar cualquiera de los dos").
- Menciona herramientas o versiones que no salieron en la lección con detalles inventados.
- **Verificación sugerida:** pídele que defienda por qué Ollama no sirve para 500 usuarios.
  Si lo razonó, habla de single-stream vs continuous batching; si lo copió, se queda en
  "no está hecho para producción" sin el mecanismo.

## Feedback sugerido (graduado)

> Ordenadas de menos a más directas. **Nunca escribir la decisión por el alumno.**

- **Pista (nivel 1):** "Para cada escenario, ¿cuál es la **una** cosa que, si la ignoras,
  hunde el proyecto? Esa es tu restricción dominante; deja que ella elija local vs API."
- **Pregunta socrática (nivel 2):** "En el escenario 2, si usaras Ollama y llegan 500
  requests al mismo tiempo, ¿qué le pasa al usuario 500? ¿Qué hace vLLM distinto para que
  no espere su turno?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Tu elección de vLLM en E2 está
  bien, pero falta el porqué: nombra el continuous batching (GPU siempre llena → throughput
  para muchos) y el KV cache (no recomputar la atención). Y en E3, recuerda que la GPU se
  paga ociosa: a 100 usuarios variables, la API gana por costo."

## Conexión con el proyecto / capstone

- Esta decisión es **literalmente** el ADR de serving del [Capstone F6 (Plataforma RAG)](/fase-6-ai-engineering/proyecto/):
  por qué API ahora y bajo qué condiciones migrar a vLLM on-prem. El escenario on-prem y la
  consideración de privacidad alimentan la sección de seguridad
  ([6.14](/fase-6-ai-engineering/6-14-seguridad-llm/)) del Definition of Done, y la elección
  de motor/cuantización entra en el budget de costo/latencia
  ([6.16](/fase-6-ai-engineering/6-16-costo-latencia-llmops/)).
