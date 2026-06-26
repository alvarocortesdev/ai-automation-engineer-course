# Fase 2 (entrada) — Diagnóstico de hábitos y plan de Fase 2

> **Modalidad: a mano (sin IA).** Este es el ejercicio de *placement* de la fase.
> No se corrige "bien o mal": se corrige por **honestidad y concreción**, y por tu
> capacidad de **ver los hábitos que faltan** en un trozo de código —el reflejo
> central de toda la Fase 2.

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.0` Portada de la fase
**Ruta:** crítica · **Timebox:** 35 min

## 🎯 Objetivos

- **O1** — Autoevaluar tu punto de partida real por sub-unidad (2.1–2.13),
  distinguiendo *"lo sé hacer sin notas"* de *"lo reconozco"*.
- **O2** — Diseñar un plan de estudio con bloques semanales concretos, con
  *interleaving* de los problemas de DSA y un ritual de *active recall* /
  *spaced repetition*.
- **O3** — Producir un *gap report*: nombrar los hábitos semi-senior que faltan en
  un trozo de código junior (**sin arreglarlo**) y mapear cada hueco a la
  sub-unidad de la fase que lo cubre.

## 📋 Contexto

La tesis de la Fase 2 es que la calidad no es una fase posterior: es un puñado de
**hábitos diarios** (tests, nombres claros, decisiones documentadas) que un
revisor mira antes de aprobar cualquier PR. La habilidad que abre la fase no es
*arreglar* código, sino **ver** qué le falta. Por eso este diagnóstico mezcla dos
cosas: tu autoevaluación honesta y un primer *gap report* real. La disciplina que
declares aquí es exactamente la que vas a necesitar para el capstone (Refactor +
suite de tests).

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox 35 min). No le pidas a una IA que te arme el plan
   ni que te diga "qué nivel tienes": eso lo decides tú.
2. Si quieres referencias, consulta **documentación oficial** (p. ej. el catálogo
   de *smells* de Fowler), no un chat.
3. **Solo al final**, usa IA para que te *corrija* (revise honestidad, realismo y
   agudeza del *gap report*), no para que te lo *escriba*.
4. Mañana, **relee tu plan** y ajústalo si ya se reveló poco realista.

## 🛠️ Instrucciones

Deja **tres archivos markdown en esta carpeta** (`ejercicios/fase-2/index/`):

1. **`diagnostico.md`** — una tabla con las 13 sub-unidades y tu nivel honesto:

   | Sub-unidad | Nivel (`nuevo` · `lo reconozco` · `lo sé hacer sin notas`) | Por qué (1 línea) |
   |---|---|---|
   | 2.1 DSA nivel trabajo | … | … |
   | 2.2 Clean code | … | … |
   | … (hasta 2.13) | … | … |

   La prueba para marcar **"lo sé hacer sin notas"**: ¿podrías, ahora mismo,
   resolver un ejercicio de ese tema sin notas y sin IA dentro del timebox? Si
   dudas, no lo es.

2. **`plan-fase-2.md`** — tu plan de estudio:
   - bloques semanales **concretos** (día y hora; ej. "Lun/Mié/Vie 20:00–20:45"),
   - cómo vas a **interleave** los problemas de DSA (2.1) con el resto en vez de
     hacerlos todos en un bloque,
   - tu **ritual de repaso**: cuándo reescribes de memoria lo del día anterior.

3. **`habitos-faltantes.md`** — el *gap report*. Parte de esta versión **junior**:

   ```python
   def calc(x, y):
       if y > 100:
           return x - x * 0.1
       elif y > 50:
           return x - x * 0.05
       else:
           return x
   ```

   **Sin reescribirla**, lista los hábitos semi-senior que le faltan y, por cada
   uno, qué sub-unidad de la fase lo cubre. Pistas de lo que un revisor marcaría:
   nombres (`calc`, `x`, `y`), *magic numbers* (`100`, `50`, `0.1`, `0.05`),
   ausencia de tests, casos borde sin cubrir (¿qué pasa con `y == 100`?, ¿con `x`
   negativo?), falta de spec/ADR sobre *por qué* esos umbrales.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] La tabla cubre **las 13** sub-unidades (2.1–2.13) con un nivel y una razón.
- [ ] El diagnóstico es **defendible**: no está todo en "lo sé hacer" (ni todo en
      "nuevo" si tienes experiencia previa real).
- [ ] El plan tiene **bloques reales en tu semana** (día/hora) y dice cómo
      *interleave* DSA, no "estudiaré más".
- [ ] El plan incluye un **ritual de repaso** explícito (active recall + spacing).
- [ ] El *gap report* nombra **≥ 4 hábitos faltantes** distintos y mapea cada uno
      a su sub-unidad.
- [ ] El *gap report* **no reescribe** la función (ver, no resolver).
- [ ] Puedes **explicar tu plan y tu gap report sin notas**.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para el *gap report*, no busques el bug: busca lo que un **revisor** marcaría
antes de aprobar el PR. Hábito por hábito: ¿entiendo qué hace sin leer el cuerpo?
(nombres → 2.2). ¿De dónde salen 100, 50, 0.1? (magic numbers → 2.3). ¿Cómo sé que
el límite es `>` y no `>=`? (no hay test → 2.6–2.9). ¿Por qué esos umbrales?
(no hay ADR → 2.13). Resiste reescribir: nombrar el hueco **es** la habilidad.
Para el plan, sostenible le gana a ambicioso: 3 bloques de 40 min que cumples
valen más que 2 h diarias que abandonas el jueves.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu intento (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-2/index.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

El corrector revisa **honestidad, realismo y agudeza**, no si "acertaste": no hay
una respuesta única. La **solución de referencia** (`.ai/soluciones/fase-2/index.md`)
es un *exemplar* para el corrector — no la mires antes de intentarlo.
