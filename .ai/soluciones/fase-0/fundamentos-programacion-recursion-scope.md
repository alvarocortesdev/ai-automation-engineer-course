---
ejercicio_id: fase-0/fundamentos-programacion-recursion-scope
fase: fase-0
sub_unidad: "0.7"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Recursión y scope, trazados a mano

## Respuesta canónica
El programa imprime, en este orden:

```text
6
10
10
```

## Razonamiento paso a paso

### `print(f(3))` → 6
Dentro de `f`, `x = n * 2 = 3 * 2 = 6`; `return x` devuelve `6`.

### `print(x)` → 10 (no 6) — scope
La línea `x = 10` (nivel del módulo, **global**) y la `x` de dentro de `f` son **variables
distintas**. Al asignar `x = n * 2` dentro de `f`, Python crea una `x` **local** que solo vive
durante la llamada y **tapa** (shadowing) a la global mientras dura. La global nunca se toca, así
que al volver vale `10`. (Regla **LEGB**: al buscar un nombre, Python mira Local → Enclosing →
Global → Built-in; dentro de `f`, `x` se resuelve a la local.)

### `print(suma_hasta(4))` → 10 — pila de llamadas
`range`/sumas bajan hasta el caso base `n == 0` y luego suben resolviendo:

| Nivel | Llamada | Baja: qué queda pendiente | Sube: qué devuelve |
|---|---|---|---|
| 1 | `suma_hasta(4)` | `4 + suma_hasta(3)` | `4 + 6 = 10` |
| 2 | `suma_hasta(3)` | `3 + suma_hasta(2)` | `3 + 3 = 6` |
| 3 | `suma_hasta(2)` | `2 + suma_hasta(1)` | `2 + 1 = 3` |
| 4 | `suma_hasta(1)` | `1 + suma_hasta(0)` | `1 + 0 = 1` |
| 5 | `suma_hasta(0)` | caso base, no baja más | `0` |

La subida resuelve de adentro hacia afuera: `0 → 1 → 3 → 6 → 10`. Total: **10** (= `4+3+2+1+0`).

## Puntos resbalosos (donde el corrector debe mirar)
1. **La subida de la recursión.** El caso base no es el final del cálculo: es el punto donde se
   *deja de bajar* y se *empieza a subir*. Un alumno que solo lista `4,3,2,1,0` sin mostrar las
   sumas de vuelta no demostró que entiende el mecanismo.
2. **Scope local vs. global.** El error #1 es predecir `print(x) → 6`. La asignación dentro de `f`
   no afecta la global porque crea una local (sin `global x`).
3. **Caso base.** Sin el `if n == 0: return 0`, la recursión bajaría a `-1, -2, …` indefinidamente
   → `RecursionError`. Vale la pena que el alumno lo note.

## Rango de soluciones aceptables
- Cualquier forma de la pila que muestre **bajada y subida** cuenta como `competente`, aunque use
  un diagrama, una lista anidada (`4 + (3 + (2 + (1 + 0)))`) o la tabla de arriba.
- Para O3, cualquier explicación que nombre con precisión la idea (variable local que tapa a la
  global; LEGB) es válida; no se exige una redacción concreta ni mencionar "shadowing" por su
  nombre si describe el fenómeno.
- Para O1, expresar el total como `4+3+2+1 = 10` (omitiendo el `+0`) es aceptable si la pila
  muestra que el caso base devuelve `0`; lo que no se acepta es un total correcto sin ninguna
  traza.
