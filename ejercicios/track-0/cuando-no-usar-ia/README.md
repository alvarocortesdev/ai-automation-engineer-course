# Ejercicio T0.9 — Defiende el cuándo-NO en una entrevista hostil

> **Modalidad: diseño/razonamiento (sin código, sin IA primero).** El momento más incómodo y más decisivo
> de una entrevista 2026 es cuando el reclutador, escéptico, te pregunta si la IA programa por ti. Es una
> trampa con dos salidas malas: "la IA hace todo" (te declaras un pasivo) y "no uso IA" (mientes o suenas
> lento). La salida buena rompe la dicotomía: **diriges y verificas**. Y el músculo más escaso que puedes
> mostrar ahí es saber **cuándo NO** usarla, defendido con un porqué de ingeniería.

**Fase:** Track 0 — Empleabilidad, marca e inglés · **Lección:** `T0.9` Vender el skill AI-augmented
**Ruta:** crítica · **Timebox:** 35 min

## 🎯 Objetivo

- **O1** — Defender en entrevista, **sin sobrevender**, tu uso de IA: romper la falsa dicotomía "o sabes o
  usas IA", anclar en **evidencia** del repo y cerrar conectando con **Primero-Sin-IA**.
- **O2** — Explicar el **trade-off de cuándo NO usar IA**: situaciones concretas, cada una con un **porqué
  de ingeniería** y el **costo** de la decisión.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox 35 min). No le pidas a la IA que te escriba la defensa —practicar
   defenderte tú es justamente el músculo que se evalúa en vivo.
2. Solo entonces relee, si dudaste, el ejemplo resuelto (la entrevista hostil) y el músculo 4 (cuándo-NO)
   de la lección.
3. **Solo al final**, usa IA para *revisar* tu defensa —no para generarla.
4. Mañana, graba tu respuesta hablada en menos de 60 segundos y escúchate: ¿sonaste a vibe-coder, a
   purista, o nombraste el criterio con evidencia?

## 📋 El insumo

Lee `transcripcion-entrevista.md` (en esta carpeta): el fragmento donde el reclutador cuestiona tu uso de
IA. Respóndele como FDE/ingeniero con criterio, no a la defensiva.

## 🛠️ Tu tarea (en `defensa.starter.md`)

1. **Tu respuesta hablada (máx. 8 frases):** que (a) rompa la dicotomía "o sabes o usas IA", (b) ofrezca
   **evidencia** del repo (un spec, unos tests, un ADR, evals), y (c) cierre conectando con
   Primero-Sin-IA. Escríbela como se *dice*, no como un ensayo.
2. **Tu lista cuándo-NO (≥3 situaciones):** dónde NO usarías IA, cada una con su **porqué de ingeniería**
   (no "porque sí" —un costo real: aprendizaje, modelo mental para debugging, código crítico/seguridad,
   costo de revisar mayor que el de escribir).
3. **El trade-off por escrito (de UNA de esas situaciones):** qué **ganas** y qué **pierdes** al NO usar IA
   ahí. Toda decisión cuesta algo; nómbralo.
4. **Una línea anti-sobreventa:** la frase que te **prohíbes** decir (la versión vibe-coder o la versión
   purista) y por qué te hundiría.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] La **respuesta hablada** rompe la dicotomía, **ancla en evidencia** y cierra con Primero-Sin-IA, sin
      sobrevender ni esconder.
- [ ] La **lista cuándo-NO** tiene **≥3** situaciones, cada una con un **porqué de ingeniería** real.
- [ ] El **trade-off** nombra explícitamente qué **ganas** y qué **pierdes**.
- [ ] La **línea anti-sobreventa** identifica una frase autodestructiva concreta y por qué hunde.
- [ ] Puedes **explicar, sin notas, por qué saber cuándo NO usar IA demuestra más criterio que la
      velocidad** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para la respuesta: no te defiendas ni te disculpes —la pregunta asume una falsa dicotomía; tu trabajo es
**romperla**. La estructura que funciona: "las dos cosas, y esa es la habilidad" → evidencia concreta del
repo ("el spec lo escribí yo, los tests también, reviso la salida contra ellos") → cierre con
Primero-Sin-IA ("la uso para multiplicar, no para pensar; por eso puedo defender esto sin la IA al lado").
Para el cuándo-NO: un buen porqué de ingeniería tiene un **costo medible** detrás. "No uso IA cuando
aprendo algo nuevo, porque delegar el pensamiento me deja sin el fundamento para luego verificar su
output" es de ingeniería; "no me gusta usar IA" no lo es. Para el trade-off: si NO usas IA en código de
pagos, ganas control y revisión a fondo, pero pierdes velocidad —el punto es que en pagos ese cambio
**vale la pena**, y saber cuándo vale es el criterio.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/track-0/cuando-no-usar-ia.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/track-0/cuando-no-usar-ia.md` — no la mires antes de
intentarlo. El corrector evaluará tu **criterio** (romper la dicotomía con evidencia + defender el
cuándo-NO con costos reales), no que tu defensa coincida palabra por palabra con un ejemplo.
