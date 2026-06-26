---
ejercicio_id: fase-0/fundamentos-programacion-recursion-scope
fase: fase-0
sub_unidad: "0.7"
version: 1
---

# Rúbrica — Recursión y scope, trazados a mano

> Rúbrica analítica para un ejercicio **a-mano**. Lo que se evalúa es el **proceso de
> razonamiento** (la pila de llamadas, la explicación del scope), no solo si los tres números
> coinciden. Un alumno puede acertar las salidas por suerte y no entender; otro puede errar un
> número y tener un modelo mental casi correcto. La rúbrica distingue ambos casos.

## Objetivos evaluados
- **O1** — Predecir las tres salidas sin ejecutar.
- **O2** — Trazar la pila de `suma_hasta(4)` (bajada y subida).
- **O3** — Explicar el scope: por qué `print(x)` da `10`.

> Salidas correctas: `f(3)` → **6**, `print(x)` → **10**, `suma_hasta(4)` → **10**. (El corrector
> lo sabe; **no se lo dice al alumno** como atajo que evite la traza.)

## Criterios y niveles

### C1 — Corrección de las predicciones · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay predicción, o se ejecutó antes de predecir (la "predicción" es la salida copiada). |
| **en-progreso** | Predice con razonamiento pero erra por un malentendido sistemático (cree que `x` global vale `6`, o que `suma_hasta` no incluye `4`). |
| **competente** | Predice `6`, `10`, `10` con razonamiento coherente, aunque la traza tenga lagunas menores. |
| **excelente** | Predice las tres y anticipa los puntos resbalosos (caso base, shadowing) explicándolos. |

### C2 — Calidad de la pila de llamadas · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay pila, o solo el resultado `10` sin niveles intermedios. |
| **en-progreso** | Muestra la bajada (`4→3→2→1→0`) pero **no la subida** (cómo se resuelve cada nivel al volver), o salta el caso base. |
| **competente** | Pila completa: cada nivel con lo pendiente (`4 + suma_hasta(3)`, …), el caso base `suma_hasta(0)=0`, y la subida `0→1→3→6→10`. |
| **excelente** | Marca explícitamente el caso base como el punto donde "deja de bajar y empieza a subir", y nota que sin él sería `RecursionError`. |

### C3 — Explicación del scope (metacognición) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No explica el scope, o afirma que `print(x)` da `6`. |
| **en-progreso** | Dice "`x` no cambia" pero sin nombrar por qué (sin la idea de variable local vs. global). |
| **competente** | Explica que `x = n * 2` crea una `x` **local** que tapa (shadowing) la global, y que la global sigue en `10`. |
| **excelente** | Liga la explicación a la regla **LEGB** y/o contrasta con qué pasaría si `f` **mutara** una lista global en vez de reasignar un entero. |

## Errores típicos a marcar
- **Olvidar la subida de la pila**: registrar solo `4,3,2,1,0` sin mostrar cómo se suman al volver. Oculta justo el mecanismo de la recursión.
- **Caso base mal**: creer que `suma_hasta(4)` para en `1` (suma `4+3+2+1=10` por casualidad da igual, pero el modelo está mal) o que sigue indefinidamente.
- **`print(x)` → `6`**: la confusión #1 de scope; creer que asignar dentro de `f` cambia la global.
- **Off-by-one en la suma recursiva**: `4+3+2+1 = 10` vs. incluir/excluir el `0` (no cambia el total aquí, pero revela si trazó de verdad el caso base).
- **Ejecutar antes de predecir**: invalida O1 aunque el resto esté impecable.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- `prediccion.md` con las tres salidas correctas pero **sin pila** ni explicación de scope (resultado sin proceso).
- Explicación del scope con vocabulario muy por encima de F0 (closures, frames de CPython) que el alumno no puede aterrizar al ejemplo concreto de las dos `x`.
- Reflexión genérica que no menciona ni el caso base ni el shadowing.
- **Verificación sugerida:** pedir que prediga, sin ejecutar, `suma_hasta(5)` y qué imprimiría `print(x)` si dentro de `f` se hiciera `global x; x = n * 2`. Si trazó de verdad, lo resuelve; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca dar las salidas ni la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Tu pila baja bien hasta `0`, pero ahí se corta. ¿Qué valor le devuelve `suma_hasta(0)` a quien lo llamó, y qué hace ese nivel con ese valor?"
- **Pregunta socrática (nivel 2):** "Cuando asignas `x = n * 2` dentro de `f`, ¿estás creando una variable nueva o cambiando la de afuera? ¿Cómo lo sabrías sin ejecutar?"
- **Dirección concreta (nivel 3, solo tras intento real):** "El patrón a corregir es la **subida** de la recursión: el caso base no es el final del cálculo, es el punto donde empieza la vuelta. Reescribe la pila con dos columnas —'baja: qué queda pendiente' y 'sube: qué devuelvo'— y vuelve a predecir antes de ejecutar."

## Conexión con el proyecto / capstone
- Trazar a mano recursión y scope es el músculo que sostiene el **Capstone F0 — CLI sin IA**: depurar tu propio código sin debugger exige predecir qué hace cada llamada y qué variable vive dónde. Es también justo lo que mide un *live coding* (T0.3).
