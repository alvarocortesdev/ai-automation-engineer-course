---
ejercicio_id: fase-0/notional-machine-parsons
fase: fase-0
sub_unidad: "0.3"
version: 1
---

# Rúbrica — Parsons: ordena la función `promedio`

> Rúbrica analítica para un ejercicio **mixto** (reordenar a mano → verificar con tests). El producto (tests verdes) importa, pero lo que de verdad se evalúa es si el alumno entiende **por qué** ese orden es el correcto: dependencias de datos y de control, e indentación como estructura. Tests verdes con un `orden.md` vacío o erróneo es solo media tarea.

## Objetivos evaluados
- **O1** — Reordenar las líneas (con indentación) hasta comportamiento correcto.
- **O2** — Justificar el orden por dependencias, no por estética.
- **O3** — Verificar con tests, incluido el caso borde de lista vacía.

> Orden correcto (vara del corrector; **no** se pega al alumno):
> ```python
> def promedio(numeros):
>     if not numeros:
>         return 0.0
>     total = 0
>     for n in numeros:
>         total = total + n
>     return total / len(numeros)
> ```

## Criterios y niveles

### C1 — Corrección del orden · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `solucion.py` no ejecuta (IndentationError, `NameError`, o el stub sin tocar). |
| **en-progreso** | Ejecuta pero falla algún test: típicamente `total = 0` después del `for` (→ `NameError`/resultado errado) o el guard de vacía mal ubicado (→ `ZeroDivisionError`). |
| **competente** | Orden correcto, todos los tests provistos en verde. |
| **excelente** | Además el alumno nota que el guard podría ir después de `total = 0` y argumenta por qué la posición elegida es más clara/segura (early return antes de tocar `len`). |

### C2 — Justificación por dependencias (`orden.md`) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `orden.md`, o solo describe el resultado sin razón ("las puse así"). |
| **en-progreso** | Justifica a medias: menciona que `return` va al final, pero no la dependencia `total = 0` → `for` que la usa. |
| **competente** | Explica las dependencias clave: `total = 0` antes del `for` que la consume; el `if` de vacía antes de dividir por `len`; indentación = qué vive dentro del bucle. |
| **excelente** | Distingue dependencia de **datos** (quién define `total`) de dependencia de **control** (el guard que evita la división) y lo nombra como tal. |

### C3 — Verificación y testing (hilo transversal) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No corrió los tests, o no agregó el test propio pedido. |
| **en-progreso** | Corrió los tests pero el test propio es trivial/duplicado (repite un caso ya cubierto). |
| **competente** | Tests provistos verdes + un test propio que cubre un caso nuevo real (negativos, decimales, un solo elemento). |
| **excelente** | El test propio expresa una aserción de **comportamiento** significativa (p. ej. promedio de negativos, o que el tipo sea `float`) y explica qué propiedad blinda. |

## Errores típicos a marcar
- **`total = 0` después del `for`**: rompe la dependencia de datos; `total` no existe cuando el bucle la usa.
- **Guard de lista vacía mal puesto** (o ausente): `total / len(numeros)` con lista vacía lanza `ZeroDivisionError`. El test del caso borde lo caza.
- **Indentación incorrecta**: poner el `if n > 0`/`total = total + n` fuera del `for`, o el `return` final dentro del bucle (retorna en la primera vuelta).
- **Perseguir tests verdes sin entender** (`orden.md` vacío): el alumno permutó hasta que pasó. Señal de que no construyó el modelo.
- (transversal) test propio que solo repite un caso existente en vez de aportar una aserción nueva.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Tests verdes pero `orden.md` ausente o genérico (no menciona dependencias concretas) → reordenó por prueba y error o pidió la respuesta.
- El test propio tiene un estilo o sofisticación impropios de F0 (fixtures, `parametrize` avanzado) sin poder explicar la sintaxis.
- **Verificación sugerida:** dar una variante con una línea distractora extra (p. ej. `total = total * 2` suelta) y pedir que arme la función correcta descartándola. Quien entendió las dependencias la rechaza; quien dependió de la IA la incluye.

## Feedback sugerido (graduado)
> Nunca pegar el orden correcto antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Un test revienta con `ZeroDivisionError` en la lista vacía. ¿Qué línea protege esa división, y está ejecutándose **antes** de dividir?"
- **Pregunta socrática (nivel 2):** "¿Qué línea *usa* `total`? ¿Puede ir antes que la línea que crea `total`? ¿Qué te dice la indentación sobre qué se ejecuta una vez por elemento y qué una sola vez?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Ordena por **dependencias**: primero la firma `def`, luego el *early return* del caso vacío, luego la inicialización del acumulador, luego el bucle que lo llena, y al final el cálculo que lo consume. La indentación define qué está dentro del `for`."

## Conexión con el proyecto / capstone
- Razonar el orden y la indentación por dependencias es la base de escribir funciones correctas a la primera en el **Capstone F0 — CLI sin IA**, donde no hay IA que reordene por ti. El hábito de cerrar con un test del caso borde es el primer eslabón del hilo de **testing** que recorre todo el curso.
