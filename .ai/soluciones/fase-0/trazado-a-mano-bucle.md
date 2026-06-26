---
ejercicio_id: fase-0/trazado-a-mano-bucle
fase: fase-0
sub_unidad: "0.3"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Trazado a mano de un bucle anidado

## Respuesta canónica
`misterio(4)` devuelve **10**.

## Razonamiento paso a paso

`range(1, n + 1)` con `n = 4` ⇒ `i` toma `1, 2, 3, 4`.
`range(i)` ⇒ `j` toma `0, 1, …, i-1` (no incluye `i`).
`fila = 0` está **dentro** del bucle externo: se reinicia en cada `i`.

Tabla de traza (estado al cerrar cada vuelta del externo):

| i | j recorre | fila (suma de j) | total acumulado |
|---|-----------|------------------|-----------------|
| 1 | 0         | 0                | 0               |
| 2 | 0, 1      | 0+1 = 1          | 0+1 = 1         |
| 3 | 0, 1, 2   | 0+1+2 = 3        | 1+3 = 4         |
| 4 | 0, 1, 2, 3| 0+1+2+3 = 6      | 4+6 = 10        |

`return total` ⇒ **10**.

> Nota: `fila` para cada `i` es la suma `0..i-1`, y `total` es la suma de esas filas. Es decir `total = Σ_{i=1..n} (i-1)·i/2`; para `n=4`: 0+1+3+6 = 10.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Reinicio de `fila`.** Si el alumno no lo reinicia mentalmente, arrastra: 0 → 0+1=1 → 1+(0+1+2)=4… y suele terminar en un total inflado. Es el error #1.
2. **`range(i)` = `0..i-1`.** Confundirlo con `1..i` o `0..i` mete un término de más/menos por fila.
3. **`range(1, n+1)` incluye `n`.** El externo llega hasta `i = 4`, no `3`.

## Rango de soluciones aceptables
- Cualquier tabla de traza que muestre los valores intermedios correctos cuenta como `competente`, aunque agrupe columnas distinto (p. ej. una fila por iteración del **interno** en vez de por iteración del externo) — siempre que el desglose de `fila` sea visible.
- La predicción puede expresarse como fórmula (`Σ (i-1)i/2`) en vez de tabla numérica: si es correcta y está justificada, es `excelente`.
- Para `O3`, cualquier reflexión que nombre con precisión la idea de fondo (reinicio del acumulador, o el rango de `range`) es válida; no se exige una redacción concreta.
