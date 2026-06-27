---
ejercicio_id: fase-6/recall-y-filtrado
fase: fase-6
sub_unidad: "6.6"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Recall + filtrado por metadata

## Respuesta canónica

```python
import math


def similitud_coseno(a, b):
    producto = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))
    return producto / (mag_a * mag_b)


def buscar_exacto(consulta, corpus, k):
    puntajes = [
        (i, similitud_coseno(consulta, doc)) for i, doc in enumerate(corpus)
    ]
    puntajes.sort(key=lambda t: t[1], reverse=True)
    return puntajes[:k]


def recall_at_k(ids_aprox, ids_exactos):
    if not ids_exactos:
        return 1.0  # nada que encontrar -> no hay división por cero
    encontrados = set(ids_aprox) & set(ids_exactos)
    return len(encontrados) / len(ids_exactos)


def buscar_con_filtro(consulta, corpus, metadatas, where, k, modo):
    def cumple(meta):
        return all(meta.get(clave) == valor for clave, valor in where.items())

    if modo == "pre":
        # Filtra el corpus ANTES de rankear; conserva el índice original.
        candidatos = [
            (i, similitud_coseno(consulta, corpus[i]))
            for i in range(len(corpus))
            if cumple(metadatas[i])
        ]
        candidatos.sort(key=lambda t: t[1], reverse=True)
        return candidatos[:k]

    if modo == "post":
        # Rankea TODO, recorta a k, y RECIÉN ahí descarta los que no cumplen.
        topk = buscar_exacto(consulta, corpus, k)
        return [(i, s) for (i, s) in topk if cumple(metadatas[i])]

    raise ValueError(f"modo desconocido: {modo!r}")
```

## Razonamiento paso a paso

1. **`similitud_coseno`** es el de 6.0/6.5, reutilizado.
2. **`buscar_exacto`** es el ground truth: arma `(indice, score)` con `enumerate`
   (conserva la posición original), ordena descendente y recorta a `k`. Slice `[:k]`
   con `k` > corpus devuelve todos sin reventar.
3. **`recall_at_k`** = |intersección| / |ground truth|. El **denominador es
   `len(ids_exactos)`** (no `ids_aprox`): eso es lo que distingue *recall* de
   *precision*. El guard `if not ids_exactos: return 1.0` evita el `ZeroDivisionError`.
4. **`buscar_con_filtro`** demuestra el bug del post-filter por el **orden de dos
   pasos**:
   - `"pre"`: filtra el corpus (solo índices cuya metadata cumple `where`), rankea esos
     y devuelve hasta `k`. Siempre da los `k` mejores que cumplen, si existen.
   - `"post"`: toma el top-k **global** y luego descarta los que no cumplen → puede
     devolver **menos** de `k`. Ese es el bug que el alumno debe poder explicar.
   - En ambos, el índice devuelto es la **posición original** en `corpus`.

## Verificación numérica (casos de los tests)

- `recall_at_k([0,2,7], [0,2,5])` → intersección {0,2} → 2/3 ≈ 0.667.
- `recall_at_k([1,2], [])` → ground truth vacío → 1.0.
- `buscar_con_filtro([1,0], CORPUS, METADATAS, {"categoria":"tech"}, 2, "pre")`:
  tech = {idx0 (cos 1.0), idx3 (cos -1.0)} → `[(0,1.0),(3,-1.0)]`.
- `... modo="post"`: top-2 global = [idx0 (1.0), idx2 (0.707)]; idx2 es 'gatos' y cae →
  `[(0,1.0)]` (¡len 1, menos de k!).

## Puntos resbalosos (donde el corrector debe mirar)

1. **Denominador de recall**: usar `len(ids_aprox)` da *precision*, no *recall*.
   `test_recall_parcial` lo atrapa solo si `ids_aprox` y `ids_exactos` tienen tamaños
   distintos — aquí ambos son de tamaño 3, así que **el test no lo distingue del todo**:
   revisar el código, no solo el verde. (`[0,2,7]` vs `[0,2,5]`: precision = recall =
   2/3 por casualidad. Marcar si el alumno usó el denominador equivocado.)
2. **Post-filter que filtra antes**: pasaría `test_prefilter_*` pero no demuestra el bug;
   `test_postfilter_puede_devolver_menos_de_k` lo expone (devolvería 2 en vez de 1).
3. **Perder el índice original**: devolver la posición dentro del subconjunto filtrado en
   `"pre"`. Los tests usan índices que coinciden a veces; revisar la lógica.
4. **`where` de una sola clave hardcodeada**: funciona en los tests (una clave) pero es
   frágil; la versión con `all(...)` es la correcta.

## Rango de soluciones aceptables

- `sorted(..., key=lambda t: -t[1])` en vez de `reverse=True` es equivalente.
- Usar `frozenset`/`set.intersection` para el recall es igual de válido.
- Un `"post"` que primero rankea todo el corpus completo y luego corta a `k` y filtra es
  aceptable **solo si** el recorte a `k` ocurre **antes** del filtro (si filtra antes de
  cortar, es pre disfrazado y no reproduce el bug).
- `numpy` da el resultado correcto pero **contradice el enunciado** ("Python puro, a
  mano"): pedir la versión a mano.
