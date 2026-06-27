# Ejercicio 6.0 — Similitud coseno desde cero (y un mini-retriever)

> **Modalidad: código (Primero-Sin-IA).** Implementas a mano la operación que está
> en el corazón de la búsqueda semántica y del RAG. Sin numpy y sin IA hasta cerrar tu intento.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.0` Matemática mínima para IA
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivo

Implementar, en Python puro, `producto_punto`, `magnitud` y `similitud_coseno` entre dos
vectores, y una función `rankear` que ordene documentos por parecido a una consulta —el
mecanismo exacto con el que un retriever decide qué traer.

## 📋 Contexto

Cuando en tu **Capstone F6 (Plataforma RAG)** preguntes algo, el sistema convierte tu
pregunta y cada fragmento en vectores y los compara con similitud coseno para traer los más
relevantes. Si puedes escribir esa comparación a mano, entiendes —y puedes depurar— por qué
tu RAG trae lo que trae. Esto es el cimiento de las sub-unidades 6.5 (Embeddings) y 6.7 (RAG).

## 📏 Primero-Sin-IA

1. **Antes de programar**, escribe el contrato en 3 líneas: ¿qué entra?, ¿qué sale?, ¿qué casos borde hay?
2. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea lento y feo.
3. Solo entonces consulta la **documentación oficial** de Python (`math.sqrt`, listas, `zip`).
4. **Solo al final**, usa IA para *revisar y explicar* — nunca para *generar*.
5. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `similitud.py` y completa las cuatro funciones (no cambies sus firmas).
2. Corre los tests:

   ```bash
   uv run pytest        # recomendado
   # o, si ya tienes pytest:  pytest
   ```

3. Itera hasta que **todos los tests pasen en verde**.
4. Añade al menos **un test borde tuyo** en `test_similitud.py` (ver el TODO al final del archivo).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Todos los tests pasan.
- [ ] `similitud_coseno([7,1],[9,1]) ≈ 0.999` y `similitud_coseno([7,1],[1,9]) ≈ 0.25`.
- [ ] El **vector cero** lanza `ValueError` con mensaje claro en vez de reventar por división por cero.
- [ ] `rankear` devuelve las tuplas `(indice, similitud)` ordenadas de mayor a menor.
- [ ] Agregaste al menos **un test propio**.
- [ ] Puedes **explicar sin notas** por qué usaste coseno y no producto punto (la trampa de la magnitud).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para `producto_punto`, `zip(a, b)` te empareja las coordenadas y `sum(x*y for x, y in zip(a, b))`
hace el trabajo en una línea —pero primero compara largos y lanza `ValueError` si difieren.
Para `magnitud`, `math.sqrt(sum(x*x for x in a))`. En `similitud_coseno`, calcula **primero** las
dos magnitudes y, si alguna es 0, lanza `ValueError` **antes** de dividir. Para `rankear`,
construye una lista de tuplas `(indice, similitud)` y ordénala con `sorted(..., key=lambda t: t[1], reverse=True)`.
Repasa la sección "Idea 3 — Similitud coseno" de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/similitud-coseno-a-mano/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-6/` — no la mires antes de intentarlo de verdad.
