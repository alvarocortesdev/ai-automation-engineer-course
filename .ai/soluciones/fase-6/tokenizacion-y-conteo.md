---
ejercicio_id: fase-6/tokenizacion-y-conteo
fase: fase-6
sub_unidad: "6.1"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como
> vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Tokenización: predice y verifica

## Respuesta canónica (la función)

```python
import tiktoken

def contar_tokens(texto: str, codificacion: str = "o200k_base") -> int:
    enc = tiktoken.get_encoding(codificacion)
    return len(enc.encode(texto))
```

- `enc.encode("")` devuelve `[]`, así que `len(...)` es `0`: el caso borde sale
  gratis, sin un `if` especial.
- "Contar tokens" es literalmente la longitud de la lista de IDs que produce
  `encode`. No hay que reimplementar nada a mano.

## Razonamiento paso a paso

El objetivo real no es la función (es trivial); es **romper la intuición
"1 palabra = 1 token"** con datos. Los conteos exactos dependen de la versión del
vocabulario, por eso los tests comparan contra `tiktoken` mismo en vez de fijar
números. Órdenes de magnitud esperados con `o200k_base` (aproximados — no exigir
el número exacto):

| Cadena | Tokens aprox. | Por qué |
|---|---|---|
| `"  "` (dos espacios) | 1 | espacios consecutivos son frecuentes |
| `"hello world"` | 2 | "hello" y " world" son tokens comunes |
| `"antidisestablishmentarianism"` | 5–7 | palabra larga y rara → se parte en sub-palabras |
| `"def suma(a, b): return a + b"` | 9–12 | identificadores + signos + espacios; el código suma muchos tokens |
| `"El murciélago ñoño comió crème brûlée"` | 15–20 | acentos/ñ/diéresis son varios bytes → más tokens por carácter |
| `"🎂🎂🎂"` | 3–6 | cada emoji ocupa varios bytes → no es 1 token |

Orden típico de menos a más: `"  "` < `"hello world"` < `"🎂🎂🎂"` ≈
`"antidisestablishmentarianism"` < `"def suma..."` < frase en español.
(El empate emoji/palabra-larga es legítimo que varíe; lo importante es la
intuición, no el desempate.)

## Puntos resbalosos (donde el corrector debe mirar)

1. **String vacío.** Debe dar 0. Si el alumno puso `if texto == "": return 0` no
   está mal, pero es innecesario — señal de que no probó que `encode("")` ya da `[]`.
2. **Predecir después de medir.** Si `prediccion.md` tiene los conteos exactos
   (incluido el emoji y el español), casi seguro se ejecutó primero. Invalida O1.
3. **tiktoken ≠ tokenizer universal.** Excelente si el alumno nota que estos
   conteos son de OpenAI y que Claude/Gemini darían otros números (y que por eso
   existe la API de token counting de Anthropic).
4. **La idea de fondo.** La reflexión `competente` nombra explícitamente una
   intuición rota: "palabras ≠ tokens", "el español cuesta más por los acentos",
   "el emoji no es 1 token", "el espacio cuenta y viaja pegado a la palabra".

## Rango de soluciones aceptables

- Usar `cl100k_base` en vez de `o200k_base` para explorar también es válido (da
  números distintos pero la intuición es la misma); el test lo cubre con ambas.
- Cualquier predicción con el **orden grueso** correcto y razonamiento cuenta como
  `competente`, aunque el desempate exacto difiera del de arriba.
- Para O3, cualquier reflexión que nombre con precisión **una** idea de fondo
  equivocada (no "fallé un número") es válida; no se exige una redacción concreta.
- Un test propio añadido (otra cadena borde, otra codificación) es señal de
  `excelente` en C2, no un requisito.
