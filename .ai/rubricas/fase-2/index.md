---
ejercicio_id: fase-2/index
fase: fase-2
sub_unidad: "2.0"
version: 1
---

# Rúbrica — Diagnóstico de hábitos y plan de Fase 2

> Rúbrica analítica para un ejercicio **a-mano** de placement/metacognición + un
> primer *gap report*. No hay "respuesta correcta": se evalúa la **honestidad** del
> autodiagnóstico, la **concreción** del plan y la **agudeza** del *gap report*
> (¿vio los hábitos faltantes?, ¿los mapeó a la sub-unidad correcta?, ¿resistió la
> tentación de reescribir?). El corrector premia ver el hueco, no taparlo.

## Objetivos evaluados
- **O1** — Autoevaluar el punto de partida por sub-unidad (2.1–2.13), distinguiendo "lo sé hacer" de "lo reconozco".
- **O2** — Diseñar un plan con bloques semanales concretos, interleaving de DSA y ritual de repaso.
- **O3** — Producir un *gap report* de un trozo de código junior: nombrar hábitos faltantes (sin arreglar) y mapearlos a la sub-unidad que los cubre.

## Criterios y niveles

### C1 — Honestidad y cobertura del diagnóstico · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Falta la tabla, o cubre menos de las 13 sub-unidades, o no asigna niveles. |
| **en-progreso** | Cubre las 13 pero el nivel no es defendible (todo en "lo sé hacer" sin evidencia, o todo "nuevo" pese a experiencia previa declarada), o sin la razón por fila. |
| **competente** | Las 13 sub-unidades con nivel **y** una razón coherente; aplica la prueba "¿podría resolverlo sin notas ahora?" de forma consistente. |
| **excelente** | Además matiza ("reconozco mocks pero nunca diseñé un fake") y usa el diagnóstico para priorizar qué sub-unidades necesitan más tiempo en el plan. |

### C2 — Concreción y realismo del plan · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay plan, o son intenciones ("estudiaré más") sin días/horas. |
| **en-progreso** | Hay bloques pero irreales (3 h diarias con pega full-time) o sin ritual de repaso, o no menciona el interleaving de DSA. |
| **competente** | Bloques concretos (día/hora/duración) plausibles para su vida, ritual de repaso explícito, **y** una estrategia para distribuir DSA en vez de hacerlo en bloque. |
| **excelente** | Ata el repaso al *spacing* (revisar al día siguiente + a los pocos días), ajusta la carga según el diagnóstico, y agenda la red de tests (2.6) antes de los refactors (2.3/capstone). |

### C3 — Agudeza del *gap report* · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay *gap report*, o solo dice "está mal" sin nombrar hábitos concretos, o reescribe la función (resolver en vez de ver). |
| **en-progreso** | Nombra 1–3 hábitos faltantes, o no los mapea a sub-unidades, o mezcla observaciones válidas con una reescritura del código. |
| **competente** | Nombra **≥ 4 hábitos faltantes** distintos (nombres, magic numbers, ausencia de tests, caso borde sin cubrir, falta de spec/ADR) y mapea cada uno a la sub-unidad correcta, **sin** reescribir la función. |
| **excelente** | Además detecta la ambigüedad de frontera (`>` vs `>=` en `y == 100`/`y == 50`) como algo que *solo un test fijaría*, y nota que no se puede refactorizar con seguridad sin esa red de tests primero. |

### C4 — Comprensión demostrada (el razonamiento calza con el trabajo) · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | El *gap report* o el diagnóstico suenan a plantilla genérica, sin referencia a *este* código o a *estas* sub-unidades. |
| **en-progreso** | Razonamiento parcial: lista hábitos correctos pero no puede explicar por qué cada uno importa. |
| **competente** | Cada hueco viene con un "por qué" de una línea (qué problema causa ese hábito faltante). |
| **excelente** | Conecta el *gap report* con el rol de **revisor de PR** y con la tesis de la fase (la calidad es un hábito, no un paso final). |

## Errores típicos a marcar
- **Sobreconfianza** (Dunning-Kruger): marcar "lo sé hacer sin notas" en sub-unidades que nunca practicó (clásico en quien escribió tests "alguna vez" pero nunca hizo TDD ni mutation testing). Pedir la prueba: "¿lo resolverías ahora sin notas?".
- **Reescribir en vez de diagnosticar:** el error #1 de este ejercicio. Arreglar la función `calc` es *refactorizar*, y aún no toca —además, refactorizar sin tests es reescribir y rezar. El *gap report* debe **nombrar**, no resolver.
- **Plan de fantasía:** bloques irreales sin día/hora, o que no sobreviven la primera semana; ausencia del *interleaving* de DSA.
- **Falta el ritual de repaso:** plan que solo dice "estudiar" sin *active recall* ni *spacing*.
- **Gap report superficial:** "le faltan tests" y nada más; no ve nombres, magic numbers, casos borde ni la falta de ADR.
- **Mapeo flojo:** nombra hábitos pero no los liga a la sub-unidad que los cubre (clean code → 2.2, smells → 2.3, tests → 2.6–2.9, ADR → 2.13).
- (transversal) confundir coverage% con calidad de tests al hablar del hueco de testing (es justo lo que la 2.9 desmonta).

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- *Gap report* impecablemente estructurado pero genérico, que no cita los identificadores reales del snippet (`calc`, `x`, `y`, `100`, `50`) ni mapea a las sub-unidades **de esta** fase: suena a salida de chat.
- Diagnóstico uniforme (todo el mismo nivel) sin razones específicas por fila.
- Plan con vocabulario de "productividad" pero sin un solo bloque con día/hora concretos de *su* semana.
- **Verificación sugerida:** pedir que explique en voz alta por qué `100` es un *smell* y no "solo una constante", y a qué sub-unidad lo mapeó. Si se autoevaluó de verdad, lo hace; si la IA lo escribió, se traba.

## Feedback sugerido (graduado)
> Nunca "darle el gap report ni el plan". Empujar a que vea por sí mismo.
- **Pista (nivel 1):** "En tu *gap report*, ¿listaste solo 'faltan tests'? Vuelve a leer la primera línea: `def calc(x, y)`. ¿Entiendes qué hace sin leer el resto? Ese es un hueco distinto."
- **Pregunta socrática (nivel 2):** "Tu código devuelve algo distinto si `y` es 100 que si es 101. ¿Estás seguro de que el `>` no debía ser `>=`? ¿Qué artefacto —de los que aún no escribiste— te diría la respuesta sin adivinar?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Estructura el *gap report* como un revisor de PR: una línea por hábito faltante, su 'por qué' y la sub-unidad que lo cubre. Y NO reescribas la función: nombrar el hueco es el ejercicio; arreglarlo viene después, con la red de tests delante."

## Conexión con el proyecto / capstone
- El *gap report* es un ensayo en pequeño del **Capstone F2 — Refactor + suite de tests**: ahí harás exactamente esto pero a escala (ver los huecos del proyecto de la Fase 1) y luego, con una red de tests, los cerrarás. La honestidad del diagnóstico y la disciplina del plan son el calendario con el que llegarás al capstone.
