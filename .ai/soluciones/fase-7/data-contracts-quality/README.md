---
ejercicio_id: fase-7/data-contracts-quality
fase: fase-7
sub_unidad: "7.5d"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). El alumno debe entregar su propio intento antes de que esto se discuta.

# Solución de referencia — Gate de calidad shift-left

Esta es **una** solución canónica. Hay variantes aceptables (recorrer por filas en vez de por campos, usar `dict` en vez de `Counter`, mensajes de detalle distintos). Lo que NO es negociable: el gate **acumula todas** las violaciones (no corta en la primera), cada `Violacion` trae `campo` + índices de `filas`, y `ok` es True solo con cero violaciones.

## Respuesta canónica

`_tipo_ok` mapea `string→str`, `number→int/float` (excluyendo `bool`), `datetime→str` parseable con `fromisoformat`. `validar_lote` recorre **el contrato** (campo por campo), no el dato, acumulando una `Violacion` por regla rota con los índices de filas afectadas. Volumen y frescura solo se evalúan si vienen en `garantias` (y frescura, además, solo si se pasa `ahora`).

## `_tipo_ok`

```python
def _tipo_ok(valor, tipo: str) -> bool:
    if tipo == "string":
        return isinstance(valor, str)
    if tipo == "number":
        return isinstance(valor, (int, float)) and not isinstance(valor, bool)
    if tipo == "datetime":
        if not isinstance(valor, str):
            return False
        try:
            datetime.fromisoformat(valor)
            return True
        except ValueError:
            return False
    return False
```

> **Punto crítico:** `not isinstance(valor, bool)`. En Python `True == 1` e `isinstance(True, int)` es `True`; sin esa exclusión, `monto=True` pasaría como `number`. Es el error de tipo más fino del ejercicio.

## `validar_lote`

```python
def validar_lote(filas, contrato, ahora=None):
    campos = contrato["campos"]
    garantias = contrato.get("garantias", {})
    n = len(filas)
    violaciones = []

    # --- Volumen (profundización) ---
    vmin, vmax = garantias.get("volumen_min"), garantias.get("volumen_max")
    if vmin is not None and n < vmin:
        violaciones.append(Violacion("volumen", None, f"{n} filas, menos que {vmin}", []))
    if vmax is not None and n > vmax:
        violaciones.append(Violacion("volumen", None, f"{n} filas, mas que {vmax}", []))

    # --- Campos extra (schema drift) ---
    declarados = set(campos)
    extra = {}
    for i, fila in enumerate(filas):
        for clave in fila:
            if clave not in declarados:
                extra.setdefault(clave, []).append(i)
    for clave, idxs in extra.items():
        violaciones.append(Violacion("campo_extra", clave, "campo no declarado", idxs))

    # --- Por campo declarado ---
    for campo, regla in campos.items():
        if regla.get("requerido"):
            faltan = [i for i, f in enumerate(filas) if campo not in f]
            if faltan:
                violaciones.append(Violacion("campo_faltante", campo, "requerido ausente", faltan))
            nulos = [i for i, f in enumerate(filas) if campo in f and f[campo] is None]
            if nulos:
                violaciones.append(Violacion("nulo", campo, "requerido con None", nulos))

        tipo = regla.get("tipo")
        mal_tipo = [i for i, f in enumerate(filas)
                    if campo in f and f[campo] is not None and not _tipo_ok(f[campo], tipo)]
        if mal_tipo:
            violaciones.append(Violacion("tipo", campo, f"no es {tipo}", mal_tipo))

        if "valores" in regla:
            permitidos = set(regla["valores"])
            fuera = [i for i, f in enumerate(filas)
                     if campo in f and f[campo] is not None and f[campo] not in permitidos]
            if fuera:
                violaciones.append(Violacion("valor_no_aceptado", campo, "fuera de dominio", fuera))

        if "min" in regla or "max" in regla:
            fuera_rango = []
            for i, f in enumerate(filas):
                if campo in f and f[campo] is not None and _tipo_ok(f[campo], "number"):
                    v = f[campo]
                    if "min" in regla and v < regla["min"]:
                        fuera_rango.append(i)
                    elif "max" in regla and v > regla["max"]:
                        fuera_rango.append(i)
            if fuera_rango:
                violaciones.append(Violacion("fuera_de_rango", campo, "fuera de [min,max]", fuera_rango))

        if regla.get("unico"):
            presentes = [(i, f[campo]) for i, f in enumerate(filas)
                         if campo in f and f[campo] is not None]
            cuenta = Counter(v for _, v in presentes)
            dups = [i for i, v in presentes if cuenta[v] > 1]
            if dups:
                violaciones.append(Violacion("duplicado", campo, "repetidos en el lote", dups))

    # --- Frescura (profundización) ---
    fr = garantias.get("frescura_horas")
    if fr is not None and ahora is not None:
        ts_vals = []
        for f in filas:
            v = f.get("ts")
            if isinstance(v, str):
                try:
                    ts_vals.append(datetime.fromisoformat(v))
                except ValueError:
                    pass
        if ts_vals and ahora - max(ts_vals) > timedelta(hours=fr):
            violaciones.append(Violacion("frescura", "ts", f"supera {fr} h", []))

    return Reporte(contrato=contrato.get("nombre", "?"), filas_totales=n, violaciones=violaciones)
```

