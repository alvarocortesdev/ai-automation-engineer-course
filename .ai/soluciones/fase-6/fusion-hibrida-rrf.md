---
ejercicio_id: fase-6/fusion-hibrida-rrf
fase: fase-6
sub_unidad: "6.7"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Retrieval híbrido: RRF + metadata filtering

## Respuesta canónica

```python
def rrf_fusion(listas_ranqueadas, k=60):
    puntajes = {}
    for lista in listas_ranqueadas:
        for posicion, doc_id in enumerate(lista, start=1):   # rank 1-based
            puntajes[doc_id] = puntajes.get(doc_id, 0.0) + 1.0 / (k + posicion)
    # tie-break determinista: score descendente, doc_id ascendente
    return sorted(puntajes.items(), key=lambda t: (-t[1], t[0]))


def filtrar_por_metadata(doc_ids, metadata, filtro):
    return [
        d for d in doc_ids
        if all(metadata.get(d, {}).get(clave) == valor
               for clave, valor in filtro.items())
    ]


def recuperar_hibrido(ranking_vectorial, ranking_bm25, metadata, filtro, k_final):
    fusion = rrf_fusion([ranking_vectorial, ranking_bm25])
    ids_ok = set(filtrar_por_metadata([d for d, _ in fusion], metadata, filtro))
    filtrado = [(d, s) for d, s in fusion if d in ids_ok]
    return filtrado[:k_final]
```

## Razonamiento paso a paso

1. **`rrf_fusion`** ignora los scores originales (un coseno y un BM25 no son
   comparables) y usa solo la **posición**. `enumerate(lista, start=1)` da el rank
   1-based: el primer puesto vale `1/(k+1)`, no `1/(k+0)`. Se **acumula** en un dict,
   así un doc que aparece en varias listas suma su aporte de cada una. El `sorted` con
   `key=lambda t: (-t[1], t[0])` ordena por score descendente y rompe empates por
   `doc_id` ascendente — eso hace el resultado **determinista** y por tanto testeable.
2. **`filtrar_por_metadata`** es **fail-closed** gracias a los dos `.get` encadenados:
   `metadata.get(d, {})` devuelve `{}` si el doc no está; `.get(clave)` devuelve
   `None` si falta la clave. En ambos casos `None == valor` es `False` → el doc **no
   pasa**. `all(...)` exige **todas** las claves del filtro; con filtro vacío, `all`
   sobre un iterable vacío es `True` → pasa todo. Se preserva el orden de entrada.
3. **`recuperar_hibrido`** **compone** (no reimplementa): fusiona, filtra sobre el
   orden fusionado, conserva los pares `(doc_id, score)` y recorta a `k_final`. El
   slice `[:k_final]` devuelve todos si quedan menos.

## Verificación numérica (casos de los tests)

- `rrf_fusion([["a","b"]], k=1)`: a = 1/(1+1) = **0.5**, b = 1/(1+2) = **0.333**.
- `rrf_fusion([["a","b","c"],["b","c","a"]])` (k=60):
  a = 1/61+1/63 = 0.032266, b = 1/62+1/61 = **0.032522**, c = 1/63+1/62 = 0.032002
  → orden `["b","a","c"]`.
- `rrf_fusion([["x"],["y"]])`: x = 1/61, y = 1/61 (empate) → tie-break por id →
  `["x","y"]`.
- `recuperar_hibrido(["d1","d2","d3"], ["d2","d4","d1"], meta, {"tenant":"A"}, 2)`:
  fusión = d2(0.032522) > d1(0.032266) > d4(0.016129) > d3(0.015873); filtro saca a
  d3 (tenant B); top-2 = `[("d2", 0.032522), ("d1", 0.032266)]`.

## Puntos resbalosos (donde el corrector debe mirar)

1. **Sumar scores originales** en vez de RRF: el error conceptual central. Marcar
   aunque el alumno no tenga scores que sumar (recibe solo posiciones) — si intenta
   "inventar" un score por posición distinto de `1/(k+rank)`, revisar.
2. **Rank 0-based**: `test_rrf_primer_puesto_usa_rank_1_based` lo atrapa (esperaría
   0.5 con k=1 y daría 1.0).
3. **Filtro fail-open**: el bug de seguridad. Comparar contra
   `test_filtrar_es_fail_closed_si_falta_la_clave` y `..._si_el_doc_no_esta_en_metadata`.
   Una implementación que asume que la clave existe revienta o deja pasar de más.
4. **No determinismo**: si no rompe empates, `test_rrf_empate...` falla de forma
   intermitente. El alumno debe entender *por qué* importa, no solo parchar.
5. **`recuperar_hibrido` que pierde el score** (devuelve solo ids) o que filtra antes
   de fusionar de un modo que altera el resultado.

## Rango de soluciones aceptables

- `collections.defaultdict(float)` en vez de `dict.get(..., 0.0)` es equivalente y
  limpio.
- `sorted(..., key=lambda t: t[1], reverse=True)` **sin** tie-break secundario NO es
  aceptable: el orden de empates queda indefinido y rompe el determinismo. Marcar.
- Filtrar **antes** de fusionar (sobre cada ranking de entrada) y luego fusionar es
  aceptable y a veces preferible en producción (menos cómputo), siempre que el
  resultado y el score coincidan; con estas entradas da el mismo orden. Reconocerlo
  como válido si el alumno lo justifica.
- Pre-filtrar a nivel de la vector DB (no en Python) es la respuesta de producción
  por costo; si el alumno lo menciona en su write-up, es señal de **excelente**.
- `numpy`/`pandas` da el resultado pero **contradice el enunciado** ("Python puro, a
  mano"): pedir la versión a mano.
