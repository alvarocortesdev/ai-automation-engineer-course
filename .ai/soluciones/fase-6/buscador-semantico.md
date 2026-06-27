---
ejercicio_id: fase-6/buscador-semantico
fase: fase-6
sub_unidad: "6.5"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Buscador semántico desde cero

## Respuesta canónica

```python
import math


def chunk_texto(texto, tam, solape):
    if solape >= tam:
        raise ValueError(f"solape ({solape}) debe ser menor que tam ({tam})")
    palabras = texto.split()
    if not palabras:
        return []
    paso = tam - solape
    chunks = []
    i = 0
    while i < len(palabras):
        chunks.append(" ".join(palabras[i : i + tam]))
        if i + tam >= len(palabras):
            break
        i += paso
    return chunks


def similitud_coseno(a, b):
    producto = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))
    return producto / (mag_a * mag_b)


def buscar(consulta_vec, corpus_vecs, k):
    puntajes = [
        (i, similitud_coseno(consulta_vec, doc)) for i, doc in enumerate(corpus_vecs)
    ]
    puntajes.sort(key=lambda t: t[1], reverse=True)
    return puntajes[:k]


def deduplicar(vecs, umbral):
    conservados = []
    for i, v in enumerate(vecs):
        if all(similitud_coseno(v, vecs[j]) < umbral for j in conservados):
            conservados.append(i)
    return conservados
```

## Razonamiento paso a paso

1. **`chunk_texto`** valida `solape >= tam` **primero** (si no, `paso` sería 0 o
   negativo y el `while` nunca avanzaría → bucle infinito). Divide en palabras,
   avanza `paso = tam - solape` por vuelta tomando `palabras[i : i + tam]`, y corta
   cuando `i + tam` ya cubre el resto. El último chunk queda más corto y es correcto.
   Texto vacío → `[]`; texto ≤ `tam` → un solo chunk (entra al `while` una vez y
   corta en el primer `if`).
2. **`similitud_coseno`** es el de 6.0, reutilizado. Los tests no usan el vector
   cero, así que no hace falta el `ValueError` aquí (en producción sí).
3. **`buscar`** arma `(indice, score)` con `enumerate` (conserva la posición
   original), ordena descendente por el score y recorta a `k`. Si `k` > corpus,
   el slice `[:k]` devuelve todos sin reventar.
4. **`deduplicar`** es greedy: conserva el primero y, para cada candidato, lo agrega
   solo si su coseno contra **todos** los ya conservados es `< umbral`. Comparar
   contra *todos* (no solo el anterior) es lo que evita dejar pasar duplicados de un
   vector más antiguo.

## Verificación numérica (casos de los tests)

- `chunk_texto("uno dos tres cuatro cinco seis", 4, 2)` → paso 2; chunks que
  empiezan en 0 y 2 → `["uno dos tres cuatro", "tres cuatro cinco seis"]`.
- `buscar([1,0], [[1,0],[0,1],[1,1],[-1,0]], 2)`: cosenos 1.0, 0.0, 0.7071, -1.0
  → ordenados → `[(0, 1.0), (2, 0.7071)]`.
- `deduplicar([[1,0],[1,0],[0,1],[1,1]], 0.95)`: v1 tiene coseno 1.0 con v0 (≥0.95,
  descartado); v2 y v3 no llegan a 0.95 contra ningún conservado → `[0, 2, 3]`.

## Puntos resbalosos (donde el corrector debe mirar)

1. **Paso = `tam`** en vez de `tam - solape` (error #1): los chunks no se solapan.
   El test `test_chunk_avanza_tam_menos_solape` lo atrapa.
2. **No validar `solape >= tam`**: el test `test_chunk_solape_mayor_o_igual_que_tam_lanza`
   lo exige; sin la guarda, el código entraría en bucle infinito en producción.
3. **`deduplicar` que compara solo contra el último conservado** en vez de contra
   todos: funciona en los tests pequeños por casualidad, pero es conceptualmente
   incorrecto. Marcarlo aunque pasen los tests.
4. **`>` en lugar de `>=`** en el umbral de `deduplicar`: `test_deduplicar_descarta_casi_iguales`
   usa coseno exactamente 1.0 con umbral 0.95, así que `>` también pasaría ahí; el
   borde real (coseno == umbral) hay que revisarlo en la lógica, no solo en los tests.
5. **`buscar` que no recorta a `k`** o que revienta con `k` > corpus.

## Rango de soluciones aceptables

- Usar `sorted(puntajes, key=lambda t: -t[1])` en vez de `reverse=True` es equivalente.
- `math.hypot(*a)` para la magnitud es **excelente** (norma euclidiana exacta, evita overflow).
- Un `chunk_texto` que recorre con `range(0, len(palabras), paso)` y rompe cuando el
  chunk repetiría es aceptable si maneja los mismos bordes.
- `numpy` (`np.dot`, `np.linalg.norm`, `np.argsort`) da el resultado correcto pero
  **contradice el enunciado** ("Python puro, a mano"): pedir la versión a mano.
- `deduplicar` que devuelve los **vectores** en vez de los **índices** no pasa los
  tests tal como están escritos; si el alumno cambió la firma, marcarlo (el contrato
  pide índices) pero reconocer si la lógica greedy es correcta.