(Requiere `from collections import Counter` y `from datetime import datetime, timedelta`.)

## Salida esperada de `pytest -v`

Los 10 tests provistos en `PASSED`. Caso feliz: `ok=True`, `violaciones=[]`. Cada caso de violación: `ok=False` y la `regla` correspondiente en el set. El test de acumulación verifica que una sola fila mala dispara `duplicado` + `fuera_de_rango` + `valor_no_aceptado` a la vez.

## Puntos resbalosos (donde el corrector debe mirar)

1. **Orden nulo → tipo/rango.** Si evalúa `min`/`max` o `_tipo_ok` numérico sobre un `None`, revienta con `TypeError`. La solución salta los `None` en tipo, dominio y rango (ya cubiertos por `nulo`). Es el bug #1.
2. **`bool` como `number`.** Sin `and not isinstance(v, bool)`, `monto=True` pasa. Bug fino pero clásico.
3. **Acumular vs cortar.** Un `return` o `raise` en la primera violación es `en-progreso`, no `competente`: un productor necesita el reporte completo de una sola corrida.
4. **Índices de filas.** Si `Violacion.filas` queda vacío o trae el valor en vez del índice, el reporte no sirve para diagnosticar. Los tests de `campo_faltante`, `fuera_de_rango` y `duplicado` lo verifican.
5. **`campo_extra` olvidado.** Muchos validan "están los campos que espero" y no detectan campos *de más* — justo el schema drift más sutil.

## Rango de soluciones aceptables

- **Recorrer por filas** (un loop externo de filas, chequeando cada campo dentro) en vez de por campos del contrato es válido si acumula bien y produce índices correctos; suele ser más verboso pero correcto.
- Usar `dict` de conteo manual en vez de `collections.Counter` para duplicados — equivalente.
- Detectar tipo `datetime` con una validación más estricta (regex / formato fijo) en vez de `fromisoformat` — aceptable si no rechaza ISO 8601 válidos.
- Para la profundización, declarar **solo** volumen (sin frescura) ya empuja hacia `excelente` si está bien hecho; ambas + el manejo de zona horaria es el techo.
- Cualquier `WRITEUP.md` que (a) distinga contract/test/observability, (b) justifique shift-left en el borde, y (c) nombre una patología concreta que haría alucinar un RAG en silencio, cuenta como comprensión demostrada (O1+O3).

## Nota sobre la lección (para el corrector)

La lección 7.5d muestra el equivalente en **Great Expectations** (GX Core 1.x: `context.data_sources.add_pandas` → `add_dataframe_asset` → `add_batch_definition_whole_dataframe` → `ExpectationSuite` + `ValidationDefinition.run` → `resultados.success`) y en **OpenLineage** (`OpenLineageClient`, `event_v2.RunEvent/Run/Job/RunState`, `emit`). El alumno NO debía usarlas en el ejercicio (implementa el motor a mano); si las usó delegando todo y no sabe explicar el predicado por debajo, es señal de dependencia-IA, no de dominio.
