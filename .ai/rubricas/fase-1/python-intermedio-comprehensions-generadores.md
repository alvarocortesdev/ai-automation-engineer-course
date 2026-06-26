---
ejercicio_id: fase-1/python-intermedio-comprehensions-generadores
fase: fase-1
sub_unidad: "1.2"
version: 1
---

# Rúbrica — Procesar transacciones con comprehensions y un generador

> Rúbrica analítica atada a los `objetivos` del contrato. Evalúa el **código** y la **comprensión**
> detrás, no solo el verde de los tests. Un alumno puede pasar los tests con un `for`/`append`
> disfrazado o con una lista en vez de un generador; la rúbrica lo detecta.

## Objetivos evaluados
- **O1** — Reescribir una transformación/filtrado como `set` y `dict` comprehension.
- **O2** — Implementar un **generador** (`yield`) que produce de a uno, en orden, sin materializar.
- **O3** — Explicar el trade-off de la evaluación perezosa (memoria/streaming) vs. la lista.

> Resultado esperado: `categorias_unicas` → `set` con categorías distintas; `indexar_por_id` →
> `dict` id→transacción; `stream_montos` → **generador** que produce los montos `>= minimo` en
> orden. (El corrector lo sabe; no se lo entrega al alumno como atajo.)

## Criterios y niveles

### C1 — Corrección: usa la herramienta correcta · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No corre, o `stream_montos` devuelve una lista (los tests de generador fallan), o las comprehensions no producen el contenedor pedido. |
| **en-progreso** | Las tres funciones dan el valor correcto, pero `categorias_unicas`/`indexar_por_id` están escritas con `for`+`append`/asignación en vez de comprehension (cumplen el resultado, no el objetivo). |
| **competente** | `categorias_unicas` es set comprehension, `indexar_por_id` es dict comprehension, `stream_montos` usa `yield`; todos los tests pasan. |
| **excelente** | Además, el alumno puede justificar por qué `set`/`dict` (no `list`) y por qué generador; maneja con naturalidad la lista vacía sin un `if` especial. |

### C2 — Comprensión del generador (lazy) · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Cree que un generador es "una lista más rápida"; no distingue `yield` de `return [...]`. |
| **en-progreso** | Usa `yield` pero no puede explicar la evaluación perezosa ni por qué se agota tras una pasada. |
| **competente** | Explica que el generador produce de a uno y no carga todo en memoria; reconoce que se consume una sola vez. |
| **excelente** | Conecta con un caso real (streaming de tokens de un LLM, archivo enorme) y sabe que el generador no es indexable ni reutilizable. |

### C3 — Calidad de tests · mapea: O1–O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No agregó test propio, o el agregado no corre. |
| **en-progreso** | Test propio trivial (repite un caso existente). |
| **competente** | Test borde nuevo y razonable (id repetido, monto igual al `minimo`, una sola transacción) con aserción precisa. |
| **excelente** | Test que verifica una propiedad del generador (p. ej. que `next()` avanza de a uno, o que no se materializó). |

## Errores típicos a marcar
- **`stream_montos` con `return [m for m in ...]`**: es una lista, no un generador; `inspect.isgenerator` falla. El contrato pide `yield`.
- **`for`+`append` donde se pedía comprehension**: pasa los tests pero no cumple el objetivo O1; márcalo.
- **Romper el orden** en `stream_montos` (p. ej. ordenar o usar un `set` intermedio): debe respetar el orden de entrada.
- **Olvidar la lista vacía**: `categorias_unicas([])` debe ser `set()`, no `{}` (eso es un dict vacío) ni error.
- **Comprehension de solo escritura**: anidar de más cuando un `for` sería más legible (aplica si el alumno "se pasó de listo").
- (transversal/testing) test propio que solo replica el ejemplo del enunciado.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Código idiomático perfecto (generator expressions, walrus, etc.) pero **no puede explicar** por qué `stream_montos` no debería devolver una lista.
- Usa `defaultdict` o trucos avanzados que no calzan con el nivel de la lección y no sabe defender.
- **Verificación sugerida:** pide que prediga, sin ejecutar, qué imprime `g = stream_montos(datos, 0); print(list(g)); print(list(g))`. Si entiende generadores, dice "la segunda lista sale vacía"; si copió, duda.

## Feedback sugerido (graduado)
> Nunca pegar la solución de referencia ni el código completo.
- **Pista (nivel 1):** "Dos de tus funciones construyen un contenedor a partir de otro: eso es justo lo que una comprehension expresa en una línea. La tercera no debe construir nada."
- **Pregunta socrática (nivel 2):** "Si `transacciones` tuviera 10 millones de elementos, ¿cuál de tus tres funciones haría que el programa se quede sin memoria, y por qué?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Reescribe `categorias_unicas` como `{...}` y `indexar_por_id` como `{clave: valor for ...}`. Para `stream_montos`, recorre con un `for` y `yield` el monto cuando cumpla el filtro: no acumules en una lista. No te doy el código."

## Conexión con el proyecto / capstone
- Transformar el *payload* de la mini-API del **Capstone F1** en su respuesta JSON es exactamente este trabajo de comprehensions; el generador es la base del *streaming* que verás en frontend y en la Fase 6.
