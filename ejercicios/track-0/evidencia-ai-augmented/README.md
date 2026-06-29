# Ejercicio T0.9 — Reframe + mapa de evidencia del skill AI-augmented

> **Modalidad: diseño/razonamiento (sin código, sin IA primero).** Sí: vas a escribir *sin IA* un
> ejercicio sobre *vender que usas IA*. Es a propósito —es el músculo Primero-Sin-IA en acción. "Soy bueno
> orquestando IA" es una declaración vacía que cualquiera dice; el skill se **prueba** con evidencia
> abrible, no se **declara** con adjetivos. Aquí entrenas a reframear el discurso y a mapear cada músculo a
> un artefacto concreto.

**Fase:** Track 0 — Empleabilidad, marca e inglés · **Lección:** `T0.9` Vender el skill AI-augmented
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivo

- **O1** — Explicar el framing honesto del skill AI-augmented (multiplicador **con criterio**, no muleta) y
  diagnosticar por qué un framing dado *resta* en una entrevista 2026.
- **O2** — Producir **evidencia concreta y verificable**: mapear cada uno de los **cuatro músculos**
  (spec-driven, agentic+review, evals, cuándo-NO) a un **artefacto abrible** (un commit, un ADR, un
  `spec.md`, un `evals/`).

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox 40 min). No le pidas a la IA que escriba el reframe por ti —sería
   la ironía perfecta de hacer exactamente lo que esta lección te enseña a no hacer.
2. Solo entonces relee, si dudaste, el modelo mental (muleta vs. multiplicador), los cuatro músculos y la
   sección "El mapa de evidencia" de la lección.
3. **Solo al final**, usa IA para *revisar* tu reframe y tu mapa —no para generarlos.
4. Mañana, escribe **un** ADR real en tu repo del curso que documente una decisión de **no** delegar algo a
   la IA. Es el artefacto más escaso del mapa.

## 📋 El insumo

Lee `autodescripcion-junior.md` (en esta carpeta): cómo un candidato describe hoy su relación con la IA.
Tu trabajo NO es burlarte de él, sino diagnosticar el framing y reescribirlo con criterio.

## 🛠️ Tu tarea (en `reframe.starter.md`)

1. **Diagnostica el framing actual:** ¿en qué cuadro cae (purista / vibe-coder / AI-augmented) y por qué
   ese framing le resta en una entrevista 2026?
2. **Reescribe la narrativa** en el framing AI-augmented honesto: 4–6 frases que nombren **el criterio**
   (no la velocidad), aptas para una entrevista o un README de perfil. Cero sobreventa ("10x", "la IA hace
   todo"), cero ocultamiento.
3. **Construye el mapa de evidencia:** una tabla que mapee los **cuatro músculos** a un **artefacto
   concreto y abrible** que probaría cada uno en un repo real tuyo. Si aún no tienes el artefacto, anota
   cuál vas a producir y dónde.
4. **Cierra con una frase honesta** sobre tu músculo **más débil** (el que hoy no podrías demostrar con
   evidencia) y qué harás para tenerla.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] El **diagnóstico** nombra el cuadro y explica por qué resta.
- [ ] La **narrativa reescrita** habla de **criterio** (no de velocidad), sin sobrevender ni ocultar.
- [ ] El **mapa** cubre los **4 músculos**, cada uno con un artefacto **concreto y abrible** (un
      archivo/commit/ADR, no "buen código").
- [ ] La **frase final** identifica con honestidad tu músculo más débil y un plan para la evidencia.
- [ ] Puedes **explicar, sin notas, por qué el skill se prueba y no se declara** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para el diagnóstico: fíjate en los **verbos** del insumo. ¿Dominan "uso / me ahorra / me hace rápido"
(suena a vibe-coder: velocidad sin criterio) o "dirijo / reviso / mido"? Para la narrativa: por cada cosa
que quieras decir, pregúntate "¿esto lo podría verificar un reclutador abriendo mi repo?". Si la frase es
"soy súper productivo con IA", no se puede verificar y suena a humo; si es "escribo el spec y los tests
yo, reviso la salida del agente contra ellos", sí. Para el mapa: un artefacto **abrible** es un archivo o
commit que existe (o existirá) en tu repo —"un `spec.md` commiteado antes del código", "un ADR titulado
'no cacheamos el token en memoria del proceso'", "un `evals/dataset.jsonl` + el gate en el workflow de
CI"— no una cualidad abstracta como "código limpio".

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/track-0/evidencia-ai-augmented.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/track-0/evidencia-ai-augmented.md` — no la mires
antes de intentarlo. El corrector evaluará tu **criterio** (framing honesto + evidencia concreta), no que
tu reframe coincida palabra por palabra con un ejemplo.
