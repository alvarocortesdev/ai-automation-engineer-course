---
ejercicio_id: fase-0/notional-machine-trazado
fase: fase-0
sub_unidad: "0.3"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Traza una inversión in-place con aliasing

## Respuesta canónica

El programa imprime, en este orden:

```
[1, 2, 8, 5]
[1, 2, 8, 5]
True
```

## Razonamiento paso a paso

`len(xs)` con `[5, 8, 2, 1]` es `4`, así que `derecha = 3` al inicio. El `while` intercambia los extremos y converge hacia el centro.

Tabla de estado del bucle (estado **después** de cada vuelta):

| Vuelta | `izquierda` (entra) | `derecha` (entra) | `izquierda < derecha` | swap | `xs` tras la vuelta |
|--------|--------------------|-------------------|----------------------|------|---------------------|
| inicio | 0 | 3 | — | — | `[5, 8, 2, 1]` |
| 1 | 0 | 3 | sí | `xs[0]↔xs[3]` | `[1, 8, 2, 5]` (luego `izq=1`, `der=2`) |
| 2 | 1 | 2 | sí | `xs[1]↔xs[2]` | `[1, 2, 8, 5]` (luego `izq=2`, `der=1`) |
| 3 | 2 | 1 | **no** | — | bucle termina |

`return xs` devuelve `[1, 2, 8, 5]`.

**El punto del ejercicio (aliasing + mutación in-place):** existe **un solo** objeto lista en todo el programa.
- `original = [5, 8, 2, 1]` crea ese objeto; `original` lo apunta.
- `copia = original` **no** copia: `copia` apunta al mismo objeto.
- `reordenar(copia)` recibe ese objeto como `xs`. El swap lo muta **in-place** (cambia posiciones dentro de la misma lista, no crea una nueva). `return xs` devuelve el mismo objeto.
- Por eso `resultado`, `copia` y `original` apuntan todos al mismo objeto mutado: las dos primeras líneas son idénticas, y `original is resultado` es `True`.

## Puntos resbalosos (donde el corrector debe mirar)
1. **`is` → `False`.** Es el error central. Quien cree que `=` copia, o que `return` crea una lista nueva, predice `False`. Aquí se separa quien entendió "nombres → objetos" de quien no.
2. **`original` "no debería cambiar".** Intuición de caja: "no toqué `original`". Pero `reordenar(copia)` mutó el objeto compartido; `original` lo ve.
3. **Swap mal trazado.** El intercambio simultáneo `xs[i], xs[j] = xs[j], xs[i]` evalúa el lado derecho primero; no hace falta variable temporal. Confundir el orden produce una lista mal invertida.
4. **Condición de parada del `while`.** Con 4 elementos hace exactamente 2 swaps; en la tercera evaluación `2 < 1` es falso y para. Off-by-one típico: hacer un swap de más (re-invierte) o de menos.

## Rango de soluciones aceptables
- Cualquier tabla que muestre el contenido de `xs` tras cada swap cuenta como `competente`, aunque agrupe columnas distinto (p. ej. una fila por swap, o anote también el estado intermedio dentro del swap).
- Para O3, vale cualquier redacción que nombre con precisión la idea de fondo: "un solo objeto, varios nombres" / "mutación in-place visible por el alias" / "`=` no copia". No se exige el término `id()` ni hablar de CPython.
- Variante de control para detectar dependencia-IA: si `reordenar` hiciera `xs = xs[::-1]` (reasigna el **nombre local**, no muta), entonces `original` quedaría intacto y `original is resultado` daría `False`. Un alumno con el modelo correcto explica esta diferencia; uno que dependió de la IA no la ve.
