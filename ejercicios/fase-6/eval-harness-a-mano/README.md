# Ejercicio 6.9 — Un eval harness con gate de regresión, a mano

> **Modalidad: código (sin IA para resolver).** Construyes las cuatro piezas de un eval
> harness: **dataset → scorer → agregación → gate**. Todo **determinista, sin API ni API
> key** — el "sistema" (el retriever) se te **inyecta** como una función. Si entiendes este
> esqueleto, entiendes ragas y DeepEval: solo te dan scorers más listos sobre el mismo molde.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.9` Eval-driven development
**Ruta:** crítica · **Timebox:** 45 min

## 🎯 Objetivo

Implementar las métricas de **retrieval** de un RAG y el gate que las usa:

1. `precision_recall_at_k(recuperados, relevantes, k)` — precision@k y recall@k (teoría de
   conjuntos, determinista).
2. `correr_eval(sistema, dataset, k)` — corre el retriever sobre el golden set, agrega
   recall/precision medios y **guarda los casos malos** (no solo el promedio).
3. `gate_de_regresion(resumen, umbral, baseline, tolerancia)` — bloquea si no llega al
   umbral **o** si **regresó** respecto al baseline.

## 📋 Contexto

Un RAG falla en dos mitades. Aquí mides la de **recuperación** (¿trajo los chunks
correctos?), que es **determinista**: no necesitas un LLM juez, solo conjuntos. `recall@k`
castiga dejar fuera lo necesario; `precision@k` castiga traer ruido. El `gate_de_regresion`
es lo que convierte el número en una decisión de ship: es el corazón del eval-*driven*
development y un entregable de primera clase del capstone de la fase.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea feo y lento.
2. Solo entonces, consulta la **documentación oficial** (ragas: context precision/recall).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ El contrato (lo que ya está en `harness.py`)

- `CasoRAG`: dataclass con `pregunta: str` y `relevantes: set[str]` (los chunk-ids correctos).
- `ResultadoGate`: dataclass con `pasa: bool` y `razon: str`.
- Las tres funciones a completar, con su firma y docstring.

El **sistema** que evalúas es una función `pregunta -> list[str]`: recibe la pregunta y
devuelve la lista de chunk-ids recuperados **en orden** (el primero es el mejor rankeado).
Se inyecta para que puedas probar con un retriever falso, sin API.

Reglas de cada función:

- **`precision_recall_at_k(recuperados, relevantes, k)`** → `(precision, recall)`:
  - considera solo los **primeros k** de `recuperados`;
  - `hits` = cuántos de esos k están en `relevantes`;
  - `precision = hits / k`;
  - `recall = hits / len(relevantes)`, y **`1.0` si `relevantes` está vacío** (no hay nada
    que recuperar, no se castiga).
- **`correr_eval(sistema, dataset, k)`** → `dict` con `recall`, `precision` (medias sobre el
  dataset), `n` (número de casos) y `fallos`: lista con los casos donde **`recall < 1.0`**
  (se dejó fuera un chunk relevante) — cada fallo es un dict con `pregunta`, `precision`,
  `recall` y `recuperados`.
- **`gate_de_regresion(resumen, umbral, baseline=None, tolerancia=0.02)`** → `ResultadoGate`:
  gatea sobre **`resumen["recall"]`** (en retrieval, perder un chunk no se recupera después).
  - si `recall < umbral` → no pasa (barra absoluta);
  - si `baseline is not None` y `recall < baseline - tolerancia` → no pasa (**regresión**);
  - si no, pasa.

## 🧩 Instrucciones

1. Abre `harness.py` y completa las tres funciones.
2. Corre los tests:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

3. Itera hasta que **los tests pasen en verde**.
4. Añade al menos **un test propio** (idea: `k` mayor que la cantidad de chunks recuperados;
   o un golden con dos chunks relevantes de los que solo se recupera uno).

## 📦 Qué entregar (deja estos archivos en esta carpeta)

- `prediccion.md` — para los 2 casos de abajo, calcula a mano precision@k y recall@k
  (cuenta los conjuntos) y di si el gate pasa. **Escríbelo ANTES de ejecutar.**
- `harness.py` — tu implementación (tests en verde).
- `verificacion.md` — 2-3 frases: por qué recall y precision del retrieval se miden **sin
  LLM** pero faithfulness de la generación **no**; y qué arreglarías si recall sube pero
  faithfulness baja.

Los 2 casos a calcular en `prediccion.md` (con `k = 3`):
- **A:** `recuperados = ["c1", "c2", "c3", "c4"]`, `relevantes = {"c1", "c3"}`.
- **B:** `recuperados = ["c5", "c6", "c1"]`, `relevantes = {"c1", "c9"}`. ¿Pasa el gate con
  `umbral = 0.8`, `baseline = 0.9`, `tolerancia = 0.02` evaluando solo el caso B?

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `prediccion.md` existe **antes** de ejecutar, con los conjuntos contados a mano.
- [ ] Todos los tests pasan (`pytest`).
- [ ] El gate bloquea por **regresión** aunque el `recall` supere el umbral absoluto.
- [ ] El resumen incluye la **lista de casos malos** (`fallos`), no solo el promedio.
- [ ] Agregaste al menos un test propio.
- [ ] `verificacion.md` distingue qué métricas son deterministas y cuál necesita un juez.
- [ ] Puedes **explicar precision@k vs recall@k sin notas** (qué cambia en el denominador).

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/eval-harness-a-mano/` usando el framework de `.ai/`. Sigue
> `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-6/` — no la mires antes de
intentarlo de verdad.
