---
ejercicio_id: fase-2/refactor-precio-con-smells
fase: fase-2
sub_unidad: "2.3"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Refactoriza una función con smells (red ya puesta)

## Implementación canónica (`solucion.py` refactorizado)

```python
DESCUENTO_VIP_ALTO = 0.20
DESCUENTO_VIP_BASE = 0.10
DESCUENTO_FRECUENTE_ALTO = 0.10
DESCUENTO_FRECUENTE_BASE = 0.05
UMBRAL_DESCUENTO_ALTO = 100000
UMBRAL_ENVIO_GRATIS = 50000
COSTO_ENVIO = 3990
TASA_IVA = 0.19
CUPON_ENVIO_GRATIS = "ENVIOGRATIS"


def subtotal(items):
    return sum(precio * cantidad for _, precio, cantidad in items)


def descuento_por_cliente(tipo_cliente, monto):
    if tipo_cliente == "vip":
        tasa = DESCUENTO_VIP_ALTO if monto > UMBRAL_DESCUENTO_ALTO else DESCUENTO_VIP_BASE
    elif tipo_cliente == "frecuente":
        tasa = DESCUENTO_FRECUENTE_ALTO if monto > UMBRAL_DESCUENTO_ALTO else DESCUENTO_FRECUENTE_BASE
    else:
        tasa = 0.0
    return monto * tasa


def costo_envio(codigo_cupon, monto):
    if codigo_cupon == CUPON_ENVIO_GRATIS:
        return 0
    if monto > UMBRAL_ENVIO_GRATIS:
        return 0
    return COSTO_ENVIO


def iva(monto):
    return monto * TASA_IVA


def total_orden(items, tipo_cliente, codigo_cupon):
    monto = subtotal(items)
    monto = monto - descuento_por_cliente(tipo_cliente, monto)
    return monto + iva(monto) + costo_envio(codigo_cupon, monto)
```

> El test debe importar `total_orden` (si el alumno renombró `calc`) ajustando **solo**
> la línea de `import`. Verificado de forma exhaustiva: para todo el espacio de casos
> relevante, `total_orden` devuelve exactamente lo mismo que la `calc` original.

## Mapa smell → refactoring (lo que el `smells.md` debería contener)

| Smell | Refactoring de Fowler | Dónde |
|---|---|---|
| Mysterious Name (`calc`, `c`, `p`, `t`, `i`) | Rename Function / Rename Variable | toda la función |
| Magic Numbers (`0.20`, `0.10`, `0.05`, `100000`, `50000`, `3990`, `0.19`) | Replace Magic Literal with Symbolic Constant | constantes al tope |
| Duplicated Code (bloque vip ≈ bloque frecuente) | Extract Function (`descuento_por_cliente`) | descuento |
| Long Function (subtotal + descuento + envío + IVA en una) | Extract Function (`subtotal`, `costo_envio`, `iva`) | toda |
| Nested Conditional (`if` dentro de `if`) | Decompose Conditional / guardas con `return` | descuento y envío |
| Comments (desodorante: `# calcular el subtotal sumando`, etc.) | borrarlos (el código se explica solo) | toda |

## Razonamiento paso a paso (el orden que debió recorrer)

1. **Confirmar verde de partida** (`pytest`). Sin esto, nada empieza.
2. **Rename** (bajo riesgo): `calc`→`total_orden`, `c`→`tipo_cliente`, `p`→`codigo_cupon`, `t`→`monto`/`subtotal`. Ajustar import del test. Correr → verde. Commit `refactor: renombra total_orden y variables`.
3. **Replace Magic Literal**: subir los números a constantes nombradas. Correr → verde.
4. **Extract Function `subtotal(items)`**: reemplazar el bucle acumulador por `sum(...)`. Correr → verde.
5. **Extract Function `descuento_por_cliente(tipo, monto)`**: aquí muere la duplicación. Aplanar el anidamiento a `if/elif/else` con la tasa elegida por umbral. Correr → verde.
6. **Extract Function `costo_envio` e `iva`**: aplanar el condicional de envío a guardas. Correr → verde.
7. **Componer** `total_orden` en 3 líneas legibles. Correr → verde. Commit final.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Equivalencia de floats.** El original calcula `monto - monto*0.20`. La referencia hace lo mismo (`monto - descuento`, con `descuento = monto*0.20`). Si el alumno usa `monto*0.80`, es **algebraicamente** igual y casi siempre **idéntico** en float; los tests usan `pytest.approx`, así que pasa. No penalizar por esto.
2. **Orden de evaluación del descuento.** El `else`/normal debe dar descuento 0. Si el alumno olvida la rama "otro tipo de cliente", un caso `normal` se rompe.
3. **`subtotal` con desempaquetado.** `for nombre, precio, cantidad in items` es más limpio que `i[1]*i[2]`; ambas válidas.
4. **No tocar las aserciones.** Si el alumno cambió un `esperado` o un caso para "que pase", es C1 incompleto: la red dejó de garantizar el comportamiento.
5. **Parar a tiempo.** Para 4 ramas no hace falta Strategy/registry/enum (eso es 2.4–2.5). Si aparece, marcar posible Speculative Generality / receta pegada, no "excelente".

## Rango de soluciones aceptables
- **`descuento_por_cliente` con un dict de tasas** (`{("vip", True): 0.20, ...}`) o con dos funciones: válido si elimina la duplicación y queda legible.
- **`costo_envio` con un solo `if/elif/else`** en vez de dos guardas: equivalente.
- **No extraer `iva`** (dejar `monto * TASA_IVA` inline): aceptable; baja un poco la nota de C3 pero no es error.
- **Mantener el nombre `calc`** y renombrar solo internamente: válido (evita tocar el import), aunque `calc` sigue siendo un nombre pobre — comentar como mejora.
- **Constantes con otros nombres**: cualquiera con intención clara.
- **Caso borde propio en `smells.md`/tests**: no se exige test nuevo aquí (la red es provista), pero un caso extra documentado suma.
