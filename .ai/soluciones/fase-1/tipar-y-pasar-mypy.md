---
ejercicio_id: fase-1/tipar-y-pasar-mypy
fase: fase-1
sub_unidad: "1.4"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Tipar un módulo y hacer pasar `mypy --strict`

## Respuesta canónica

```python
def descuento(precio: int, porcentaje: int) -> float:
    """Aplica un descuento porcentual (0..100) a un precio y devuelve el precio final."""
    return precio - (precio * porcentaje / 100)


def total_despensa(items: list[dict[str, int]]) -> float:
    """Suma el precio final de cada item; un item sin 'descuento_pct' cuenta como 0%."""
    suma: float = 0
    for item in items:
        suma += descuento(item["precio"], item.get("descuento_pct", 0))
    return suma
```

Con esto: `mypy --strict despensa.py` reporta **0 errores** y los 4 tests pasan.

## Razonamiento paso a paso

1. **`descuento`**: ambos parámetros son enteros (precio en pesos, porcentaje 0..100). El retorno es `float` porque la división `/` en Python siempre devuelve `float` (`1000 - 250.0 == 750.0`). Aunque el resultado parezca "redondo", su tipo es `float`.
2. **`total_despensa`**: la lista de items es `list[dict[str, int]]` (cada dict mapea claves `str` a valores `int`). Bajo `--strict` no se permite `dict` ni `list` pelados (regla `disallow_any_generics`): hay que dar el contenido.
3. **El acumulador**: si se escribe `suma = 0`, mypy lo infiere `int`; al hacer `suma += <float>` el resultado es `float` y mypy marca `Incompatible types in assignment`. La anotación `suma: float = 0` resuelve esto (un `int` se asigna sin problema a un `float` por la torre numérica).
4. **El bug que mypy revela**: con las firmas puestas, `item.get("descuento_pct")` tiene tipo `int | None` (porque `.get` devuelve `None` si la clave falta) y se pasa a `descuento`, que exige `int`. mypy:

   ```text
   error: Argument 2 to "descuento" has incompatible type "int | None"; expected "int"  [arg-type]
   ```

   El arreglo correcto **elimina el `None` en origen**: `item.get("descuento_pct", 0)`. Ahora el método devuelve siempre `int`, el test del item sin descuento pasa, y mypy queda limpio por la razón correcta.

## Puntos resbalosos (donde el corrector debe mirar)
1. **`# type: ignore` / `cast` / `assert`** para callar a mypy sin quitar el `None`. mypy pasa, pero el bug de runtime sigue latente: es la trampa principal del ejercicio. El default (`, 0`) es estrictamente superior porque hace **imposible** el `None`, no solo invisible el aviso.
2. **Olvidar `suma: float = 0`.** Es el error de tipo más fácil de pasar por alto; quien solo anota las funciones sigue con un error de mypy.
3. **`dict`/`list` pelados** bajo `--strict`: deben llevar parámetros (`list[dict[str, int]]`).
4. **Arreglar el test** (forzar que todos los items traigan `descuento_pct`) en vez del código: esquiva el objetivo.

## Rango de soluciones aceptables
- El default puede expresarse también con un guard explícito antes de llamar: `pct = item.get("descuento_pct"); if pct is None: pct = 0` — válido y `competente` si elimina el `None` (aunque `.get(..., 0)` es más idiomático).
- Tipos numéricos: aceptar `float` en vez de `int` para `precio`/`porcentaje` es defendible si el alumno lo justifica (precios con decimales); lo importante es que sean **coherentes** y mypy quede limpio. Lo que **no** es aceptable es `Any` o `dict`/`list` sin parametrizar.
- `descuento` anotado `-> float` es lo correcto; anotarlo `-> int` sería un error porque `/` produce `float`.
- Un test propio de lista vacía (`total_despensa([]) == 0`) cuenta para el nivel `excelente`.
