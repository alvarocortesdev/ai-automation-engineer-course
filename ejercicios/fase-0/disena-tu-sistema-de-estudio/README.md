# Ejercicio 0.1 — Diseña tu sistema de estudio

> **Modalidad: a mano (de diseño/razonamiento, sin IA para pensar).** Este es el
> primer entregable del curso. No tiene tests automáticos: lo que se evalúa es la
> **calidad y coherencia de tu razonamiento**, no una salida de programa. El
> objetivo es que salgas con un sistema que puedas _ejecutar todos los días_.

**Fase:** Fase 0 — Fundamentos y autonomía · **Lección:** `0.1` Mentalidad y método de estudio
**Ruta:** crítica · **Timebox:** 35 min

## 🎯 Objetivo

Diseñar tu propio sistema de estudio que integre la **regla del Primero-Sin-IA
escalada por novedad**, **active recall** y **spaced repetition** como ritual
diario, y poder **justificar** cada decisión. Sabrás _hacer_ esto: clasificar una
tarea por novedad y decidir el punto de partida correcto.

## 📋 Contexto

Todo el curso descansa en _cómo_ estudias, no solo en _qué_ estudias. Este
documento (`metodo.md`) es la infraestructura del capstone de la fase (la **CLI
sin IA**) y tu primer documento-spec. Lo vas a releer y ajustar muchas veces.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox 35 min). Está bien que sea imperfecto.
2. Solo entonces consulta la lección o documentación oficial.
3. **Solo al final**, usa IA para _revisar y explicar_ — no para _generar_ tu método.
4. Mañana, **reescribe de memoria** los 4 pasos del Primero-Sin-IA. Si no puedes,
   no lo aprendiste todavía.

## 🛠️ Instrucciones

Copia `plantilla-metodo.md` a `metodo.md` y complétalo con **cuatro** secciones:

1. **Tu protocolo Primero-Sin-IA** — los 4 pasos con _tus_ palabras + la frase de
   una línea que pondrás visible en tu repo.
2. **Tabla de novedad** — para cada una de estas 6 tareas, marca `nuevo` o
   `repaso` **para ti**, la **primera acción** (worked example / faded /
   Primero-Sin-IA) y **una línea de justificación**:
   - (a) usar `git rebase`
   - (b) escribir un `if/else`
   - (c) qué es un embedding
   - (d) sumar dos números en una función
   - (e) desplegar con Docker
   - (f) leer un stack trace
3. **Horario semanal** — bloques fijos (día + hora + duración) + tu **drill
   diario** (1 problema pequeño resuelto a mano antes de tocar el teclado).
4. **Cadencia de spaced repetition** — cuándo reescribes de memoria (mismo día /
   +1 / +3 / +7) y cómo lo registras.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Las 4 secciones están completas y son **tuyas** (no copiadas/genéricas).
- [ ] La tabla **justifica** cada clasificación; al menos una tarea es `repaso` y
      al menos una es `nuevo`, coherente con tu experiencia real.
- [ ] El horario tiene bloques **concretos** (no "cuando pueda") y un drill diario.
- [ ] Puedes **explicar sin notas** por qué el active recall le gana a releer.
- [ ] Guardas `metodo.md` con un commit `docs: add personal study method`
      (tu primer Conventional Commit).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para la tabla de novedad, no busques la etiqueta "correcta": busca **coherencia
con tu historia**. La pregunta es siempre _"¿la he hecho antes con éxito?"_. Si
sí → `repaso` → Primero-Sin-IA de entrada. Si no → `nuevo` → worked example
primero. Lo que se evalúa es la **justificación**, no la etiqueta. Tareas como
_(d) sumar dos números_ suelen ser repaso para casi todos; _(c) embedding_ casi
seguro es nuevo. Las del medio dependen de ti — ahí está el ejercicio.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu asistente de IA:

> "Corrige `ejercicios/fase-0/disena-tu-sistema-de-estudio/` usando el framework
> de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md` al pie de la letra."

Entrégale: tu `metodo.md`, la **rúbrica**
(`.ai/rubricas/fase-0/disena-tu-sistema-de-estudio.md`) y las instrucciones del
corrector. La **solución de referencia** vive en
`.ai/soluciones/fase-0/disena-tu-sistema-de-estudio.md` — no la mires antes de
intentarlo de verdad.
