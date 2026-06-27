---
ejercicio_id: fase-6/decisiones-sampling-modelo
fase: fase-6
sub_unidad: "6.1"
version: 1
---

# Rúbrica — Decisiones de sampling, alucinación y modelo

> Rúbrica analítica para un ejercicio **de diseño**. No hay respuesta única: se
> evalúa la **coherencia entre la decisión y la tarea** y la **calidad de la
> justificación**. Una decisión "no estándar" bien argumentada vale más que la
> "correcta" sin defensa. El corrector mide criterio, no coincidencia.

## Objetivos evaluados
- **O1** — Elegir y justificar el sampling apropiado a cada tarea.
- **O2** — Evaluar el riesgo de alucinación y diseñar dos mitigaciones por caso.
- **O3** — Elegir familia/tier de modelo nombrando la restricción dominante.

## Criterios y niveles

### C1 — Sampling coherente con la tarea · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No decide, o asigna al revés (alta para SQL/extracción, baja para brainstorming) sin notarlo. |
| **en-progreso** | Decide bien en general pero sin justificar, o justifica con muletillas ("porque es mejor"). |
| **competente** | Baja/determinista para SQL y FAQ factual; alta/variada para nombres; cada decisión ligada a la naturaleza de la tarea. |
| **excelente** | Además reconoce el matiz 2026 (algunas APIs no exponen temperature; se steerea por prompt/effort) en al menos un escenario. |

### C2 — Análisis y mitigación de alucinaciones · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No evalúa el riesgo, o las "mitigaciones" no atacan la alucinación (p. ej. "usar buen prompt" a secas). |
| **en-progreso** | Riesgo razonable pero mitigaciones genéricas o repetidas (dos veces "temperature baja"). |
| **competente** | Riesgo bien calibrado por caso (FAQ y SQL = alto impacto; nombres = bajo) + dos mitigaciones **distintas y apropiadas** (grounding/RAG, validación de salida, citar y verificar, HITL, "di que no sabes"). |
| **excelente** | Conecta la mitigación con dónde se profundiza (RAG → 6.7, validación → 6.4, evals → 6.9) y prioriza por impacto/costo. |

### C3 — Elección de modelo por restricción · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | "El mejor modelo" sin criterio, o ignora una restricción evidente (manda datos sensibles a una API cerrada en el caso SQL). |
| **en-progreso** | Elige tier razonable pero no nombra la restricción dominante. |
| **competente** | SQL → privacidad (open-weight self-hosted); nombres → costo (tier barato basta); FAQ → latencia + costo (tier rápido) con calidad suficiente. Restricción dominante explícita. |
| **excelente** | Añade el trade-off honesto (qué cede al elegir barato/local) y menciona "empezar barato y subir solo si los evals lo exigen". |

## Errores típicos a marcar
- **Sampling al revés**: temperature alta para extracción/SQL (invita a inventar) o baja para brainstorming (mata la variedad).
- **Mandar datos sensibles fuera**: en el caso SQL, elegir una API cerrada sin notar la restricción de privacidad.
- **Mitigaciones que no mitigan**: "mejor prompt" o "usar GPT-4" como si fueran defensas contra alucinación.
- **"El mejor modelo" como respuesta**: no nombrar la restricción que manda.
- **Tratar el FAQ como bajo riesgo**: una respuesta inventada de cara al cliente es alto impacto.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Las nueve decisiones idénticas a una respuesta "de manual" pero sin poder defender ninguna en voz alta.
- Vocabulario muy por encima del nivel (cita papers o técnicas no vistas) sin conexión con los escenarios concretos.
- **Verificación sugerida:** pedir que defienda una sola decisión —"¿por qué open-weight y no una API cerrada para el SQL?"— y que proponga qué pasaría si cambiara la restricción (p. ej. si los datos dejaran de ser sensibles).

## Feedback sugerido (graduado)
> Nunca entregar la matriz de respuestas completa.
- **Pista (nivel 1):** "Vuelve a leer el escenario del FAQ: ¿qué pasa si el bot inventa un precio frente a un cliente? ¿Eso es riesgo bajo o alto?"
- **Pregunta socrática (nivel 2):** "Para el generador de SQL, ¿qué restricción pesa más: tener el modelo más inteligente, o que los datos no salgan de la empresa? ¿Cómo cambia tu elección?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Tus mitigaciones repiten 'temperature baja'. Una mitigación distinta ataca otra causa: para el FAQ, **grounding/RAG** (le das el documento correcto) ataca la causa raíz —que el modelo rellene de memoria—. Reescribe la mitigación 2 atacando una causa diferente a la 1."

## Conexión con el proyecto / capstone
- Estas tres decisiones (sampling, mitigación de alucinación, elección de modelo) son exactamente las que documentarás en los **ADRs** del Capstone F6 y las que tu **eval harness** (6.9) tendrá que respaldar con números.
