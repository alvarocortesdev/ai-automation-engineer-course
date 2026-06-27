---
ejercicio_id: fase-6/diseno-evals-agente-y-juez
fase: fase-6
sub_unidad: "6.9"
version: 1
---

# Rúbrica — Diseño: plan de evals para un agente + un juez calibrado

> Rúbrica **analítica** atada a los `objetivos` del contrato. Es un ejercicio de **diseño**:
> no hay tests, se evalúa el **razonamiento**. Lo central es que el alumno (1) sepa qué medir
> de un agente y qué es determinista vs con-juez, (2) entienda que el golden set sale de
> **prod**, (3) trate el LLM-as-judge como un sistema **con sesgos que hay que mitigar y
> validar**, y (4) defina un gate y una trazabilidad reales. Un diseño que elige métricas
> sonoras sin justificar, o que confía en un juez sin nombrar sus sesgos, no demuestra el
> objetivo.

## Objetivos evaluados
- **O1** — Elegir métricas de agente y clasificar cada una determinista / con-juez, con razón.
- **O2** — Construir el golden set desde trazas de prod, justificando qué se promueve.
- **O3** — Diseñar un LLM-as-judge con rúbrica; mitigar 2 sesgos; validarlo contra humanos.
- **O4** — Definir gate de regresión + budget de costo/pasos y la trazabilidad del score.

## Criterios y niveles

### C1 — Métricas y su naturaleza (¿hace lo que el objetivo pide?) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Lista métricas sin definir, o no distingue determinista de con-juez. |
| **en-progreso** | Define las métricas pero clasifica mal (p. ej. dice que tool-call accuracy necesita un juez), o ignora costo/pasos. |
| **competente** | Define las 4 métricas; clasifica bien (tool-call/trajectory/costo deterministas; task completion abierta con juez) con razón por cada una. |
| **excelente** | Conecta costo/pasos con el techo de pasos del agente de 6.8 (el guardrail también es métrica) y matiza cuándo trajectory necesita comparación flexible (por orden/conjunto) vs exacta. |

### C2 — Dataset desde prod (calidad de ingeniería) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | El golden set es inventado en el escritorio; no menciona las trazas. |
| **en-progreso** | Dice "desde prod" pero no explica qué casos promueve ni por qué. |
| **competente** | Promueve casos desde trazas y justifica que los fallidos/raros valen más; da 2 ejemplos concretos. |
| **excelente** | Menciona el bucle de mejora continua (pulgar abajo del usuario → caso de eval) y versionar el dataset para comparar corridas. |

### C3 — LLM-as-judge: rúbrica, sesgos, validación · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay rúbrica, o trata el juez como objetivo (no nombra ningún sesgo). |
| **en-progreso** | Rúbrica vaga (sin escala o sin formato); nombra un sesgo sin mitigación accionable; no valida el juez. |
| **competente** | Rúbrica con criterio + escala + formato; 2 sesgos con 1 mitigación concreta cada uno; valida el juez contra labels humanos en una muestra. |
| **excelente** | Mitigaciones específicas y correctas (orden alternado para position, rúbrica anti-verbosity, juez de otra familia para self-enhancement) y propone un umbral de acuerdo juez-humano (p. ej. ≥0.9). |

### C4 — Gate, budget y trazabilidad · mapea: O4
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No define gate, o solo "que pase los tests"; sin budget ni trazabilidad. |
| **en-progreso** | Gate con umbral pero sin regresión; o budget sin número; o trazabilidad mencionada sin contenido. |
| **competente** | Gate con umbral **y** regresión vs baseline + tolerancia; budget de costo/pasos con techo; trazabilidad score ↔ prompt + modelo + dataset (Langfuse). |
| **excelente** | Ubica el gate en el pipeline (PRs que tocan el agente) y explica por qué un número sin la cadena de trazabilidad no es comparable entre corridas. |

## Errores típicos a marcar
- **"Más métricas = mejor"** — listar 8 métricas sin priorizar ni justificar; un buen plan elige pocas y defendibles.
- **Confiar en el LLM-as-judge sin sesgos** — tratar su número como verdad objetiva; no validarlo contra humanos.
- **Golden set inventado** — diseñar casos de cabeza en vez de promoverlos desde trazas reales (mide lo imaginado, no lo que pasa).
- **Gate sin regresión** — solo umbral absoluto; deja pasar una versión que empeoró respecto a prod.
- **Olvidar costo/pasos** — un agente que acierta pero gasta USD 40 y 30 pasos "pasa" un eval que solo mira calidad: falló en producción.
- **HITL/seguridad ausente** — no notar que el reembolso (irreversible) necesita tratamiento especial al evaluar acciones.
- (transversales) confía en la salida del LLM sin validar; falta un trade-off defendible; no versiona el dataset.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Diseño exhaustivo y bien redactado que enumera sesgos del juez con vocabulario de paper, pero no puede explicar **por qué** la mitigación de position bias es alternar el orden (qué cancela).
- Clasifica todas las métricas como "con-juez" (señal de no entender que tool-call/costo son set math / aritmética determinista).
- **Verificación sugerida:** pedir que justifique, sin notas, por qué task completion necesita un juez pero tool-call accuracy no. Si entendió, distingue "comparar (tool, args) contra un golden" (determinista) de "¿esto resolvió el problema del cliente?" (juicio abierto); si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca redactar el diseño por el alumno antes de que cierre su intento.
- **Pista (nivel 1):** "De tus 4 métricas, ¿cuáles puedo calcular con un `==` o sumando números, y cuál necesita que alguien *lea* la respuesta y juzgue? Esa última es la del juez."
- **Pregunta socrática (nivel 2):** "Tu juez prefiere siempre la respuesta más larga. ¿Eso es señal de calidad? ¿Cómo escribirías la rúbrica para que premie sustento y no extensión? ¿Y cómo sabrías que tu juez concuerda con un humano?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Estructura: (1) tabla métrica → determinista/juez → razón; (2) golden set = casos promovidos de trazas, prioriza fallidos/raros, versiónalo; (3) rúbrica del juez = criterio + escala 0–1 + formato JSON; mitiga position (orden alternado), verbosity (rúbrica anti-relleno), self-enhancement (juez de otra familia); valida vs muestra humana; (4) gate = umbral + baseline−tolerancia + budget de costo/pasos; trazabilidad en Langfuse."

## Conexión con el proyecto / capstone
- Este plan es el **eval gate de agente** del capstone estrella del portafolio (Fase 7): un agente que clasifica/extrae/decide/ejecuta, con tool-call accuracy, trajectory, task completion y costo/pasos como gate de regresión. Sin él, un agente en producción es un incidente con factura; con él, es un sistema defendible con un número.
