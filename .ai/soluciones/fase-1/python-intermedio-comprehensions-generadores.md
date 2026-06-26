---
ejercicio_id: fase-1/python-intermedio-comprehensions-generadores
fase: fase-1
sub_unidad: "1.2"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Procesar transacciones con comprehensions y un generador

## Respuesta canónica

```python
from collections.abc import Iterator


def categorias_unicas(transacciones: list[dict]) -> set[str]:
    return {t["categoria"] for t in transacciones}


def indexar_por_id(transacciones: list[dict]) -> dict[int, dict]:
    return {t["id"]: t for t in transacciones}


def stream_montos(transacciones: list[dict], minimo: float) -> Iterator[float]:
    for t in transacciones:
        if t["monto"] >= minimo:
            yield t["monto"]
```

## Razonamiento paso a paso
1. **`categorias_unicas` — set comprehension.** `{t["categoria"] for t in transacciones}`. El `set`
   elimina duplicados gratis (categorías repetidas colapsan). La lista vacía devuelve `set()` sin
   ningún caso especial, porque no hay nada que iterar.
2. **`indexar_por_id` — dict comprehension.** `{t["id"]: t for t in transacciones}`. Indexar por una
   clave permite buscar una transacción por su `id` en tiempo constante en vez de recorrer la lista.
   La lista vacía devuelve `{}`.
3. **`stream_montos` — generador.** El `yield` es lo que lo hace generador: la función **no construye
   ninguna lista**; produce un monto, se pausa, y reanuda cuando le piden el siguiente. Respeta el
   orden de entrada porque recorre con un `for` simple. La lista vacía no produce nada (el `for` no
   itera). El filtro `>= minimo` incluye el valor límite.

## Puntos resbalosos (donde el corrector debe mirar)
1. **`stream_montos` con `return [...]`**: es lo más común. Pasa a ojo pero falla
   `test_stream_montos_es_un_generador` (`inspect.isgenerator`). El contrato pide `yield`.
2. **Comprehension simulada con `for`+`append`**: `categorias_unicas`/`indexar_por_id` con un bucle
   y `.add()`/asignación dan el resultado correcto pero **no cumplen O1**. Si el objetivo es aprender
   comprehensions, márcalo como en-progreso aunque los tests estén verdes.
3. **`set()` vs `{}`**: `{}` es un **dict** vacío, no un set vacío. `categorias_unicas([])` debe ser
   `set()`.
4. **Romper el orden** en `stream_montos** (ordenar, pasar por un `set`): debe conservar el orden de
   entrada (lo verifica `test_stream_montos_filtra_y_conserva_orden`).
5. **Filtro con `>` en vez de `>=`**: excluiría el valor igual al `minimo`
   (`test_stream_montos_incluye_el_limite`).

## Rango de soluciones aceptables
- `stream_montos` como **generator expression** devuelta: `return (t["monto"] for t in transacciones
  if t["monto"] >= minimo)` es **excelente** y sigue siendo un generador (`inspect.isgenerator` da
  `True`), así que pasa todos los tests. Acéptala si el alumno la entiende.
- Usar `t.get("categoria")`/`t.get("id")` en vez de `t["..."]` es válido (más defensivo).
- Anotaciones de tipo con `Iterator[float]`, `Generator[float, None, None]` o sin anotación: todas
  válidas; no afectan el comportamiento.
- Nombres de variable de iteración distintos (`tx`, `trans`) son irrelevantes.
