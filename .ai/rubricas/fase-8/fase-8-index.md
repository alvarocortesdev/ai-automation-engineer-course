---
ejercicio_id: fase-8/fase-8-index
fase: fase-8
sub_unidad: "8.0"
version: 1
---

# Rúbrica — Diagnóstico de Fase 8 + contrato de método de diseño

> Rúbrica analítica para un ejercicio **a-mano** de placement/metacognición y
> compromiso de método. No hay "respuesta correcta": se evalúa la **honestidad** del
> autodiagnóstico, la **concreción** del plan y la **calidad del contrato de método**
> (adoptar ADRs + diagramas con razón, articular el triángulo latencia/costo/calidad
> y pre-clasificar los 3 sistemas con una restricción dominante cada uno). El
> corrector premia el realismo y el razonamiento, no la ambición ni el "ya lo sé".

## Objetivos evaluados
- **O1** — Autoevaluar prerrequisitos y punto de partida por sub-unidad, distinguiendo "lo sé diseñar sin notas" de "lo reconozco".
- **O2** — Diseñar un plan con bloques semanales concretos, ritual de repaso y decisión de qué diferir (8.3/8.4).
- **O3** — Comprometerse con ADRs + diagramas, articular el triángulo latencia/costo/calidad con un ejemplo propio y pre-clasificar los 3 sistemas con una restricción dominante.

## Criterios y niveles

### C1 — Honestidad y cobertura del diagnóstico · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Falta una de las dos tablas, o la de sub-unidades cubre menos de las 5, o no asigna niveles. |
| **en-progreso** | Cubre prerrequisitos y las 5 sub-unidades, pero el nivel no es defendible (todo en "lo sé diseñar" sin evidencia, o todo "nuevo" pese a experiencia declarada), o falta la razón por fila. |
| **competente** | Prerrequisitos autoevaluados (con plan de retorno si falta alguno) **y** las 5 sub-unidades con nivel y razón coherente; aplica la prueba "¿lo diseñaría en una pizarra sin notas ahora?" de forma consistente. |
| **excelente** | Además matiza ("he dibujado arquitecturas pero nunca defendí un trade-off con números ni escribí un ADR" → `lo reconozco`, no "lo sé diseñar") y usa el diagnóstico para priorizar el plan (más tiempo donde marcó `nuevo`, sobre todo 8.5 si nunca pensó IA a escala). |

### C2 — Concreción y realismo del plan · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay plan, o son intenciones ("estudiaré más") sin días/horas; no decide qué diferir. |
| **en-progreso** | Hay bloques pero irreales (p. ej. 3 h diarias con pega full-time) o sin ritual de repaso, o no menciona 8.3/8.4. |
| **competente** | Bloques concretos (día/hora/duración) plausibles **y** ritual de repaso explícito **y** decisión clara de qué difiere (8.3/8.4) con razón. |
| **excelente** | El plan ata el repaso al *spacing* (reescribir de memoria un diagrama/ADR al día siguiente y a los pocos días), ajusta carga según el diagnóstico y protege tiempo para 8.5 (especialización) y para el ejercicio de cierre largo (3 diseños). |

### C3 — Calidad del contrato de método (ADRs, triángulo, 3 sistemas) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No adopta ADRs/diagramas, o lo dice sin razón; no nombra el triángulo ni clasifica los 3 sistemas. |
| **en-progreso** | Adopta ADRs + diagramas pero la razón es superficial ("son útiles"); nombra el triángulo sin ejemplo propio, o clasifica los 3 sistemas sin restricción dominante. |
| **competente** | Explica por qué un diagrama sin ADR es decoración **y** articula el triángulo con un ejemplo propio **y** pre-clasifica los 3 sistemas con una restricción dominante plausible para cada uno. |
| **excelente** | La razón de los ADRs conecta con la entrevista ("defender el porqué, no solo el qué"); el ejemplo del triángulo es concreto y propio (p. ej. "modelo grande sube calidad pero me saca del budget de latencia"); las restricciones dominantes de los 3 sistemas son agudas (aislamiento multi-tenant, latencia/costo del agente, frescura del dato) y anticipa qué ADR escribirá primero. |

## Errores típicos a marcar
- **Sobreconfianza** (Dunning-Kruger): marcar "lo sé diseñar sin notas" por haber *dibujado* arquitecturas. Pedir la prueba: "¿dirigirías esa pizarra 40 min sin notas? ¿qué trade-off defiendes en 8.5?".
- **Confundir dibujar con diseñar:** un diagrama bonito no es una decisión defendida. "He hecho diagramas" no es "he escrito un ADR ni estimado capacidad".
- **Diseñar de más como señal de nivel:** creer que mencionar microservicios/Kafka/sharding lo hace ver senior (es justo la misconception que la fase ataca).
- **Plan de fantasía:** bloques irreales sin día/hora, o sin ritual de repaso.
- **No decidir qué diferir:** tratar 8.3/8.4 como ruta crítica e inflar el plan.
- **Triángulo recitado sin ejemplo propio:** repetir "latencia, costo, calidad" sin una decisión concreta donde una arista compita con otra.
- **Restricciones dominantes genéricas:** "que escale bien" para los tres, en vez de algo específico por sistema.
- **Delegar el diagnóstico/contrato a la IA:** pedirle a un chat "qué nivel tengo" o "escríbeme el contrato de método".

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Plan o contrato con redacción genérica que no menciona ninguna sub-unidad concreta de **esta** Fase 8 (suena a plantilla de IA).
- Diagnóstico uniforme (todo el mismo nivel) sin razones específicas por fila.
- Ejemplo del triángulo abstracto/de manual, sin aterrizarlo en una decisión propia.
- **Verificación sugerida:** pedir que explique en voz alta su ejemplo del triángulo y por qué clasificó un sistema como el más difícil. Si se autoevaluó de verdad, lo hace; si la IA lo escribió, se traba.

## Feedback sugerido (graduado)
> Nunca "darle el plan" ni "escribirle el contrato". Empujar a que el suyo sea honesto, sostenible y argumentado.
- **Pista (nivel 1):** "Mira las filas que marcaste 'lo sé diseñar sin notas'. ¿Es haber *dibujado* el tema o poder *defenderlo en una pizarra* con un trade-off? Revisa 8.2 (aggregate/ACL) y 8.5 (triángulo) con esa lente."
- **Pregunta socrática (nivel 2):** "Tu plan dice cuánto quieres estudiar, pero ¿qué día y hora ocurre el primer bloque esta semana? ¿Cuándo reescribes de memoria un ADR? Y en el triángulo: ¿qué decisión TUYA sube una arista y baja otra?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Convierte cada intención en un bloque con día/hora que quepa en tu semana, añade una línea de repaso por bloque, y protege tiempo para 8.5. En el contrato, sustituye el ejemplo genérico del triángulo por una decisión concreta (p. ej. elegir modelo barato + caché semántico vs modelo caro), y dale a cada uno de los 3 sistemas una restricción dominante específica."

## Conexión con el proyecto / capstone
- La honestidad del diagnóstico, la disciplina del plan y el compromiso con **ADRs + diagramas** son **exactamente** lo que sostiene el ejercicio de cierre de F8 (diseña 3 sistemas en papel). El triángulo latencia/costo/calidad y las restricciones dominantes que aquí anticipas son las decisiones que tendrás que defender en cada diseño. El método que firmas aquí es el que distingue un diagrama decorativo de una arquitectura defendible —y el que examinan en la entrevista de system design de [Track-0](/track-0-empleabilidad/).
