# Ejercicio 6.0b — Defiende tus fundamentos (modo entrevista)

> **Modalidad: a mano (razonamiento + comunicación, sin IA).** Este ejercicio no tiene tests automáticos: lo que se evalúa es si puedes **explicar y diagnosticar** los fundamentos de ML/DL como lo harías frente a un entrevistador. La meta de toda la sub-unidad 6.0b es que *"explícame attention / qué es un embedding de verdad"* **no te tumbe**.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.0b` Puente ML/DL/transformers
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivo

- **O1** — Explicar, en tus palabras, qué es un modelo, la diferencia entre **entrenar** e **inferir**, y de dónde salen los embeddings (vectores **aprendidos**).
- **O2** — Diagnosticar **overfitting vs underfitting** a partir de números de train/test y justificar por qué se separan los datos.
- **O3** — Explicar la intuición de **self-attention** con un ejemplo de ambigüedad propio.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo, a mano** (timebox 40 min). Sin copiar la lección, sin IA. Está bien que sea lento.
2. Solo entonces, consulta la documentación oficial (paper de transformers, Google ML Crash Course).
3. **Solo al final**, usa IA para *revisar y repreguntarte* — no para *redactar por ti*.
4. Mañana, **reescribe de memoria** la tabla entrenar/inferir y el diagnóstico. Si no salen, no lo aprendiste todavía.

## 🛠️ Instrucciones

Hay starters en esta carpeta. Complétalos **con tus propias palabras y ejemplos** (no los de la lección).

### Parte A — Explica (en `respuestas.md`)

Cada concepto en 2–4 frases, con un ejemplo o analogía **propio**:

1. Qué es un **modelo** (y por qué no es una base de datos de respuestas).
2. **Entrenar vs inferir**, y qué haces tú cuando llamas a una API de LLM.
3. Qué es una **red neuronal**, conectándola con el **producto punto** de 6.0.
4. Qué es **overfitting** y **por qué** se separan train y test.
5. La intuición de **attention** (con un ejemplo de ambigüedad propio, NO el del trofeo).
6. **De dónde salen los embeddings** y por qué no se pueden mezclar embeddings de dos modelos.

### Parte B — Diagnostica (en `diagnostico.md`)

Tres modelos con estos números:

| Modelo | Train | Test |
|---|---|---|
| A | 99% | 72% |
| B | 70% | 68% |
| C | 94% | 91% |

Para cada uno: nombra el diagnóstico (overfitting / underfitting / sano), justifícalo **mirando el gap** (train − test) en una frase, y di qué harías (o no harías).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Las 6 explicaciones están en tus palabras, con un ejemplo/analogía **propio** cada una.
- [ ] Entrenar/inferir deja claro que en inferencia **los pesos NO cambian**.
- [ ] La de embeddings dice que son **vectores aprendidos** (salida de un modelo), no una propiedad del texto.
- [ ] La de attention menciona **al menos una** de sus dos ventajas (larga distancia / paralelización) y trae un ejemplo de ambigüedad tuyo.
- [ ] El diagnóstico de A, B y C es correcto y **justificado por el gap**, no adivinado.
- [ ] Puedes **leer tus respuestas en voz alta sin trabarte** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Ataca primero el par **entrenar/inferir**: si queda nítido, los otros cinco se ordenan solos (un embedding es un peso ajustado *al entrenar*; overfitting es un riesgo *del entrenamiento*; en inferencia nada cambia). Para attention, cualquier frase donde una palabra dependa de otra lejana sirve (pronombres y referentes). Para la Parte B, calcula el **gap** antes de etiquetar: gap grande + train alto = overfitting; ambos bajos = underfitting; ambos altos y cercanos = sano.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (`respuestas.md` y `diagnostico.md` de este directorio),
- la **rúbrica**: `.ai/rubricas/fase-6/puente-ml-dl.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

> "Corrige `ejercicios/fase-6/puente-ml-dl/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md` al pie de la letra."

La **solución de referencia** vive en `.ai/soluciones/fase-6/puente-ml-dl.md` — no la mires antes de intentarlo de verdad. El corrector revisa tu **comprensión demostrada**, no si coincides palabra por palabra.
