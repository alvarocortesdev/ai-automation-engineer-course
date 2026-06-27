---
ejercicio_id: fase-6/eval-harness-a-mano
fase: fase-6
sub_unidad: "6.9"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es una **vara de
> medir**: el alumno debe corregir su trabajo, no recibir este código. Úsala para
> detectar el error y graduar las pistas.

# Solución de referencia — Un eval harness con gate de regresión, a mano

## Respuesta canónica (implementación)

```python
def precision_recall_at_k(recuperados, relevantes, k):
    top_k = recuperados[:k]                                  # truncar al top-k
    hits = sum(1 for c in top_k if c in relevantes)          # intersección
    precision = hits / k                                     # castiga ruido
    recall = hits / len(relevantes) if relevantes else 1.0   # castiga dejar fuera
    return precision, recall


def correr_eval(sistema, dataset, k):
    precisiones, recalls, fallos = [], [], []
    for caso in dataset:
        recuperados = sistema(caso.pregunta)
        p, r = precision_recall_at_k(recuperados, caso.relevantes, k)
        precisiones.append(p)
        recalls.append(r)
        if r < 1.0:                                          # solo los que pierden contexto
            fallos.append({"pregunta": caso.pregunta, "precision": p, "recall": r,
                           "recuperados": recuperados})
    n = len(dataset)
    return {"recall": sum(recalls) / n, "precision": sum(precisiones) / n,
            "n": n, "fallos": fallos}


def gate_de_regresion(resumen, umbral, baseline=None, tolerancia=0.02):
    score = resumen["recall"]
    if score < umbral:                                       # barra absoluta
        return ResultadoGate(False, f"recall {score:.2f} < umbral {umbral}")
    if baseline is not None and score < baseline - tolerancia:  # regresión
        return ResultadoGate(False, f"regresión: {score:.2f} < baseline {baseline:.2f}")
    return ResultadoGate(True, "ok")
```

Verificado contra `test_harness.py`: **8 passed** (Python 3.12, pytest 9.x).

## Razonamiento paso a paso

1. **El denominador lo es todo.** precision y recall comparten el numerador (`hits`, la
   intersección de top-k con relevantes), pero precision divide por `k` (de lo que traje,
   ¿cuánto es señal?) y recall por `len(relevantes)` (de lo que debía traer, ¿cuánto traje?).
   Confundirlos es el error conceptual #1 del ejercicio.
2. **Truncar a `k` antes de contar.** `recuperados[:k]`. Si cuentas hits sobre toda la lista,
   precision y recall salen inflados y el `k` deja de significar nada.
3. **`relevantes` vacío → recall 1.0.** No hay nada que recuperar, así que no se castiga. Sin
   esa guarda, `hits / 0` revienta.
4. **`fallos` guarda los casos con recall < 1.0.** En retrieval, perder un chunk relevante es
   el fallo que no se recupera después (la generación no puede usar lo que no llegó). Un
   harness que solo devuelve el promedio es casi inútil para mejorar: lo accionable es la
   lista de casos malos.
5. **El gate tiene dos chequeos distintos.** El **umbral** es la barra absoluta. El
   **baseline − tolerancia** es la barra relativa: aunque siga sobre el umbral, si bajó
   respecto a la versión en prod, *regresó* y se bloquea. La tolerancia absorbe el ruido del
   LLM no determinista; sin ella, un eval que parpadea entre 0.84 y 0.85 bloquea por nada.

## Predicciones esperadas (`prediccion.md`)

Con `k = 3`:

- **Caso A:** `recuperados=["c1","c2","c3","c4"]`, top-3 = `["c1","c2","c3"]`, `relevantes={"c1","c3"}`.
  hits = 2 → **precision@3 = 2/3 ≈ 0.67**, **recall@3 = 2/2 = 1.0**.
- **Caso B:** `recuperados=["c5","c6","c1"]`, top-3 = `["c5","c6","c1"]`, `relevantes={"c1","c9"}`.
  hits = 1 (solo c1) → **precision@3 = 1/3 ≈ 0.33**, **recall@3 = 1/2 = 0.5**.
  Gate con `umbral=0.8`: recall 0.5 &lt; 0.8 → **NO pasa** (falla la barra absoluta; el baseline
  ni siquiera entra a jugar porque ya falló el umbral).

## Puntos resbalosos (donde el corrector debe mirar)
1. **Denominadores cruzados.** Si precision y recall dan siempre lo mismo, el alumno usó el
   mismo denominador para ambos. Es el error a cazar primero.
2. **Sin truncar a `k`.** Contar sobre toda la lista en vez de `recuperados[:k]`. El test
   `test_k_trunca_la_lista` lo fija (precision=0, recall=0 con k=2).
3. **Gate sin regresión.** Solo `if score < umbral`. Pasa `test_gate_bloquea_por_umbral` pero
   falla `test_gate_bloquea_por_regresion_aunque_supere_umbral`. Es el punto pedagógico del
   ejercicio: el umbral solo no basta.
4. **`fallos` con criterio equivocado.** Guardar por precision < 1.0 (mete demasiados) o no
   guardar nada. El criterio es recall < 1.0.
5. **División por cero** con `relevantes` vacío o `k=0`.

## Rango de soluciones aceptables
- **`sum(1 for c in top_k if c in relevantes)` vs `len(set(top_k) & relevantes)`**: equivalentes
  mientras no haya chunk-ids duplicados en `recuperados` (el contrato asume ids únicos). La
  versión con `set` es prolija; ambas cuentan como `competente`.
- **Gatear sobre `recall` vs sobre una métrica combinada**: el contrato pide recall (la
  métrica crítica de retrieval). Gatear además sobre precision es válido y suma a `excelente`
  si lo justifica; gatear **solo** sobre precision no cumple el objetivo.
- **`fallos` como lista de dicts vs de dataclasses/tuplas**: cualquiera con `pregunta` y
  `recall` accesibles cuenta; el test espera claves de dict, así que respetar el contrato es
  lo limpio.
- Para `verificacion.md`: cualquier texto que (a) ligue recall/precision a teoría de conjuntos
  determinista y faithfulness a un juez (comprensión de texto, no conjuntos), y (b) diga que
  recall alto + faithfulness bajo se arregla en la **generación** (prompt/modelo) no en el
  retrieval, es válido. No se exige redacción concreta.
