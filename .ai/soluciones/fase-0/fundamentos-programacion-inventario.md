---
ejercicio_id: fase-0/fundamentos-programacion-inventario
fase: fase-0
sub_unidad: "0.7"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Resumen de gastos por categoría

## Respuesta canónica

```python
def total_por_categoria(gastos):
    totales = {}
    for gasto in gastos:
        categoria = gasto.get("categoria")
        monto = gasto.get("monto")
        if not categoria:                     # "" , None o ausente -> falsy
            raise ValueError(f"Categoría inválida: {categoria!r}")
        if monto is None or monto < 0:
            raise ValueError(f"Monto inválido en {categoria!r}: {monto!r}")
        totales[categoria] = totales.get(categoria, 0) + monto
    return totales
```

## Razonamiento paso a paso
1. **Acumulador fuera del bucle.** `totales = {}` se crea una sola vez, antes del `for`. Si
   estuviera dentro, se reiniciaría en cada vuelta y solo quedaría el último gasto.
2. **Validar antes de acumular.** Por cada gasto, primero se chequea categoría y monto; si algo
   falla, `raise ValueError` corta ahí mismo y el total nunca se contamina.
   - `if not categoria` cubre `""`, `None` y la clave ausente (`.get` devuelve `None`) en una sola
     condición, porque todos son *falsy*.
   - `monto is None or monto < 0` separa "ausente" de "negativo"; el orden importa: comparar
     `None < 0` reventaría con `TypeError`, por eso `is None` va primero (cortocircuito).
3. **Sumar con `.get(clave, 0)`.** Para el primer gasto de una categoría, `totales.get(cat, 0)`
   devuelve `0`, así no hace falta un `if cat in totales` aparte. Para los siguientes, devuelve el
   acumulado y suma encima.
4. **Lista vacía.** El `for` no itera ni una vez → devuelve el `{}` inicial. El caso borde sale
   "gratis" porque el acumulador ya está bien inicializado.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Acumulador dentro del bucle** (error #1): pierde todo menos el último gasto.
2. **`monto < 0` antes de `is None`**: si el monto es `None`, `None < 0` lanza `TypeError`, no
   `ValueError` — manejo de errores mal ordenado.
3. **`if categoria == ""` solo**: no atrapa `None` ni la clave ausente. `if not categoria` es más
   robusto.
4. **`print` en vez de `return`**: la función devuelve `None`; todos los tests fallan.
5. **Validar después de sumar**: el negativo ya entró al total antes de lanzar.

## Rango de soluciones aceptables
- `from collections import defaultdict; totales = defaultdict(int)` y `totales[cat] += monto` es
  **excelente** si el alumno lo entiende y devuelve un `dict` (los tests comparan contra `dict`;
  `defaultdict == dict` con mismo contenido es `True`, así que pasa).
- Separar la validación en una función auxiliar (`_validar(gasto)`) es válido y bienvenido.
- Validar con `monto < 0` envuelto en `try/except TypeError` para el caso `None` es aceptable
  aunque menos limpio que `is None` primero.
- Mensajes de error con otra redacción son válidos mientras nombren el problema; el contrato solo
  exige que sea un `ValueError`, no un texto específico.
