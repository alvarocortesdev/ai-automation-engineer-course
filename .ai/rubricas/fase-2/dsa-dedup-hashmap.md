---
ejercicio_id: fase-2/dsa-dedup-hashmap
fase: fase-2
sub_unidad: "2.1"
version: 1
---

# Rúbrica — De O(n²) a O(n): two-sum con hashmap

> Rúbrica **analítica** atada a los `objetivos` del contrato. Lo que se evalúa no es solo que la
> función pase los tests, sino que el alumno **entienda y defienda** la mejora de complejidad. Un
> alumno puede pasar todos los tests con un bucle anidado O(n²) y aun así **no** cumplir el objetivo
> central (la versión rápida). La rúbrica separa "pasa los tests" de "entendió el porqué".

## Objetivos evaluados
- **O1** — Implementar en O(n) el two-sum booleano usando un `set`.
- **O2** — Estimar y justificar la Big-O (tiempo y espacio) de la versión O(n²) vs la O(n).
- **O3** — Explicar el space–time trade-off (memoria del `set` a cambio de lookup O(1)).

## Criterios y niveles

### C1 — Corrección (¿hace lo que el objetivo pide?) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | La función falla casos del enunciado, o no maneja `[3, 3]→6=True` / `[1]→2=False` (el matiz de "dos posiciones distintas"). |
| **en-progreso** | Pasa los tests pero la solución es O(n²) (bucle anidado) — funciona pero no cumple el objetivo de complejidad. |
| **competente** | Pasa todos los casos con una solución **O(n)**: un solo recorrido y lookups en `set`. |
| **excelente** | Además agregó casos borde propios significativos (negativos, ceros repetidos, valor que es la mitad del objetivo una sola vez) y los tests siguen verdes. |

### C2 — Calidad de ingeniería (tests reales, manejo de casos) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay tests propios, o los tests no afirman nada útil (no podrían fallar). |
| **en-progreso** | Tests presentes pero solo del camino feliz; no cubre el caso de "no empareja consigo mismo". |
| **competente** | Tests con `parametrize`, cubren casos positivos y negativos, e incluyen al menos un caso borde propio. |
| **excelente** | Escribió el test **antes** del código (se nota en el historial o lo declara), y los nombres describen el comportamiento. |

### C3 — Comprensión demostrada (el `NOTAS.md` calza con el código) · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `NOTAS.md`, o no menciona complejidad. |
| **en-progreso** | Da la Big-O de una sola versión, o confunde tiempo con espacio, o dice "O(n) porque es rápido" sin razonar. |
| **competente** | Da tiempo **y** espacio de ambas versiones correctamente: O(n²)/O(1) vs O(n)/O(n), y dice por qué el `set` baja el tiempo. |
| **excelente** | Nombra el trade-off como tal (space–time), explica que el lookup es O(1) **amortizado** por la tabla hash, y reconoce cuándo el `set` *no* valdría la pena (n muy chico). |

## Errores típicos a marcar
- **Entrega la versión O(n²)** y la da por buena: pasa los tests pero no cumple O1. Es el error central.
- **Empareja un elemento consigo mismo**: agregar `x` al `set` *antes* de preguntar por el complemento, dando `[1]→2=True` (incorrecto). El orden es preguntar-luego-agregar.
- **Usa `nums.count()` o `in` sobre la lista** dentro del bucle: eso reintroduce un O(n) interno → vuelve a O(n²) disfrazado.
- **Confunde la Big-O de espacio**: decir que la versión con `set` es O(1) de espacio (ignora que el `set` puede crecer a `n`).
- (transversales) `NOTAS.md` que dice "O(n) porque usa set" sin contar operaciones; no reconoce que para `n` pequeño el O(n²) podría bastar.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Solución O(n) impecable pero `NOTAS.md` que no puede explicar **por qué** el lookup es O(1) (resultado sin razonamiento).
- Vocabulario sofisticado (hablar de "load factor", "rehashing", "open addressing") sin poder explicar el caso simple de "un solo recorrido vs comparar todos con todos".
- Tests que parecen autogenerados (cubren combinaciones raras pero ninguno el caso clave `[3,3]→6`).
- **Verificación sugerida:** pedir que, en voz alta, explique qué pasaría con la complejidad si reemplazara el `set` por una `list` y usara `in`. Si entendió, dice "vuelve a O(n²)"; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Tu solución funciona. ¿Cuántas veces miras cada elemento? Si la respuesta es 'una vez por cada otro elemento', estás en O(n²). ¿Puedes mirar cada uno **una sola vez**?"
- **Pregunta socrática (nivel 2):** "Si por cada `x` pudieras preguntar instantáneamente '¿ya vi `objetivo - x`?', ¿qué estructura hace esa pregunta en O(1)? ¿Y en qué orden debes preguntar y agregar para no emparejar `x` consigo mismo?"
- **Dirección concreta (nivel 3, solo tras intento real):** "El patrón es 'recordar lo visto en un `set` y buscar el complemento'. Un solo recorrido, lookup O(1), pregunta antes de agregar. Reescribe tu `NOTAS.md` contando las operaciones de ambas versiones para que el trade-off quede explícito."

## Conexión con el proyecto / capstone
- Este salto O(n²)→O(n) con un índice (`dict`/`set`) es exactamente el refactor de rendimiento que aparece en el **Capstone F2** (y que se documenta como ADR). Es también el germen del **problema N+1** de la Fase 3: el mismo bucle anidado, escondido en consultas a la base de datos.
