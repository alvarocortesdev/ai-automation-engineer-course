# Ejercicio 6.5 — Buscador semántico desde cero (chunking + ranking + dedup)

> **Modalidad: código (Primero-Sin-IA).** Implementas el motor de una búsqueda
> semántica: la lógica de ingeniería que rodea al embedding. Recibes los vectores
> ya calculados, así que los tests corren **offline, sin API key y sin descargar
> modelos** — el foco está en que entiendas y puedas escribir el chunking, el
> ranking por coseno y la deduplicación. Sin numpy y sin IA hasta cerrar tu intento.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.5` Embeddings y búsqueda semántica
**Ruta:** crítica · **Timebox:** 45 min

## 🎯 Objetivo

Implementar, en Python puro, las cuatro piezas de una búsqueda semántica:
`chunk_texto` (partir un documento con solape), `similitud_coseno` (reúsalo de 6.0),
`buscar` (top-k por coseno) y `deduplicar` (quitar casi-duplicados). Es el motor que
después pondrás sobre una vector DB en el Capstone F6.

## 📋 Contexto

Cuando tu **Capstone F6 (Plataforma RAG)** ingiere documentos, los parte en chunks,
los embebe y los busca por coseno. Una vector database hará la búsqueda rápida sobre
millones de vectores, pero la **lógica** (cómo cortas, cómo rankeas, cómo limpias
duplicados) es tuya y es lo que se rompe en producción cuando "el RAG trae basura".
Si puedes escribir este motor a mano, puedes depurarlo.

## 📏 Primero-Sin-IA

1. **Antes de programar**, escribe el contrato de cada función en una línea: ¿qué
   entra?, ¿qué sale?, ¿qué casos borde hay? (texto vacío, `solape >= tam`, `k`
   mayor que el corpus).
2. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea lento y feo.
3. Solo entonces consulta la **documentación oficial** de Python (`str.split`,
   `list slicing`, `sorted` con `key`, `math.sqrt`).
4. **Solo al final**, usa IA para *revisar y explicar* — nunca para *generar*.
5. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `buscador.py` y completa las cuatro funciones (no cambies sus firmas).
2. Corre los tests:

   ```bash
   uv run pytest        # recomendado
   # o, si ya tienes pytest:  pytest
   ```

3. Itera hasta que **todos los tests pasen en verde**.
4. Añade al menos **un test borde tuyo** en `test_buscador.py` (ver el TODO al final).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Todos los tests pasan.
- [ ] `chunk_texto` avanza `tam - solape` por chunk, maneja texto corto/vacío y
      lanza `ValueError` si `solape >= tam`.
- [ ] `buscar` devuelve tuplas `(indice, score)` de mayor a menor, recortadas a `k`.
- [ ] `deduplicar` aplica la estrategia greedy (conserva el primero, descarta lo
      casi-igual a algo ya conservado).
- [ ] Agregaste al menos **un test propio** (caso borde).
- [ ] Puedes **explicar sin notas** por qué el solape importa y por qué el texto
      original del chunk se guarda como metadata, aparte del vector.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para `chunk_texto`: usa `texto.split()` para obtener las palabras, valida
`solape >= tam` **antes** del bucle (si no, `paso = tam - solape` sería 0 o negativo
→ bucle infinito), y avanza con un índice `i` que suma `paso` cada vuelta tomando
`palabras[i : i + tam]`. Corta cuando `i + tam >= len(palabras)`.

Para `buscar`: arma `[(i, similitud_coseno(consulta_vec, v)) for i, v in enumerate(corpus_vecs)]`
y ordena con `sorted(..., key=lambda t: t[1], reverse=True)`, luego `[:k]`.

Para `deduplicar`: lleva una lista `conservados` de índices; agrega `i` solo si
`similitud_coseno(vecs[i], vecs[j]) < umbral` para **todo** `j` ya conservado.

Repasa "El otro 70% del trabajo: chunking" de la lección antes de mirar la solución
de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/buscador-semantico/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-6/` — no la mires antes
de intentarlo de verdad.
