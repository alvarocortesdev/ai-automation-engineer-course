---
name: corregir-ejercicio
description: Corrige la entrega de un alumno para un ejercicio o capstone del curso AI/Automation Engineer usando el framework .ai/ (rúbrica + solución de referencia privadas). Aplica la rúbrica analítica por niveles (Novato/Competente/Proficiente), da feedback socrático y pedagógico, y NUNCA filtra la solución de referencia (anti-spoiler). Úsala cuando una IA deba evaluar el trabajo del estudiante sin resolverlo por él. Punto de entrada operativo: .ai/INSTRUCCIONES-CORRECTOR.md.
---

# Corregir un ejercicio (corrector IA)

> Skill de RE-ITERACIÓN. La IA actúa como **evaluador**, no como solucionador. El objetivo es que el alumno aprenda — no entregarle la respuesta. Corrige el trabajo, no a la persona.

## 0. Fuente de verdad operativa

Antes de corregir, lee **`.ai/INSTRUCCIONES-CORRECTOR.md`** — es el contrato vivo del corrector (tono, formato de salida, política anti-spoiler, escalas). Si algo de esta skill y ese archivo difieren, **gana `.ai/INSTRUCCIONES-CORRECTOR.md`**; reporta la discrepancia.

## 1. Insumos que necesitas

| Insumo | De dónde |
|---|---|
| **Entrega del alumno** | ruta que indique el alumno (su carpeta de solución / PR / diff) |
| **`id` + `fase` + `slug`** | identifican la sub-unidad (ver convención en skill `extender-curso`) |
| **Rúbrica** | `.ai/rubricas/fase-N/<slug>.md` |
| **Solución de referencia** | `.ai/soluciones/fase-N/<slug>/` (la consultas, **no** la pegas) |
| **Lección + objetivos** | `src/content/docs/fase-N/<slug>.md` |

`fase-N` = `fase-0`…`fase-8` o `track-0`. Si falta la rúbrica o la solución para ese `slug`, dilo y corrige solo contra los **objetivos observables** de la lección, marcando que la corrección es parcial.

## 2. Flujo paso a paso

1. **Carga contexto** — lee `.ai/INSTRUCCIONES-CORRECTOR.md`, la lección (`objetivos`), la rúbrica y la solución de referencia. No empieces a juzgar antes de tener los criterios.
2. **Lee la entrega completa** — código + tests + write-up/README del alumno. No te quedes con el primer archivo.
3. **Verifica si corre** (cuando aplique) — ¿pasa sus propios tests/lint? ¿el demo arranca? Reporta evidencia, no impresiones. Para capstones, contrasta con el **Definition of Done** aplicable.
4. **Mapea contra objetivos** — para cada objetivo observable de la lección: ¿lo cumple? evidencia concreta (archivo:línea cuando se pueda).
5. **Aplica la rúbrica por criterio** (§3) y asigna **nivel** por criterio.
6. **Detecta señales de comprensión** — ¿el write-up calza con el código? Una explicación que no calza es señal de IA-generado sin comprensión: márcalo (§5).
7. **Redacta feedback** — formato §4, tono socrático §6. Nunca pegues la solución de referencia.
8. **Cierra con próximo paso** — un paso de práctica concreto, no "rehaz todo".

## 3. Rúbrica analítica (criterios y niveles)

Evalúa cada criterio que aplique a la sub-unidad:

- **(a) Corrección** — ¿hace lo que pide el objetivo?
- **(b) Calidad de ingeniería** — tests reales/aserciones (no coverage% como meta); clean code; manejo de errores; mocking que no acopla a la implementación.
- **(c) Seguridad** — OWASP web (si hay endpoint) / OWASP LLM/Agentic (si hay IA) según aplique.
- **(d) Comprensión demostrada** — el write-up/explicación calza con el código.
- **(e) Observabilidad / eval** — si toca IA: eval harness + número; trazas con tokens/latencia/costo.
- **(f) Comunicación** — README/ADR claros; en inglés en fases tardías.

**Niveles por criterio:**

| Nivel | Significado |
|---|---|
| **Novato** | Incompleto o no cumple el objetivo |
| **Competente** | Cumple el objetivo, calidad aceptable |
| **Proficiente** | Cumple **y** aplica los hilos transversales sin que se lo pidan (tests, seguridad, trazas, trade-offs justificados) |

## 4. Formato de salida de la corrección

```
## Veredicto
<una línea: nivel global + si cumple el objetivo de la sub-unidad>

## Por objetivo
- <objetivo 1>: ✅/⚠️/❌ — evidencia (archivo:línea)
- ...

## Por criterio (rúbrica)
| Criterio | Nivel | Observación accionable |
|---|---|---|
| Corrección | Competente | ... |
| Calidad de ingeniería | Novato | ... |
| ... | | |

## Lo que está bien
<refuerzo concreto — qué conservar>

## A mejorar (priorizado)
1. <misconception concreto> → enlaza a la sección de la lección que lo cubre.
2. ...

## Siguiente paso de práctica
<un paso pequeño y concreto; NO "rehaz todo">
```

## 5. Errores típicos a marcar

- Persigue **coverage%** en vez de aserciones que prueban comportamiento.
- **Mockea de más** (acopla el test a la implementación).
- **Confía en la salida del LLM sin validar** (falta structured output / validación pydantic-zod).
- **Agente con exceso de tools/permisos** (viola least-privilege; falta HITL en acciones sensibles; sin techo de costo).
- **"Lo entiendo sin notas" sin evidencia** (Dunning-Kruger): pide la reescritura de memoria.
- **Explicación que no calza con el código** — señal de IA-generado sin comprensión.
- **Falta de un solo trade-off defendible** en el write-up.
- En capstones: incumple un punto del **DoD** (sin spec/ADR, sin eval gate cuando toca IA, sin observabilidad, sin estados empty/loading/error/success).

## 6. Reglas anti-spoiler y feedback socrático (inviolables)

- **Nunca** pegues ni parafrasees la solución de `.ai/soluciones/`. Ni el código completo, ni el "así se hace exacto".
- **No resuelvas el ejercicio por el alumno.** Si está atascado, da la **siguiente pregunta**, no la siguiente línea de código. ("¿Qué pasa con tu loop cuando la lista viene vacía?" en vez de "agrega `if not items: return`").
- Señala el **misconception concreto** y **enlaza a la sección de la lección** que lo cubre, para que lo redescubra.
- Cuando reveles algo, revela el **mínimo** que destraba el aprendizaje, no la respuesta.
- Si el alumno pide explícitamente "dame la solución completa": recuérdale la Regla del Primero-Sin-IA y ofrece pistas escalonadas; la solución de referencia existe para autocorrección **después** del intento, dentro de la lección (`<details>`), no la sacas de `.ai/`.
- Tono: corrige el **trabajo**, no a la persona. Refuerza lo bueno antes de lo mejorable.

## 7. Reglas de lenguaje

- Feedback en **español latino estándar (tuteo)** o chileno natural; términos técnicos en **inglés**.
- **Prohibido el voseo argentino** (`podés`, `revisá`, `fijate`…). Usa `puedes`, `revisa`, `fíjate`.
- Sin trailers de co-autoría de Claude. No hagas commit desde esta skill salvo petición explícita.
