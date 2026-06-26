---
ejercicio_id: fase-2/escribir-adr-y-mini-spec
fase: fase-2
sub_unidad: "2.13"
version: 1
---

# Rúbrica — Mini-spec + ADR de una decisión real

> Rúbrica **analítica** atada a los `objetivos`. **No hay respuesta correcta única.** Lo que se evalúa
> NO es si el alumno coincidió con una solución, sino si **resolvió la ambigüedad a propósito** (spec) y
> **registró una decisión defendible con sus alternativas** (ADR). Una decisión contraria, bien
> argumentada, es `competente` o `excelente`. Este ejercicio no se implementa: si el alumno entregó
> código de `acortar_titulo`, se desvió del objetivo (especificar, no codear).

## Objetivos evaluados
- **O1** — Mini-spec que resuelve la ambigüedad antes de codear: entradas con **restricciones**, salida con **invariante**, **≥3 casos borde** acordados, criterios de aceptación **falsables**.
- **O2** — ADR de la decisión significativa: **contexto/problema**, **2-3 opciones con pro/contra**, decisión justificada por el contexto, consecuencias con **gatillo**.
- **O3** — Comprensión: por qué un ADR es **inmutable** y cuándo el spec-first paga vs es burocracia.

## Criterios y niveles

### C1 — Calidad del mini-spec · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | El "spec" repite el issue ("recorta el título") sin entradas/salida/bordes; o describe la implementación en vez del contrato. |
| **en-progreso** | Hay entradas y salida pero sin **restricciones** (solo `str`/`int`), o menos de 3 casos borde, o criterios vagos ("que se vea bien") no falsables. |
| **competente** | Entradas con restricciones (rango de `max_len`, título vacío), salida con **invariante** (`len(resultado) <= max_len`), **≥3 casos borde resueltos a propósito**, criterios de aceptación que se pueden volver tests. |
| **excelente** | Además anticipa un caso que el enunciado no nombró (p. ej. `max_len` menor que la elipsis, o título de una sola palabra larguísima) y deja el spec listo para escribir los tests sin más preguntas. |

### C2 — Calidad del ADR · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay ADR, o es una sola frase ("uso elipsis") sin contexto ni opciones; o "documenta" la decisión sin alternativas. |
| **en-progreso** | Estructura presente pero con **una sola opción** (no hubo trade-off), o decisión sin justificar ("porque sí"), o sin consecuencias/gatillo. |
| **competente** | Contexto/problema claro; **≥2 opciones reales con pro y contra**; decisión **atada al contexto**; consecuencias (+/−) y un **gatillo** observable de revisión. |
| **excelente** | Las opciones son genuinamente distintas (no una de paja); nombra qué se vuelve **más difícil** por la decisión; estado/fecha/decididores presentes; el gatillo es concreto y medible. |

### C3 — Comprensión demostrada · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Trata el ADR como doc editable; o no distingue spec de implementación. |
| **en-progreso** | Entiende el formato pero no puede defender *por qué* es inmutable ni cuándo el spec sobra. |
| **competente** | Articula que el ADR se **supersede, no se edita** (historia), y que el spec **escala con la incertidumbre**, no con el tamaño del código. |
| **excelente** | Da un ejemplo propio de cambio donde el spec formal sería teatro vs uno donde paga; conecta el ADR con la trazabilidad de decisiones de los capstones. |

## Errores típicos a marcar
- **Spec que es implementación disfrazada**: pseudo-código de `acortar_titulo` en vez del contrato (qué entra/sale/borde). El spec define *qué*, no *cómo*.
- **Casos borde "los veré al codear"**: dejar la elipsis-dentro-de-`max_len` o el `max_len=3` sin decidir es exactamente la ambigüedad que el ejercicio pide cerrar.
- **Criterios de aceptación no falsables** ("que se vea bien", "que sea rápido"): no se pueden volver test.
- **ADR con una sola opción**: si no hay alternativas con pro/contra, no hubo decisión, hubo un capricho documentado.
- **Decisión sin gatillo**: un "no hago X ahora" sin el evento que lo reabriría es una decisión a medias.
- **Editar el ADR para "actualizarlo"**: rompe la inmutabilidad; lo correcto es un ADR nuevo que supersede.
- (transversal spec-driven) confundir spec con ADR: el spec es el contrato del comportamiento; el ADR es el registro de una decisión técnica con sus alternativas.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Spec y ADR impecables en forma pero el alumno no puede explicar **por qué** eligió que la elipsis cuente (o no) dentro de `max_len`: la forma vino de fuera, el criterio no.
- ADR con opciones sospechosamente exhaustivas (4-5 alternativas pulidas) impropias de un ejercicio de 40 min, sin que el alumno defienda cuál descartó primero y por qué.
- Jerga ("speculative generality", "YAGNI") en el ADR pero sin poder aplicarla al caso concreto.
- **Verificación sugerida:** pedir que defienda en voz alta un caso borde y el gatillo del ADR; pedir que invente un cambio trivial donde un spec formal sería burocracia. Si no lo razona, no interiorizó el criterio.

## Feedback sugerido (graduado)
> Nunca dar el código/artefacto de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Recorre `acortar_titulo` con `max_len=3` y un título de 100 caracteres: ¿cabe siquiera la elipsis? Esa pregunta sin respuesta es un caso borde que aún no resolviste."
- **Pregunta socrática (nivel 2):** "Si dentro de un año alguien quiere que la elipsis NO cuente dentro de `max_len`, ¿cómo sabrá por qué tú decidiste lo contrario? ¿Dónde vive esa razón?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Tu spec necesita una invariante explícita (`len(resultado) <= max_len`) y los 3 bordes resueltos a propósito. Tu ADR necesita una segunda opción real con su contra, y un gatillo concreto. Repasa las secciones 4.2–4.3 antes de mirar la referencia."

## Conexión con el proyecto / capstone
- Este es el ensayo directo del **[Capstone F2](/fase-2-ingenieria/proyecto/)**: arrancar con un mini-spec y documentar las decisiones (dónde abstraer y dónde no, de `2.4`) en ADRs inmutables dentro de `ARQUITECTURA.md`. El hábito de "spec antes de código, decisión con alternativas" escala a todos los capstones siguientes (su Definition of Done lo exige).
