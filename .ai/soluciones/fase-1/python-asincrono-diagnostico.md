---
ejercicio_id: fase-1/python-asincrono-diagnostico
fase: fase-1
sub_unidad: "1.3"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Diagnostica el async roto

## Los tres bugs (diagnóstico canónico)

### Bug (1) — corutina llamada sin `await`
```python
registrar_inicio(nombre)      # ❌ falta await
```
`registrar_inicio` es `async def`, así que llamarla **no ejecuta su cuerpo**: crea un objeto corutina
que se descarta. **Síntoma:** el log nunca se imprime y Python avisa
`RuntimeWarning: coroutine 'registrar_inicio' was never awaited`. **Causa:** una corutina solo avanza
si se la espera (`await`) o se la agenda (`create_task`/`gather`).

### Bug (2) — código bloqueante dentro de una corutina
```python
time.sleep(recurso["demora"])    # ❌ síncrono: congela el event loop
```
`time.sleep` es **síncrono**: no cede el turno. **Causa:** el event loop solo cambia de tarea en un
`await`; mientras `time.sleep` corre, **ninguna** otra corutina avanza. **Síntoma:** aunque hubiera
concurrencia, las "descargas" se serializan igual. **Fix:** `await asyncio.sleep(...)`. (Si fuera una
librería bloqueante real sin versión async —p. ej. `requests`— se envuelve en
`await asyncio.to_thread(funcion_bloqueante, ...)` para sacarla a otro hilo.)

### Bug (3) — `await` en serie dentro del bucle
```python
for recurso in recursos:
    datos = await descargar(recurso)   # ❌ espera cada una antes de lanzar la siguiente
```
**Causa:** `await` espera hasta el final de cada descarga antes de pasar a la próxima → secuencial.
**Síntoma:** tarda la suma de las demoras. **Fix:** lanzar todas y esperar juntas con
`asyncio.gather`/`TaskGroup`.

> **Punto clave que distingue `competente` de `excelente`:** (2) y (3) **se suman**. Arreglar solo el
> `gather` pero dejar `time.sleep` deja el programa igual de lento (el loop sigue bloqueado). Hay que
> corregir los dos para que el test de tiempo pase.

## Solución corregida (`solucion.py`)

```python
import asyncio


async def registrar_inicio(nombre: str) -> None:
    await asyncio.sleep(0.01)
    print(f"[log] empezando {nombre}")


async def descargar_todo(recursos: list[dict]) -> list[str]:
    async def descargar(recurso: dict) -> str:
        await registrar_inicio(recurso["nombre"])   # (1) ahora SÍ se espera
        await asyncio.sleep(recurso["demora"])       # (2) sleep asíncrono, no bloquea el loop
        return f"datos de {recurso['nombre']}"

    async with asyncio.TaskGroup() as tg:            # (3) concurrente, no en serie
        tareas = [tg.create_task(descargar(r)) for r in recursos]
    return [t.result() for t in tareas]
```

Variante equivalente con `gather`:

```python
async def descargar_todo(recursos: list[dict]) -> list[str]:
    async def descargar(recurso: dict) -> str:
        await registrar_inicio(recurso["nombre"])
        await asyncio.sleep(recurso["demora"])
        return f"datos de {recurso['nombre']}"

    return list(await asyncio.gather(*(descargar(r) for r in recursos)))
```

Ambas pasan los tres tests: resultados en orden, lista vacía → `[]`, y total ≈ la mayor demora.

## Puntos resbalosos (donde el corrector debe mirar)

1. **Arreglo a medias.** Cambió `await` por `gather` pero dejó `time.sleep`: el test de tiempo sigue
   rojo. Es `en-progreso`, y es la trampa pedagógica central.
2. **Borrar en vez de arreglar.** "Solucionar" el bug (1) eliminando la llamada al log, o silenciando
   el `RuntimeWarning` con un filtro de warnings, no demuestra comprensión: márcalo.
3. **Diagnóstico que confunde causa y síntoma.** "El time.sleep es lento" es síntoma; la causa es que
   **bloquea el event loop**. Exige la causa.
4. **`to_thread` innecesario.** Envolver `asyncio.sleep` en `to_thread` revela que no distingue I/O
   asíncrono nativo (no necesita hilo) de librería bloqueante (sí lo necesita).

## Rango de soluciones aceptables

- `gather` o `TaskGroup` son ambos válidos; `create_task` + `await` posterior también, si se crean todas
  antes de esperar.
- Mantener `registrar_inicio` con `await`, o integrar el log dentro de `descargar`, ambas valen; lo que
  no vale es eliminar el log para "callar" la advertencia.
- El `diagnostico.md` puede ordenar los bugs como quiera y usar sus propias palabras; lo que se exige es
  **causa correcta** para los tres, no una redacción concreta.
- No se acepta: `solucion.py` que pase los tests pero con `diagnostico.md` ausente o que no explique por
  qué cada cambio resuelve su bug (es un ejercicio mixto: la comprensión es entregable de primera clase).
