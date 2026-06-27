# Ejercicio 6.7 — Retrieval híbrido: RRF + metadata filtering fail-closed

> **Modalidad: código (Primero-Sin-IA).** Implementas el núcleo del retrieval
> híbrido de un RAG: fusionar un ranking vectorial y uno léxico (BM25) con
> **Reciprocal Rank Fusion**, filtrar por **metadata** con cierre seguro, y
> componer ambos en un top-k. Recibes los dos rankings **ya calculados** (listas de
> `doc_id`), así que los tests corren **offline, sin API key ni modelos** — el foco
> está en la lógica de ingeniería, que es lo que se rompe en producción. Python
> puro, sin numpy, sin IA hasta cerrar tu intento.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.7` RAG a fondo
**Ruta:** crítica · **Timebox:** 45 min

## 🎯 Objetivo

Implementar, en Python puro, las tres piezas del retrieval híbrido:
`rrf_fusion` (fusionar rankings por posición), `filtrar_por_metadata` (control de
acceso fail-closed) y `recuperar_hibrido` (componerlas en un top-k). Es el motor que
pondrás sobre tu vector DB en el Capstone F6.

## 📋 Contexto

Cuando tu **Capstone F6 (Plataforma RAG)** recibe una pregunta, corre **dos**
búsquedas: una vectorial (significado) y una BM25 (palabra clave exacta). Cada una
devuelve un ranking de `doc_id`, pero sus scores **no son comparables** (un coseno de
0.7 y un BM25 de 12.3 no se suman). **RRF** resuelve eso usando solo la **posición**
en cada lista. Y como tu RAG es multi-tenant, antes de responder filtras por
`tenant`/`permisos`: ese filtro es una **frontera de seguridad**, no de relevancia, y
por eso va **fail-closed** (lo que no cumple, no pasa).

## 📏 Primero-Sin-IA

1. **Antes de programar**, escribe en una línea el contrato de cada función: ¿qué
   entra?, ¿qué sale?, ¿qué casos borde hay? (doc en una sola lista, filtro vacío,
   `k_final` mayor que los candidatos, doc al que le falta una clave del filtro).
2. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea lento.
3. Solo entonces consulta la **documentación oficial** de Python (`enumerate`,
   `dict.get`, `sorted` con `key`, `all`).
4. **Solo al final**, usa IA para *revisar y explicar* — nunca para *generar*.
5. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `fusion.py` y completa las tres funciones (no cambies sus firmas).
2. Corre los tests:

   ```bash
   uv run pytest        # recomendado
   # o, si ya tienes pytest:  pytest
   ```

3. Itera hasta que **todos los tests pasen en verde**.
4. Añade al menos **un test borde tuyo** en `test_fusion.py` (ver el TODO al final).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Todos los tests pasan.
- [ ] `rrf_fusion` usa rank **1-based** (`1/(k+1)` para el primer puesto), acumula
      sobre todas las listas, y es **determinista** en empates (`doc_id` ascendente).
- [ ] `filtrar_por_metadata` es **fail-closed**: un doc sin la clave del filtro NO
      pasa; preserva el orden de entrada.
- [ ] `recuperar_hibrido` fusiona, filtra y recorta a `k_final`, devolviendo
      `(doc_id, score)`.
- [ ] Agregaste al menos **un test propio** (caso borde).
- [ ] Puedes **explicar sin notas** por qué RRF usa la posición y no el score, y por
      qué el filtro de seguridad va fail-closed.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para `rrf_fusion`: recorre cada lista con `enumerate(lista, start=1)` para tener el
rank 1-based, y **acumula** `1.0 / (k + rank)` en un `dict` `{doc_id: score}` (un doc
en dos listas suma dos veces). Ordena con
`sorted(puntajes.items(), key=lambda t: (-t[1], t[0]))`: `-t[1]` ordena score
descendente, `t[0]` rompe empates por `doc_id`. El `start=1` no es cosmético: con
`start=0`, el primer puesto sería `1/(k+0)` y cambiarían todos los scores.

Para `filtrar_por_metadata`: por cada candidato, comprueba
`all(metadata.get(d, {}).get(clave) == valor for clave, valor in filtro.items())`.
El `metadata.get(d, {})` y el `.get(clave)` devuelven `None` cuando falta el dato →
no coincide → no pasa (eso ES fail-closed).

Para `recuperar_hibrido`: `rrf_fusion([ranking_vectorial, ranking_bm25])`, quédate
con los `doc_id` que pasan el filtro **en el orden fusionado**, recorta a `k_final`,
y devuelve los pares `(doc_id, score)`.

Repasa "Worked example 2: las tres palancas de calidad" de la lección antes de mirar
la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/fusion-hibrida-rrf/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-6/` — no la mires antes de
intentarlo de verdad.
