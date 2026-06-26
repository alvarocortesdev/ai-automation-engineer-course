---
ejercicio_id: fase-1/python-asincrono-descargas-concurrentes
fase: fase-1
sub_unidad: "1.3"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Descargas concurrentes que se miden solas

## Solución canónica (con `gather`)

```python
import asyncio


async def obtener_todos(recursos: list[dict]) -> list[str]:
    async def descargar(recurso: dict) -> str:
        await asyncio.sleep(recurso["demora"])      # simula la espera de I/O
        return f"datos de {recurso['nombre']}"

    # Construyo las corutinas SIN esperarlas, y las paso todas juntas a gather.
    # gather las arranca, deja que el loop intercale sus esperas, y devuelve los
    # resultados EN ORDEN DE ENTRADA (no de finalización).
    corutinas = [descargar(r) for r in recursos]
    return list(await asyncio.gather(*corutinas))
```

La lista vacía sale gratis: `asyncio.gather()` sin argumentos devuelve `[]`.

## Variante moderna (`TaskGroup`, Python 3.11+)

```python
import asyncio


async def obtener_todos(recursos: list[dict]) -> list[str]:
    async def descargar(recurso: dict) -> str:
        await asyncio.sleep(recurso["demora"])
        return f"datos de {recurso['nombre']}"

    async with asyncio.TaskGroup() as tg:
        tareas = [tg.create_task(descargar(r)) for r in recursos]
    # al salir del 'async with', todas terminaron; recojo resultados en orden.
    return [t.result() for t in tareas]
```

Ambas son `competente`. `TaskGroup` se prefiere en código nuevo porque, si una tarea falla, cancela
las demás y agrupa los errores en un `ExceptionGroup` (no deja tareas zombis). `gather` sin
`return_exceptions=True` propaga la primera excepción pero deja correr el resto.

## Por qué funciona (el punto que el corrector debe confirmar que el alumno entiende)

- La concurrencia **no** viene de `async`/`await` por sí solos: viene de tener **varias** corutinas
  cuyas esperas (`await asyncio.sleep`) se **solapan**. La pieza que las solapa es `gather`/`TaskGroup`.
- El orden de los resultados lo garantiza `gather` (mapea posición de entrada → posición de salida),
  **independiente** de cuál terminó primero. Por eso el test pone la demora más corta en el medio.
- Es un solo hilo: mientras una corutina espera en su `sleep`, el loop avanza otra. No hay paralelismo.

## Contraejemplo (lo que NO debe pasar el test)

```python
async def obtener_todos(recursos):
    resultados = []
    for recurso in recursos:
        await asyncio.sleep(recurso["demora"])          # ❌ espera cada una hasta el final
        resultados.append(f"datos de {recurso['nombre']}")
    return resultados
```

Correcto en valores, pero **secuencial**: tarda la suma de las demoras. `test_es_concurrente` lo
rechaza (≈0.6s para 3×0.2s). Este es el error central que el ejercicio busca provocar y corregir.

## Puntos resbalosos (donde el corrector debe mirar)

1. **`gather(*corutinas)` vs `gather(corutinas)`.** Sin el `*`, pasa la lista como un único argumento
   y falla. Verifica el desempaquetado.
2. **Pérdida de orden.** Si el alumno usó `asyncio.as_completed` y appendeó por llegada, los valores
   correctos saldrán **desordenados**: `test_resultados_en_orden_de_entrada` lo delata. Es `en-progreso`.
3. **`asyncio.run` anidado.** `obtener_todos` debe ser una corutina pura; el `run` vive en el test o en
   `main`. Llamar a `run` dentro produce `RuntimeError: asyncio.run() cannot be called from a running
   event loop`.
4. **`time.sleep` por costumbre.** Bloquearía el loop y además rompe el test de tiempo.

## Rango de soluciones aceptables

- `gather`, `TaskGroup`, o crear tareas con `create_task` y luego `await` de cada una (siempre que se
  creen **todas antes** de esperar) son válidas.
- Devolver una `tuple` en vez de `list` es aceptable solo si los tests siguen pasando (comparan con
  `list`; `gather` ya devuelve `list`, así que basta con no convertir a otra cosa rara).
- Manejar la lista vacía con un `if not recursos: return []` explícito es correcto aunque redundante.
- No se acepta: secuencial, fuera de orden, o con `time.sleep`.
