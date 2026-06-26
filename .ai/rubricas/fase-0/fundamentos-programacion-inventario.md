---
ejercicio_id: fase-0/fundamentos-programacion-inventario
fase: fase-0
sub_unidad: "0.7"
version: 1
---

# Rúbrica — Resumen de gastos por categoría

> Rúbrica analítica atada a los `objetivos` del contrato. Evalúa el **código entregado** y la
> **comprensión** detrás de él, no solo el verde de los tests. Un alumno puede pasar los tests
> copiando de una IA sin entender; la rúbrica lo detecta.

## Objetivos evaluados
- **O1** — Implementar una función que recorra una lista y **agrupe/sume** por clave en un `dict`.
- **O2** — **Validar** entradas y lanzar `ValueError` ante datos inválidos.
- **O3** — Manejar el **caso borde** de la lista vacía.

> Resultado esperado: agrupa y suma; lista vacía → `{}`; monto negativo/ausente o categoría
> vacía/ausente → `ValueError`. (El corrector lo sabe; no se lo entrega al alumno como atajo.)

## Criterios y niveles

### C1 — Corrección: agrupa y suma · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No agrupa (devuelve una lista, o sobrescribe en vez de sumar), o no corre. |
| **en-progreso** | Suma pero falla en algo: pierde el primer gasto de cada categoría, o usa un `dict` mal inicializado dentro del bucle. |
| **competente** | Agrupa y suma correctamente; los tests de agrupación y `float` pasan. |
| **excelente** | Además usa `dict.get(clave, 0)` (o equivalente idiomático) en vez de un `if clave in d` redundante, y lo puede justificar. |

### C2 — Validación y manejo de errores · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No valida: un monto negativo se suma en silencio, o una categoría vacía crea una clave `""`. |
| **en-progreso** | Valida algo pero no todo (p. ej. atrapa el negativo pero no la categoría ausente), o usa `assert` en vez de `raise ValueError`. |
| **competente** | Lanza `ValueError` en ambos casos inválidos, **antes** de acumular, con un mensaje legible. |
| **excelente** | Mensaje de error que incluye el valor culpable (`f"...{monto!r}"`) y valida con cuidado los casos sutiles (monto `None`, categoría `None`). |

### C3 — Caso borde y calidad de tests · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Lista vacía revienta (índice, `KeyError`) o no agregó ningún test propio. |
| **en-progreso** | Maneja la lista vacía pero el test propio es trivial (repite uno existente) o no aporta. |
| **competente** | Lista vacía → `{}`; agregó un test borde **nuevo** y razonable. |
| **excelente** | El test propio cubre un borde real no obvio (categoría con tilde, monto `0`, muchas categorías) y tiene una aserción precisa. |

## Errores típicos a marcar
- **Inicializar el `dict` acumulador dentro del bucle**: lo reinicia en cada vuelta → solo queda el último gasto.
- **No usar `.get`**: `conteo[cat] += monto` sin inicializar revienta con `KeyError` en el primer gasto de cada categoría.
- **Validar después de sumar**: suma el negativo y *luego* intenta lanzar — el dato malo ya contaminó el total.
- **`except`/`assert` en vez de `raise ValueError`**: `assert` se desactiva con `python -O` y no es el contrato pedido.
- **Confundir `print` con `return`**: la función "muestra" el resultado pero devuelve `None` → todos los tests fallan con `assert None == {...}`.
- (transversal/testing) tests que solo replican el ejemplo del enunciado sin un borde propio.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Solución idiomática y compacta (defaultdict, comprehensions) pero el alumno **no puede explicar** por qué `.get(clave, 0)` evita el `KeyError`.
- Manejo de errores sofisticado (jerarquía de excepciones propia) impropio del nivel F0 y que no sabe defender.
- Tests "propios" que claramente no escribió (estilo distinto, nombres ingleses cuando el resto está en español).
- **Verificación sugerida:** pedir que, sin ejecutar, prediga qué devuelve su función con `[]` y con un gasto de `monto: 0`; y que explique en una frase por qué validar **antes** de acumular. Si lo escribió de verdad, lo resuelve al toque.

## Feedback sugerido (graduado)
> Nunca pegar la solución de referencia ni el código completo.
- **Pista (nivel 1):** "Tu función pierde gastos / revienta en la primera categoría nueva. Mira cómo creas la clave la **primera** vez que ves una categoría."
- **Pregunta socrática (nivel 2):** "¿En qué momento exacto decides que un gasto es inválido: antes o después de sumarlo? ¿Qué pasa con el total si decides después?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Separa dos pasos por gasto: primero **validar** (y lanzar `ValueError` si algo falla), luego **acumular** con un `dict` inicializado fuera del bucle, usando `.get(clave, 0)` para el primer gasto de cada categoría. No te doy el código: reescríbelo con esa estructura."

## Conexión con el proyecto / capstone
- Esta es la forma canónica de una función del **Capstone F0 — CLI sin IA**: recibir datos, recorrer, agrupar, rechazar lo inválido. Dominarla aquí es construir el capstone por adelantado.
