---
ejercicio_id: fase-2/depurar-con-stack-trace-y-pdb
fase: fase-2
sub_unidad: "2.12"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Caza el bug con método: stack trace → pdb → test de regresión

> El fix es **una línea**. El examen real es el **método y la evidencia** en `traza.md`.
> Mide el proceso (trace leído → hipótesis → confirmación con pdb → test rojo primero →
> fix de causa raíz → deuda anotada), no solo que `pytest` quede verde.

## Paso 1 — Reproducir y leer el stack trace (lo que `traza.md` debe contener)

Al correr `pytest`, `test_regresion_412_solo_abonos` revienta. El trace (el mensaje
exacto varía entre versiones de Python — `is empty` / `is an empty sequence` — da igual):

```text
movs = [{"tipo": "abono", "monto": 1000}, {"tipo": "abono", "monto": 500}]
...
  File ".../solucion.py", line 28, in resumen_cuenta
    "mayor_cargo": max(cargos),
                   ^^^^^^^^^^^
ValueError: max() iterable argument is empty
```

Lectura correcta (abajo → arriba):
- **El QUÉ** (última línea): `ValueError: max() ... is empty` → se llamó `max()` con una secuencia vacía.
- **El DÓNDE** (último frame del propio código): `resumen_cuenta`, línea de `max(cargos)`. Ahí nace el fallo.
- **El contexto** (frames de más arriba / el caller del test): *quién* llamó con solo abonos. Contexto, no causa.

## Paso 2 — Hipótesis + confirmación con el debugger

**Hipótesis (una frase, falsable):** "`cargos` está vacío cuando la cuenta solo tiene abonos, y `max([])` no tiene valor."

Confirmación con `pdb` post-mortem (lo que se pega en `traza.md`):

```text
$ python -m pdb -c continue solucion.py     # con el caso #412 descomentado
...
ValueError: max() iterable argument is empty
> .../solucion.py(28)resumen_cuenta()
-> "mayor_cargo": max(cargos),
(Pdb) p cargos
[]
(Pdb) p abonos
[1000, 500]
(Pdb) w        # la pila: dónde estoy y quién me llamó
(Pdb) q
```

`p cargos` → `[]` confirma la hipótesis **con evidencia**, no con fe. `p abonos` → `[1000, 500]`
muestra que el resto del cálculo está sano: el único problema es `max([])`.

## Paso 3 — Test de regresión rojo primero (`test_solucion.py`)

Completar el `TODO` y **verlo fallar** antes de tocar `solucion.py`:

```python
def test_regresion_412_solo_abonos():
    movs = [{"tipo": "abono", "monto": 1000}, {"tipo": "abono", "monto": 500}]
    r = resumen_cuenta(movs)
    assert r["saldo"] == 1500
    assert r["mayor_cargo"] == 0      # decisión de diseño: 0 cuando no hay cargos
```

Hoy falla con el `ValueError`. Ese rojo es la prueba objetiva de que el bug existe y se entendió.

## Paso 4 — Fix de causa raíz (cambio mínimo en `solucion.py`)

```python
    return {
        "saldo": saldo,
        "n_movimientos": len(movimientos),
        "mayor_cargo": max(cargos, default=0),   # <-- única línea que cambia
    }
```

`max(iterable, *, default=0)` es exactamente "el máximo, o este valor si está vacío"
(parámetro `default` de la stdlib, estable desde Python 3.4). Tras el fix: `pytest` **verde**
(el de regresión pasa, `test_caso_normal_funciona` sigue pasando, el `xfail` sigue xfail).

**Decisión de diseño declarada (en `traza.md`):** `mayor_cargo = 0` mantiene el tipo numérico,
cómodo para sumar/comparar aguas abajo. `None` ("no aplica") es más honesto pero obliga a chequear
`None` en cada consumidor. Ambas son defendibles; lo indefendible es no decidir y dejar que reviente.
La referencia elige `0` y lo **fija con el test**.

## Paso 5 — Dos sombreros: la deuda del `tipo` desconocido (NO se arregla aquí)

El módulo además **ignora en silencio** un movimiento con `tipo` que no es `"abono"` ni `"cargo"`:
su `monto` no entra a `_solo("abono", ...)` ni a `_solo("cargo", ...)`, así que no se suma a ningún
lado (aunque `n_movimientos` sí lo cuenta). Eso **no es el ticket #412**. Se deja registrado:
- el test `test_deuda_tipo_desconocido_no_se_ignora_en_silencio` ya está marcado `xfail` (deuda viva en la suite),
- y se anota en `traza.md` como bug futuro con su propio ticket.

Tocarlo en este commit = cambiar comportamiento que nadie pidió (sombrero equivocado).

## `traza.md` de referencia (estructura mínima esperada)

```markdown
## 1. Trace
Tipo: ValueError · Mensaje: max() ... is empty
Frame del fallo: solucion.py:28, resumen_cuenta, en `max(cargos)`
Caller (contexto, no causa): el test que pasa solo abonos.

## 2. Hipótesis + pdb
Hipótesis: cargos == [] con solo abonos; max([]) no tiene valor.
Sesión: `p cargos` -> []  ·  `p abonos` -> [1000, 500]  ·  `w` -> pila.

## 3. Test rojo
test_regresion_412_solo_abonos falló con ValueError antes del fix.

## 4. Fix + decisión
max(cargos, default=0). Elegí 0 (mantiene tipo numérico) sobre None. Fijado por el test.

## 5. Deuda separada
tipo desconocido se ignora en silencio -> ticket aparte, ya marcado xfail. NO lo arreglo aquí.
```

## Puntos resbalosos (donde el corrector debe mirar)
1. **Parche de síntoma vs causa raíz.** `try/except ValueError: mayor_cargo = 0` "apaga" el error pero se tragaría cualquier *otro* `ValueError` real (p. ej. un `monto` corrupto) → bug silencioso peor que el original. La causa raíz es `max([])` sin valor → `default=`. Si el alumno usó `try/except`, es C3 incompleto aunque pase el test.
2. **Test escrito ya verde.** Si nunca vio el rojo (lo agregó junto al fix), no probó que entendió el bug. Buscar en `traza.md` la mención de "falló primero".
3. **Adivinar en vez de confirmar.** `traza.md` sin el valor real de `cargos` (`[]`) ni comandos de pdb = corazonada. A veces acierta; el hábito traiciona en el bug difícil.
4. **Leer el trace al revés** y culpar al caller/test en vez del frame de `resumen_cuenta`.
5. **"Arreglar" el `tipo` desconocido** dentro de este ticket: cambia comportamiento ajeno. Es justo la trampa de los dos sombreros.

## Rango de soluciones aceptables
- **`max(cargos, default=0)`** — la canónica, mínima.
- **`max(cargos) if cargos else 0`** — equivalente y legible; aceptable.
- **`mayor_cargo = 0` con un guard `if not cargos`** antes del `return` — más verboso pero válido si no cambia el resto.
- **Decidir `None` en vez de `0`** — aceptable **si** lo declara en `traza.md`, lo fija en el test y es coherente (no rompe `test_caso_normal_funciona`, que con cargos sí da un número).
- **Dejar la deuda como `xfail` + nota** (no tocarla): **excelente** (dos sombreros como flujo).
- Lo que **no** es aceptable: `try/except` que traga el error; reescribir la función entera; "corregir" el `tipo` desconocido aquí; cambiar `test_caso_normal_funciona`.
