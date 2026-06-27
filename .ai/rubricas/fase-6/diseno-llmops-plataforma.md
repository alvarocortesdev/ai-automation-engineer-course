---
ejercicio_id: fase-6/diseno-llmops-plataforma
fase: fase-6
sub_unidad: "6.16"
version: 1
---

# Rúbrica — Diseño: la capa LLMOps de la plataforma RAG

> Rúbrica **analítica** atada a los `objetivos` del contrato. Es un ejercicio de **diseño**: no hay
> tests. El corrector evalúa la **calidad del trade-off** y si el alumno puede **defender** cada
> decisión derivándola de la restricción dominante, no que coincida palabra por palabra con la
> solución de referencia (hay varias respuestas defendibles).

## Objetivos evaluados

- **O1** — Diseñar las dos capas de caching (provider con prefijo estable/volátil; semantic con umbral calibrado por eval) y nombrar dónde no sirve.
- **O2** — Política de ruteo barato→caro + corte interactivo/batch, justificados, y cómo se evalúa el router.
- **O3** — Budget de costo/latencia como gate atado al eval, y la capa LLMOps (fallbacks, versionado, despliegue seguro, monitoreo).
- **O4** — Un riesgo de seguridad que el caching introduce, con mitigación.

## Criterios y niveles

### C1 — Caching de dos capas · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Confunde prompt caching del provider con semantic cache, o trata uno solo; no separa prefijo estable de volátil. |
| **en-progreso** | Distingue las dos capas pero el umbral del semantic cache es un número inventado, o no nombra un caso donde el caching no sirve. |
| **competente** | Prefijo estable (system prompt, docs) adelante y volátil (pregunta del usuario) al final, con ejemplo; umbral del semantic cache **calibrado con el eval**; nombra un caso donde no sirve (p. ej. datos que cambian, prefijo de un solo uso). |
| **excelente** | Anticipa el invalidador silencioso (timestamp/UUID al inicio) y verifica con `cache_read_input_tokens`; razona el break-even del cache write. |

### C2 — Ruteo + batching · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | "Usa siempre Opus" o no justifica los escalones; no distingue interactivo de batch. |
| **en-progreso** | Define escalones razonables pero no dice de dónde sale la dificultad, o no dice cómo evita degradar la calidad, o el corte batch no está justificado por latencia. |
| **competente** | Escalones justificados (tarea→modelo) + señal de dificultad (heurística/clasificador) + cómo evalúa el router; corte interactivo (chat/búsqueda) vs. batch (ingest/backfill) justificado por latencia. |
| **excelente** | Cuantifica el ahorro esperado del ruteo (p. ej. "80% del tráfico a Haiku") y ata la evaluación del router al eval de 6.9. |

### C3 — Budget como gate + LLMOps · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay budget con números, o no es un gate; LLMOps ausente o reducido a un bullet. |
| **en-progreso** | Budget con números pero no atado al eval; LLMOps cubre solo 1-2 de las 4 piezas. |
| **competente** | Budget concreto (USD/consulta + p95) que **bloquea** un merge, encadenado al gate de 6.9; LLMOps cubre fallback, versionado (ADR + Conventional Commits), despliegue seguro (canary + rollback) y monitoreo (Langfuse). |
| **excelente** | El monitoreo realimenta el dataset de eval (ciclo cerrado); el versionado ata score↔prompt↔modelo↔dataset. |

### C4 — Seguridad (hilo transversal) · mapea: O4
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No nombra ningún riesgo de seguridad del caching, o nombra uno irrelevante. |
| **en-progreso** | Nombra un riesgo (fuga entre usuarios / datos sensibles cacheados) pero sin mitigación concreta. |
| **competente** | Riesgo concreto (semantic cache sirve la respuesta de un usuario a otro, o cachea PII) + mitigación (cache por tenant/usuario, no cachear contenido sensible, scoping del cache key). |
| **excelente** | Conecta con OWASP LLM (6.14): sensitive information disclosure, y cómo el cache key debe incluir el contexto de autorización. |

## Errores típicos a marcar

- Confundir prompt caching del provider (prefix match, lo cachea el provider) con semantic cache (lo haces tú, por similitud).
- Umbral del semantic cache fijado "a ojo" sin calibrar con el eval → hits incorrectos servidos como verdad.
- "Siempre el modelo más potente por las dudas": ignora la palanca de costo más grande.
- Batching para una request interactiva (el usuario espera) → confunde el trade-off latencia/costo.
- Budget que es solo de calidad, sin techo de costo/latencia, o que no bloquea (es decorativo).
- LLMOps sin despliegue seguro: cambio de prompt directo a prod "porque se ve mejor".
- (transversales) cachear sin pensar la fuga entre usuarios; falta de un solo trade-off defendible.

## Señales de dependencia-IA

> Describir sin acusar; proponer una verificación.

- Diseño que enumera buzzwords (caching, ruteo, fallback) sin derivar ninguna decisión de una restricción concreta.
- Umbral, escalones o budget con números "redondos" que el alumno no puede justificar al preguntarle "¿por qué ese y no otro?".
- **Verificación sugerida:** pedir que defienda **un** número (el umbral del semantic cache, el techo de USD/consulta) explicando qué pasa si lo sube y qué pasa si lo baja.

## Feedback sugerido (graduado)

> Nunca escribir el diseño por el alumno.

- **Pista (nivel 1):** "¿Tu prompt caching y tu semantic cache son la misma cosa? Uno lo hace el provider por prefijo, el otro lo haces tú por similitud — sepáralos."
- **Pregunta socrática (nivel 2):** "Si bajas el umbral del semantic cache para tener más hits, ¿qué le pasa a las respuestas que sirves? ¿Cómo sabrías si están bien sin un eval?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Para cada sección, escribe primero la restricción que manda (costo, latencia, confiabilidad, seguridad) y deriva la decisión de ahí. El budget tiene que ser un número que **bloquee** un merge, no una aspiración; conéctalo al gate de eval de 6.9."

## Conexión con el proyecto / capstone

- Este diseño **es** el ADR de costo/latencia + LLMOps del **Capstone F6 (RAG de producción)**: el budget como gate, el caching y el ruteo justificados, y el monitoreo con Langfuse atando USD↔ms↔score↔prompt↔modelo son entregables de primera clase del Definition of Done.
