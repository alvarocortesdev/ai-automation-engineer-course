---
ejercicio_id: fase-6/decision-rag-vs-finetuning
fase: fase-6
sub_unidad: "6.13"
version: 1
---

# Rúbrica — Decisión: RAG, fine-tuning, híbrido o ninguno

> Rúbrica **analítica** atada a los `objetivos` del contrato. Ejercicio de **diseño**: no
> hay respuesta única. El corrector evalúa la **calidad del trade-off**, no la coincidencia
> literal. El objetivo de fondo: que el alumno **derive** cada decisión del eje dominante
> (conocimiento vs comportamiento), entienda que RAG y FT no son dicotomía, y proponga un
> eval para decidir con un número en vez de una corazonada.

## Objetivos evaluados

- **O1** — Decidir RAG / fine-tuning / híbrido / ninguno según el eje dominante.
- **O2** — En el caso híbrido, explicar qué cubre RAG (hechos) y qué cubre el fine-tuning/prompt (forma): no son excluyentes.
- **O3** — Proponer un eval de una línea que zanjaría la decisión (medir, no adivinar).

## Criterios y niveles

### C1 — Decisión derivada del eje dominante · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Elige "lo mejor" o lo mismo para todos; o propone fine-tuning para los precios (Caso 1) "para que el modelo se los sepa". |
| **en-progreso** | Nombra el eje en algunos casos pero la decisión no se deriva de él, o confunde conocimiento con comportamiento en 1–2 casos. |
| **competente** | Caso 1 → RAG (conocimiento cambiante); Caso 4 → ninguno (un prompt basta); Caso 2 → fine-tuning (forma a alto volumen, tras prompt); cada uno derivado de su eje. |
| **excelente** | Separa con nitidez los tres ejes y nombra por qué el prompt es el primer intento en Caso 2 antes de saltar a FT; reconoce el costo a escala como gatillo real del FT. |

### C2 — Híbrido bien entendido (no dicotomía) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Trata RAG y FT como alternativas excluyentes; no marca ningún caso como híbrido, o marca el Caso 3 como "solo fine-tuning". |
| **en-progreso** | Marca el Caso 3 como híbrido pero no separa qué cubre cada parte. |
| **competente** | Caso 3 → híbrido: **RAG** para los contratos (hechos privados/cambiantes) + **fine-tuning o prompt** para la voz/estructura formal; cada eje a su técnica. |
| **excelente** | Nota que el RAG es no-negociable en Caso 3 (no se fine-tunean hechos) y que el FT de la forma es condicional a que el prompt no baste y a que un eval lo confirme. |

### C3 — DPO vs SFT en el caso de preferencias · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Caso 5 resuelto como RAG, o como SFT sin notar el matiz de "rankear vs escribir". |
| **competente** | Caso 5 → fine-tuning de comportamiento; reconoce que es una tarea de **preferencias** (rankear cuál suena mejor) más que de demostrar la respuesta perfecta. |
| **excelente** | Nombra **DPO** explícitamente como la técnica que entrena con pares `(preferida, rechazada)`, y por qué encaja mejor que SFT cuando "saben rankear pero no escribir". |

### C4 — Eval que zanja + comunicación (ADR-able) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No propone evals, o propone "preguntarle a la IA" / "ver si se siente mejor". |
| **competente** | Cada caso propone un eval concreto (métrica + sobre qué datos): p. ej. "% de respuestas con JSON válido sobre 200 tickets reales" para Caso 2; "exactitud factual sobre un set de preguntas con respuesta conocida" para Caso 1. |
| **excelente** | Plantea el eval como **comparación baseline vs candidato** (mide prompt+RAG primero, luego FT, y adopta solo si la mejora paga el costo); menciona un riesgo de gobernanza (FT hornea datos en los pesos) donde aplique. |

## Errores típicos a marcar

- **Fine-tunear hechos** (Caso 1): el error de manual; el modelo los aproxima, alucina y no se actualizan sin re-entrenar.
- Tratar RAG y fine-tuning como **excluyentes** y no detectar el caso híbrido (Caso 3).
- Proponer fine-tuning en Caso 4 (un prompt basta) → quemar plata por deporte.
- Saltar a fine-tuning en Caso 2 **sin** intentar primero un prompt, o sin nombrar el costo a escala como el gatillo.
- Resolver el Caso 5 como SFT sin notar que es un problema de **preferencias** (DPO).
- (transversal) ningún eval propuesto, o "se siente mejor" como criterio; ningún trade-off defendible.

## Señales de dependencia-IA

- Cinco casos con prosa pulida e idéntica estructura retórica pero **sin** comprometerse a un
  veredicto (hedging tipo "podría ser RAG o fine-tuning según el caso").
- Menciona DPO/LoRA con detalles inventados que no salieron en la lección.
- **Verificación sugerida:** pídele que explique, sin notas, por qué fine-tunear los precios
  del Caso 1 es un error. Si lo razonó, habla de que el modelo aproxima hechos y no se
  actualiza; si lo copió, se queda en "RAG es mejor para datos" sin el mecanismo.

## Feedback sugerido (graduado)

> Ordenadas de menos a más directas. **Nunca escribir la decisión por el alumno.**

- **Pista (nivel 1):** "Para cada caso, responde primero una sola pregunta: ¿lo que falta es
  **conocimiento** (un hecho/dato) o **comportamiento** (una forma)? Esa pregunta ya decide
  casi todo."
- **Pregunta socrática (nivel 2):** "En el Caso 1, si fine-tuneas los precios hoy y mañana
  sube uno, ¿qué dice el modelo? ¿Cuánto cuesta corregirlo? Compara con re-indexar un
  documento en RAG."
- **Dirección concreta (nivel 3, sólo tras intento real):** "Tu Caso 3 va bien como híbrido,
  pero falta separar los ejes: RAG cubre *qué dicen los contratos* (hechos privados,
  cambiantes), el fine-tuning o el prompt cubre *la voz formal* (comportamiento). Y para el
  Caso 5, fíjate que 'saben rankear pero no escribir' apunta a DPO, no a SFT."

## Conexión con el proyecto / capstone

- Esta decisión es **literalmente** el ADR de "por qué (no) fine-tuneamos" del
  [Capstone F6 (Plataforma RAG)](/fase-6-ai-engineering/proyecto/): por qué el conocimiento
  lo cubre RAG, el comportamiento el prompt, y bajo qué condición medible reconsiderarías un
  LoRA. El eval que zanja cada caso conecta con
  [6.9 · Eval-driven development](/fase-6-ai-engineering/6-9-eval-driven-development/), y el
  riesgo de hornear datos en los pesos con
  [6.14](/fase-6-ai-engineering/6-14-seguridad-llm/) / [6.15](/fase-6-ai-engineering/6-15-ai-governance/).
