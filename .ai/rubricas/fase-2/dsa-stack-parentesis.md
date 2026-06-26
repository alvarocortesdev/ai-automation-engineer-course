---
ejercicio_id: fase-2/dsa-stack-parentesis
fase: fase-2
sub_unidad: "2.1"
version: 1
---

# Rúbrica — Reconoce el stack: paréntesis balanceados

> Rúbrica **analítica** atada a los `objetivos` del contrato. El núcleo evaluable no es apilar y
> desapilar, sino que el alumno **reconozca** que el anidamiento exige un stack y pueda explicar por
> qué contar símbolos no basta. Un alumno puede pasar varios casos con un truco de conteo y fallar el
> caso `([)]` — esa falla revela que no entendió el patrón.

## Objetivos evaluados
- **O1** — Reconocer un problema de anidamiento como un caso de stack (LIFO) y resolverlo en O(n).
- **O2** — Implementar un stack con una `list` (`append`/`pop`) y manejar el cierre con stack vacío.
- **O3** — Explicar por qué contar símbolos no basta y el orden de cierre exige un stack.

## Criterios y niveles

### C1 — Corrección (¿hace lo que el objetivo pide?) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Falla casos básicos, o resuelve "contando" (mismo número de aperturas y cierres) y por eso da `([)]→True` (incorrecto). |
| **en-progreso** | Usa stack pero falla un borde: cierre con stack vacío revienta con `IndexError`, o no exige stack vacío al final (`"(()"→True`). |
| **competente** | Pasa todos los casos del enunciado con un stack, incluido `([)]→False` y los bordes de apertura/cierre sueltos. |
| **excelente** | Agregó casos borde propios (anidamiento profundo, solo caracteres no-paréntesis), y la verificación del par usa un `dict` (lookup O(1)) en lugar de varios `if`. |

### C2 — Calidad de ingeniería (tests reales, manejo de errores) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin tests propios, o la función puede lanzar `IndexError` en una entrada válida. |
| **en-progreso** | Tests solo del camino feliz; no prueba el cierre con stack vacío ni la apertura sin cerrar. |
| **competente** | Tests parametrizados con casos positivos y negativos, incluido un caso borde propio; maneja el stack vacío con elegancia (devuelve `False`, no excepción). |
| **excelente** | Nombres de test descriptivos; cubre explícitamente el caso `IndexError` evitado y declara haber escrito el test antes. |

### C3 — Comprensión demostrada (`NOTAS.md` calza con el código) · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `NOTAS.md`, o no menciona por qué un stack. |
| **en-progreso** | Da la complejidad pero no explica por qué el stack es necesario (o dice "porque sí"). |
| **competente** | Da O(n) tiempo / O(n) espacio y explica que el stack recuerda **el orden** de apertura, por eso detecta `([)]`. |
| **excelente** | Conecta con el patrón general: "anidamiento / undo / DFS = stack", y nota que el peor caso de espacio es un string todo de aperturas. |

## Errores típicos a marcar
- **Contar en vez de apilar**: comparar cantidad de `(` con `)`. Da `([)]→True`, el error revelador.
- **`IndexError` en cierre con stack vacío**: hacer `pila.pop()` sin comprobar `if not pila` primero.
- **Olvidar el chequeo final**: no exigir que el stack quede vacío, dando `"(()"→True`.
- **Tres stacks separados** (uno por tipo de símbolo): pierde el orden de anidamiento entre tipos; `([)]` vuelve a fallar.
- (transversales) tests que no incluyen ningún caso `False` de anidamiento cruzado; confiar en que "si compila, está bien".

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Solución correcta con `dict` de pares pero `NOTAS.md` que no explica por qué `([)]` necesita stack (resultado sin comprensión).
- Manejo de casos exóticos que el enunciado no pide (Unicode, paréntesis angulares) mientras falla en explicar el caso simple.
- **Verificación sugerida:** pedir que prediga, a mano, qué hace su código con `"([)]"` paso a paso (estado del stack en cada carácter). Quien entendió el stack lo traza sin problema; quien dependió de la IA no reconstruye el estado.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Traza `([)]` a mano: ¿cuántas aperturas y cuántos cierres hay? Si tu método solo cuenta, ¿cómo distingue `([)]` de `([])`? Mira qué se cierra y en qué orden."
- **Pregunta socrática (nivel 2):** "Cuando llega un `)`, ¿qué apertura *debería* estar esperándolo? ¿Dónde guardarías 'la última apertura sin cerrar' para consultarla? ¿Qué estructura te da 'lo último que metí' primero?"
- **Dirección concreta (nivel 3, solo tras intento real):** "El patrón es un stack: apila las aperturas; en cada cierre, compara con la **cima** (y maneja el caso de stack vacío). Balanceado solo si el stack queda vacío al final. Tu `([)]` falla porque al cerrar `)` la cima es `[`, no `(`."

## Conexión con el proyecto / capstone
- El stack es la base de los recorridos en profundidad (DFS) y del parsing — herramientas que reaparecen al leer estructuras anidadas (JSON, ASTs) en fases posteriores. Reconocer "esto es un stack" es la habilidad que el **Capstone F2** premia al refactorizar lógica de validación enredada en una estructura clara.
