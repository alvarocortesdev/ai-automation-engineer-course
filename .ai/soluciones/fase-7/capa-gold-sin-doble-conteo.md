---
ejercicio_id: fase-7/capa-gold-sin-doble-conteo
fase: fase-7
sub_unidad: "7.5a"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver
> `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Construir la capa gold sin doble conteo

## Implementación de referencia

```python
def ingresos_por_categoria(lineas: list[dict], productos: list[dict]) -> dict[str, int]:
    # mapa de la dimensión: producto_id -> categoria (una sola vez, no dentro del bucle)
    categoria_de = {p["producto_id"]: p["categoria"] for p in productos}
    out: dict[str, int] = {}
    for linea in lineas:                       # grain de LÍNEA: iterar el hecho
        cat = categoria_de[linea["producto_id"]]
        out[cat] = out.get(cat, 0) + linea["monto"]
    return out


def valor_total_por_cliente(lineas: list[dict], ordenes: list[dict]) -> dict[str, int]:
    cliente_de_orden = {o["orden_id"]: o["cliente_id"] for o in ordenes}
    out: dict[str, int] = {}

    # Grain LÍNEA: suma de montos por cliente (cliente_id sale de la orden)
    for linea in lineas:
        cli = cliente_de_orden[linea["orden_id"]]
        out[cli] = out.get(cli, 0) + linea["monto"]

    # Grain ORDEN: el envío se cuenta UNA vez por orden (iteramos ordenes, no lineas)
    for orden in ordenes:
        cli = orden["cliente_id"]
        out[cli] = out.get(cli, 0) + orden["envio"]

    return out
```

## Por qué funciona (y por qué el enfoque ingenuo no)

La clave es que **`monto` vive a grain de línea** y **`envio` vive a grain de orden**. Para combinarlos
sin error, se agrega **cada uno en su propio grain** y luego se suman por cliente.

El enfoque ingenuo —construir una sola tabla aplanada uniendo cada línea con su orden, y sumar `monto`
y `envio` en la misma pasada— produce **fan-out**: la orden O1 tiene 3 líneas, así que al unir aparece
en 3 filas, y `SUM(envio)` cuenta su envío **3 veces**:

| Cliente | Líneas (monto) | Envío correcto (1×/orden) | Envío ingenuo (1×/línea) | Total correcto | Total inflado |
|---|---|---|---|---|---|
| C1 (O1, 3 líneas) | 25000 | 3000 | 3000 × 3 = 9000 | **28000** | 34000 |
| C2 (O2, 1 línea) | 8000 | 2000 | 2000 × 1 = 2000 | **10000** | 10000 |

SQL **no da error** con el enfoque ingenuo: te entrega 34000, un número que parece válido. Por eso es
un bug peligroso —se detecta solo si conoces el grain o si tienes un test como
`test_envio_no_se_duplica_con_varias_lineas`.

**Regla general (lo que marca "excelente"):** *siempre que combines datos a distintos grains, agrega
cada uno a su grain antes de unirlos.* Lo mismo aplica en SQL: pre-agregas en subconsultas/CTEs por
grain y luego unes los resultados, en vez de unir las tablas crudas y sumar.

## Errores que la solución evita

- **Iterar `productos` en `ingresos_por_categoria`** haría aparecer la categoría "jardin" (P9, sin
  ventas) con 0. Correcto: iterar `lineas` (solo aparecen categorías con ventas).
- **Recalcular el mapa de dimensión dentro del bucle** es O(n·m) innecesario (eco del N+1 de F3).
- **Asumir una orden por cliente** rompe con `test_cliente_con_multiples_ordenes`.

## Rango de soluciones aceptables

- Cualquier solución que **separe las dos agregaciones por grain** y las combine es válida, use dicts,
  `collections.defaultdict` o `Counter`.
- El orden de las dos pasadas es indiferente.
- Soluciones de una sola pasada son aceptables **solo** si demostradamente no fan-outean el envío (p.
  ej. marcando órdenes ya contadas); en la práctica, dos pasadas es más claro y menos propenso a error.
