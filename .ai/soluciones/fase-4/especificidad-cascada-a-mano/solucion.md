---
ejercicio_id: fase-4/especificidad-cascada-a-mano
fase: fase-4
sub_unidad: "4.1"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Especificidad y box model a mano

## Respuestas canónicas
- Primer `<p class="intro">` → **green**.
- Segundo `<p>` (sin clase) → **orange**.
- Ancho total del `.post`: **600px** con `border-box`; **652px** con `content-box`.

## Tabla de especificidad

| Selector | a (id) | b (clase/attr/pseudo-clase) | c (tipo/pseudo-elem) | terna |
|---|---|---|---|---|
| `p` | 0 | 0 | 1 | (0,0,1) |
| `article p` | 0 | 0 | 2 | (0,0,2) |
| `.intro` | 0 | 1 | 0 | (0,1,0) |
| `.post p` | 0 | 1 | 1 | (0,1,1) |
| `main .intro` | 0 | 1 | 1 | (0,1,1) |

## Razonamiento

**Primer `<p class="intro">`** — lo tocan las cinco reglas. La más alta no es única: `.post p` y `main .intro` **empatan** en `(0,1,1)`. Cuando la especificidad es idéntica, decide el **orden de origen**: `main .intro` está escrita **después** de `.post p`, así que gana → **green**. Este es el punto fino del ejercicio: solo aquí entra el orden.

**Segundo `<p>` (sin clase)** — `.intro` y `main .intro` **no** lo tocan (no tiene la clase). De las que sí lo tocan (`p` `(0,0,1)`, `article p` `(0,0,2)`, `.post p` `(0,1,1)`), la más específica es `.post p` por su columna `b` → **orange**. Sin empate: el orden no interviene.

## Box model del `.post`

`width: 600px; padding: 24px; border: 2px solid; margin: 0 auto;`

- Con `box-sizing: border-box` (el que está activo): el `width` **ya incluye** padding y border. Ancho total = **600px**. (El *content* interno se encoge a 600 − 24·2 − 2·2 = **548px**.)
- Con `content-box` (si se borra la línea de reset): el `width` es solo el content; se suman padding y border por fuera. Ancho total = 600 + 24·2 + 2·2 = **652px**.
- El `margin: 0 auto` **no** cuenta en el ancho de la caja: es espacio externo (y `auto` solo la centra horizontalmente).

## Puntos resbalosos (donde el corrector debe mirar)
1. **El empate del primer `<p>`.** Si el alumno no lo detecta y "predice green porque es la última", acertó por la razón equivocada — debe poder mostrar que `.post p` y `main .intro` empatan en `(0,1,1)` *antes* de invocar el orden.
2. **`article p` cuenta como 2 tipos, no como clase.** Error frecuente al armar la terna.
3. **Border-box vs content-box.** Dar 652px con el reset presente, o sumar el margin al ancho, son los dos deslices del box model.
4. **Verificar antes de predecir** invalida O1.

## Rango de soluciones aceptables
- Cualquier tabla que muestre las cinco ternas correctas y la comparación cuenta como `competente`, aunque el formato difiera.
- Para O3, cualquier reflexión que nombre con precisión la idea de fondo (el desempate por orden, o el border olvidado) es válida; no se exige una redacción concreta.
- Si el alumno expresa la regla de la cascada con sus palabras ("primero comparo especificidad, solo si empata miro quién va después") y calcula bien ambos anchos, es `excelente`.
