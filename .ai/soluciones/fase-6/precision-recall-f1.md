---
ejercicio_id: fase-6/precision-recall-f1
fase: fase-6
sub_unidad: "6.0"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Precision, recall y F1 desde cero

## Respuesta canónica

```python
def contar(y_true, y_pred):
    if len(y_true) != len(y_pred):
        raise ValueError(f"Listas de distinto largo: {len(y_true)} vs {len(y_pred)}")
    tp = fp = fn = 0
    for real, pred in zip(y_true, y_pred):
        if pred == 1 and real == 1:
            tp += 1
        elif pred == 1 and real == 0:
            fp += 1
        elif pred == 0 and real == 1:
            fn += 1
        # (real == 0 and pred == 0) es TN: no se usa para estas métricas.
    return tp, fp, fn


def precision(tp, fp):
    denom = tp + fp
    return tp / denom if denom else 0.0


def recall(tp, fn):
    denom = tp + fn
    return tp / denom if denom else 0.0


def f1(p, r):
    denom = p + r
    return 2 * p * r / denom if denom else 0.0


def evaluar(y_true, y_pred):
    tp, fp, fn = contar(y_true, y_pred)
    p = precision(tp, fp)
    r = recall(tp, fn)
    return {"precision": p, "recall": r, "f1": f1(p, r)}
```

## Razonamiento paso a paso

1. **`contar`** valida largos y recorre los pares `(real, pred)`. Solo tres de los cuatro cuadrantes
   importan (TP, FP, FN); el TN no entra en precision/recall.
2. **El patrón del caso borde es el mismo en las tres métricas:** `numerador / denominador if denominador else 0.0`.
   Esto evita `ZeroDivisionError` cuando el modelo no predice positivos (precision), no hay positivos
   reales (recall), o ambas métricas son 0 (f1).
3. **`f1` es la media armónica**, no la aritmética. Con `p=1.0, r=0.0` da `2·1·0/(1+0) = 0`, no 0.5:
   castiga correctamente al modelo que acierta lo poco que predice pero se pierde todo lo demás.
4. **`evaluar`** compone: cuenta una vez, deriva precision y recall, y pasa esos a `f1` (no recalcula).

## Verificación numérica

- Ejemplo RAG (TP=6, FP=4, FN=2): `precision = 6/10 = 0.60`, `recall = 6/8 = 0.75`,
  `f1 = 2·0.60·0.75/1.35 = 0.90/1.35 ≈ 0.667`.
- `contar([1,1,0,1,0,0], [1,0,0,1,1,0])` → `(2, 1, 1)`.
- `evaluar([1,1,1,0,0], [1,1,0,0,0])` → TP=2, FP=0, FN=1 → `{"precision": 1.0, "recall": 0.6667, "f1": 0.8}`.

## Puntos resbalosos (donde el corrector debe mirar)

1. **FP y FN intercambiados** en `contar` (error #1): el conteo del caso base lo delata (debe ser 2,1,1).
2. **Fórmulas cruzadas**: precision con FN o recall con FP.
3. **División por cero sin proteger**: `precision(0,0)` debe ser `0.0`, no excepción.
4. **F1 como `(p+r)/2`**: parece pasar casos "normales" pero falla `f1(1.0, 0.0)` (daría 0.5 en vez de 0.0).
5. **`evaluar` que recalcula a mano** en vez de reusar las funciones: funciona pero es la diferencia
   competente vs excelente.

## Rango de soluciones aceptables

- Contar con sumas vectorizadas en Python puro
  (`tp = sum(1 for r, p in zip(y_true, y_pred) if r == 1 and p == 1)`, etc.) es **excelente**: claro y
  conciso.
- Tratar etiquetas booleanas `True/False` además de `1/0` es un extra válido si los tests siguen pasando.
- Redondear los resultados (p. ej. `round(p, 4)`) es aceptable mientras `pytest.approx` siga pasando;
  no es necesario.
- `from sklearn.metrics import precision_score, ...` da el resultado correcto pero **contradice el
  enunciado** (a mano, sin librerías de ML): no cuenta como haber hecho el ejercicio; pedir la versión propia.
- Mensajes de error con otra redacción son válidos mientras nombren el problema (distinto largo).
