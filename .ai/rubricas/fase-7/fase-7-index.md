---
ejercicio_id: fase-7/fase-7-index
fase: fase-7
sub_unidad: "7.0"
version: 1
---

# Rúbrica — Diagnóstico de Fase 7 + decisión de capstone estrella

> Rúbrica analítica para un ejercicio **a-mano** de placement/metacognición y
> decisión de portafolio. No hay "respuesta correcta": se evalúa la **honestidad**
> del autodiagnóstico, la **concreción** del plan y la **calidad del trade-off**
> de la decisión de capstone. Una decisión bien argumentada hacia el agéntico (F7)
> vale lo mismo que una bien argumentada hacia el RAG (F6); lo que se mide es el
> razonamiento, no la opción. El corrector premia el realismo y el trade-off
> nombrado, no la ambición ni la opción "de moda" (ni copiar la recomendación del
> curso sin defenderla).

## Objetivos evaluados
- **O1** — Autoevaluar prerrequisitos y punto de partida por sub-unidad, distinguiendo "lo sé hacer" de "lo reconozco".
- **O2** — Diseñar un plan con bloques semanales concretos, ritual de repaso y decisión de qué diferir (7.4/7.6).
- **O3** — Decidir la estrella de portafolio con un trade-off defendible y reconocer los gates difíciles del DoD.

## Criterios y niveles

### C1 — Honestidad y cobertura del diagnóstico · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Falta una de las dos tablas, o la de sub-unidades cubre menos de las 10, o no asigna niveles. |
| **en-progreso** | Cubre prerrequisitos y las 10 sub-unidades, pero el nivel no es defendible (todo en "lo sé hacer" sin evidencia, o todo "nuevo" pese a experiencia declarada), o falta la razón por fila. |
| **competente** | Prerrequisitos autoevaluados (con plan de retorno si falta alguno) **y** las 10 sub-unidades con nivel y razón coherente; aplica la prueba "¿podría resolverlo sin notas ahora?" de forma consistente. |
| **excelente** | Además matiza ("armo flujos en n8n pero nunca configuré un error workflow ni pensé el evento duplicado" → `lo reconozco`, no "lo sé hacer") y usa el diagnóstico para priorizar el plan (más tiempo donde marcó `nuevo`, sobre todo el bloque de Data Engineering 7.5a–d y el eval de agente de 7.7). |

### C2 — Concreción y realismo del plan · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay plan, o son intenciones ("estudiaré más") sin días/horas; no decide qué diferir. |
| **en-progreso** | Hay bloques pero irreales (p. ej. 3 h diarias con pega full-time) o sin ritual de repaso, o no menciona 7.4/7.6. |
| **competente** | Bloques concretos (día/hora/duración) plausibles **y** ritual de repaso explícito **y** decisión clara de qué difiere (7.4/7.6) con razón. |
| **excelente** | El plan ata el repaso al *spacing* (revisar al día siguiente + a los pocos días), ajusta carga según el diagnóstico y protege tiempo extra para Data Engineering (7.5a–d) y el eval de agente (7.7), reconociéndolos como el músculo más nuevo y de mayor retorno. |

### C3 — Calidad de la decisión de capstone (trade-off) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No elige estrella, o elige sin ninguna razón ("me gusta más" / "porque el curso lo dice"). |
| **en-progreso** | Elige y da una razón superficial, pero no compara alternativas ni nombra los gates difíciles del DoD. |
| **competente** | Elige una estrella **y** argumenta con un trade-off real (saturación de mercado / nicho / complejidad / tiempo) **y** nombra tres puntos del DoD que le costarán. |
| **excelente** | El trade-off considera honestamente la otra opción y la descarta con criterio (p. ej. reconoce que el RAG genérico está saturado y que el agéntico expone manejo de fallas, su nicho de automatización) y conecta los gates difíciles con sub-unidades concretas (eval de agente 7.7/6.9, DLQ/replay 7.2, durabilidad 7.3, HITL/costo 7.7). |

## Errores típicos a marcar
- **Sobreconfianza** (Dunning-Kruger): marcar "lo sé hacer sin notas" en temas que solo *usó* (clásico en quien arma flujos en n8n/Make). Pedir la prueba: "¿lo resolverías ahora sin notas? Explícame por qué 7.2 quedó en ese nivel; ¿cómo harías el flujo idempotente y qué pasa con la DLQ?".
- **Confundir usar con diseñar:** "sé hacer n8n" cuando en realidad sabe *arrastrar nodos del happy path*, no *diseñar idempotencia, error workflows ni criterio de salida*. "Moví datos con un ETL" no es "modelé un star schema con dbt y tests". Es justo la brecha que la fase ataca.
- **Plan de fantasía:** bloques irreales sin día/hora, o sin ritual de repaso (el hábito que el curso instala).
- **No decidir qué diferir:** tratar 7.4/7.6 como ruta crítica e inflar el plan.
- **Decisión de capstone sin trade-off:** elegir por moda o por obediencia ("agéntico porque el curso lo recomienda") sin comparar saturación/nicho/tiempo.
- **Subestimar el Data Engineering:** no reservar tiempo para 7.5a–d pese a marcarlo `nuevo` (es el gap individual más grande del roadmap).
- **Delegar el propio diagnóstico/decisión a la IA:** pedirle a un chat "qué nivel tengo" o "qué capstone elijo".

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Plan o decisión con redacción genérica que no menciona ninguna sub-unidad concreta de **esta** Fase 7 (suena a plantilla de IA).
- Diagnóstico uniforme (todo el mismo nivel) sin razones específicas por fila.
- Trade-off de capstone que recita argumentos de mercado sin aterrizarlos en *su* situación (su nicho, su tiempo, su experiencia previa de automatización).
- **Verificación sugerida:** pedir que justifique en voz alta por qué eligió su capstone y qué gate del DoD le da más miedo. Si se autoevaluó de verdad, lo hace; si la IA lo escribió, se traba.

## Feedback sugerido (graduado)
> Nunca "darle el plan" ni "elegir su capstone". Empujar a que el suyo sea honesto, sostenible y argumentado.
- **Pista (nivel 1):** "Mira las filas que marcaste 'lo sé hacer sin notas'. ¿Es *usar* el tema o *diseñarlo/diagnosticarlo* sin ayuda? Revisa 7.2 (idempotencia/DLQ) y 7.5b (dbt) con esa lente."
- **Pregunta socrática (nivel 2):** "Tu plan dice cuánto quieres estudiar, pero ¿en qué día y hora ocurre el primer bloque esta semana? ¿Y cuándo reescribes de memoria lo anterior? Sobre el capstone: ¿por qué la otra opción NO es tu estrella?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Convierte cada intención en un bloque con día/hora/duración que quepa en tu semana, añade una línea de repaso por bloque, y protege tiempo extra para Data Engineering (7.5a–d) y el eval de agente (7.7). En la decisión, escribe explícitamente qué pierdes al no elegir la otra opción: eso es el trade-off."

## Conexión con el proyecto / capstone
- La honestidad del diagnóstico, la disciplina del plan y la decisión de portafolio son **exactamente** lo que sostiene los capstones de F7 (agéntico) y F6 (RAG). El eval gate de agente, el HITL + techo de costo y la DLQ/replay durable que aquí reconoces como difíciles son los **gates** del Definition of Done que tendrás que cumplir. El plan que defines es el calendario con el que llegarás a tu **proyecto estrella** —el que demuestra tus dos pilares a la vez.
