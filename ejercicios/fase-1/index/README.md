# Fase 1 (entrada) — Diagnóstico de entrada y plan de Fase 1

> **Modalidad: a mano (sin IA).** Este es el ejercicio de *placement* de la fase.
> No se corrige "bien o mal": se corrige por **honestidad y concreción**. Su
> objetivo es que entres a la Fase 1 sabiendo dónde estás parado en **cada una de
> las dos pistas** (Python y TypeScript) y con un plan que de verdad vayas a
> cumplir.

**Fase:** Fase 1 — Lenguajes núcleo · **Lección:** `1.0` Portada de la fase
**Ruta:** crítica · **Timebox:** 30 min

## 🎯 Objetivos

- **O1** — Autoevaluar tu punto de partida real por sub-unidad (1.1–1.10),
  distinguiendo *"lo sé hacer sin notas"* de *"lo reconozco"*, en las dos pistas.
- **O2** — Diseñar un plan de Fase 1 que **alterne** las dos pistas (Python núcleo
  y TypeScript) y **agende** la victoria-IA temprana (1.10), con un ritual de
  *active recall* / *spaced repetition*.
- **O3** — Justificar por escrito por qué el curso exige **dos** lenguajes (el rol
  de Python como puente a IA y el de TypeScript como filtro fullstack) y cuándo
  usarías cada uno.

## 📋 Contexto

Antes de la primera lección, orientarte. La Fase 1 corre en dos pistas que
convergen en el capstone. El error más común es estudiarlas como bloques aislados
(toda Python, luego todo TS) o saltar a "Python avanzado" antes de tener la base.
Sin un diagnóstico honesto, la sobreconfianza ("ya sé Python") o el desánimo ("no
sé nada") te sabotean. Y sin un plan que alterne las pistas y agende tu primera
victoria de IA, el método Primero-Sin-IA se queda en buenas intenciones. Este
ejercicio cierra esos huecos y se conecta directo con el capstone: la disciplina y
el orden que declaras aquí son los que vas a necesitar para escribir la misma app
en dos lenguajes.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox 30 min). No le pidas a una IA que te arme el plan
   ni que te diga "qué nivel tienes": eso lo decides tú.
2. Si quieres referencias para el plan, consulta **documentación oficial** (p. ej.
   técnicas de estudio), no un chat.
3. **Solo al final**, usa IA para que te *corrija* (revise la honestidad y el
   realismo), no para que te lo *escriba*.
4. Mañana, **relee tu plan** y ajústalo si ya se reveló poco realista.

## 🛠️ Instrucciones

Deja **tres archivos markdown en esta carpeta** (`ejercicios/fase-1/index/`):

1. **`diagnostico.md`** — una tabla con las 10 sub-unidades y tu nivel honesto:

   | Sub-unidad | Pista | Nivel (`nuevo` · `lo reconozco` · `lo sé hacer sin notas`) | Por qué (1 línea) |
   |---|---|---|---|
   | 1.1 Python básico | Python | … | … |
   | 1.2 Python intermedio | Python | … | … |
   | … (hasta 1.10) | … | … | … |

   La prueba para marcar **"lo sé hacer sin notas"**: ¿podrías, ahora mismo,
   resolver un ejercicio de ese tema sin notas y sin IA dentro del timebox? Si
   dudas, no lo es.

2. **`plan-fase-1.md`** — tu plan de estudio:
   - bloques semanales **concretos** (día y hora; ej. "Lun/Mié/Vie 20:00–20:45"),
   - cómo vas a **alternar** las dos pistas (no toda Python y luego todo TS),
   - **cuándo** te das la victoria-IA (1.10) como ancla de motivación,
   - tu **ritual de repaso**: cuándo reescribes de memoria lo del día anterior.

3. **`por-que-dos-lenguajes.md`** — en 4–6 frases, con tus palabras: por qué este
   curso pide Python *y* TypeScript, qué rol juega cada uno en tu perfil y en qué
   situación concreta usarías uno u otro.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] La tabla cubre **las 10** sub-unidades (1.1–1.10) con pista, nivel y una razón.
- [ ] El diagnóstico es **defendible**: no está todo en "lo sé hacer" (ni todo en
      "nuevo" si tienes experiencia previa real).
- [ ] El plan tiene **bloques reales en tu semana** (día/hora), no "estudiaré más".
- [ ] El plan **alterna** las dos pistas y **agenda** la victoria-IA (1.10).
- [ ] El plan incluye un **ritual de repaso** explícito (active recall + spacing).
- [ ] El texto de los dos lenguajes nombra el **rol concreto** de cada uno, no
      "porque están de moda".
- [ ] Puedes **explicar tu plan sin notas**.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

No busques el plan "perfecto": busca el **sostenible**. Tres bloques de 40 minutos
que cumples valen más que dos horas diarias que abandonas el jueves. Para alternar
las pistas, dedica la mayor parte a Python (es la pista larga) y reserva al menos
un bloque por semana a TypeScript para que no se enfríe. Agenda la 1.10 (tu primer
LLM) **temprano**, en cuanto cierres 1.5: es la zanahoria que sostiene la
motivación. Para el diagnóstico, vigila la sobreconfianza: si nunca escribiste un
test con `pytest`, 1.6 es `nuevo`, no "lo reconozco". Para los dos lenguajes, ancla
cada rol en algo concreto (Python → IA, APIs, datos; TypeScript → frontend y los
filtros automáticos de las ofertas), no en una frase genérica.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu intento (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-1/index.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

El corrector revisa **honestidad y realismo**, no si "acertaste": no hay una
respuesta única. La **solución de referencia** (`.ai/soluciones/fase-1/index.md`)
es un *exemplar* para el corrector — no la mires antes de intentarlo.
