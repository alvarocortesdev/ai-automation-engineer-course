---
ejercicio_id: fase-0/notional-machine-parsons
fase: fase-0
sub_unidad: "0.3"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Parsons: ordena la función `promedio`

## Respuesta canónica

```python
def promedio(numeros):
    if not numeros:
        return 0.0
    total = 0
    for n in numeros:
        total = total + n
    return total / len(numeros)
```

`uv run pytest` (o `pytest`) en verde: `promedio([2, 4, 6]) == 4.0`, `promedio([7]) == 7.0`, `promedio([]) == 0.0` (sin `ZeroDivisionError`).

## Razonamiento (por qué ese orden y no otro)

El orden no es estético: lo fijan las **dependencias**.

1. **`def promedio(numeros):`** — la firma abre todo; nada puede ir antes.
2. **`if not numeros: return 0.0`** — *dependencia de control*. Es un **early return** (guard clause): corta la ejecución cuando la lista está vacía, **antes** de llegar a `total / len(numeros)`. Sin él, dividir entre `len([]) == 0` lanza `ZeroDivisionError`. El test del caso borde lo verifica.
3. **`total = 0`** — *dependencia de datos*. El acumulador debe **existir** antes del bucle que lo usa. Ponerlo después del `for` produce `NameError`.
4. **`for n in numeros:` + `total = total + n`** (indentado dentro del `for`) — recorre y acumula. La indentación **es** la estructura: `total = total + n` está dentro del bucle (se ejecuta una vez por elemento); si quedara fuera, sumaría solo el último.
5. **`return total / len(numeros)`** — al nivel de la función (no dentro del `for`). Si estuviera indentado dentro del bucle, retornaría en la primera vuelta con un promedio falso.

## Puntos resbalosos (donde el corrector debe mirar)
1. **`total = 0` mal ubicado.** Después del `for` → `NameError`. Es el error de dependencia de datos más común.
2. **Guard ausente o tardío.** Si `if not numeros` no existe o va después de calcular `len`, el caso vacío revienta. La división entre cero es justo lo que el test caza.
3. **Indentación.** Confundir qué vive dentro del `for`. `return` final dentro del bucle = retorna demasiado pronto; `total = total + n` fuera del bucle = no acumula.
4. **Orden alternativo válido.** `total = 0` *podría* ir antes del guard sin romper nada (no hay dependencia entre ambos). La referencia pone el guard primero por claridad (early return antes de tocar datos), pero un alumno que coloque `total = 0` antes del `if` y lo **justifique** sigue siendo correcto.

## Rango de soluciones aceptables
- Cualquier orden que pase todos los tests y respete las dependencias es `competente`. La posición relativa de `total = 0` y el guard es intercambiable (ver punto 4) **si el alumno lo razona**.
- Cuerpo del bucle equivalente: `total += n` en vez de `total = total + n` es válido (no se exige una forma).
- El guard puede escribirse `if len(numeros) == 0:` en vez de `if not numeros:`; ambos correctos. `not numeros` es más idiomático, pero no se penaliza el otro.
- Para C3, el test propio del alumno debe aportar un caso **nuevo** (negativos, decimales, tipo `float`), no repetir uno ya cubierto.
