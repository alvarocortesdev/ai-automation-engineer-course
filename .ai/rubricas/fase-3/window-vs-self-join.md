---
ejercicio_id: fase-3/window-vs-self-join
fase: fase-3
sub_unidad: "3.2"
version: 1
---

# Rúbrica — Reemplaza el self-join: window functions sobre transacciones

> Rúbrica **analítica** atada a los `objetivos`. Lo central no es que las tres queries devuelvan la
> tabla esperada, sino que el alumno **entienda y defienda** que la window function reemplaza al
> self-join (objetivo O3). Una query que pasa la verificación con un self-join correlacionado en (B)
> es correcta en resultado pero **no** cumple el objetivo. La rúbrica separa "da el resultado" de
> "usó y entendió la herramienta correcta".

## Objetivos evaluados
- **O1** — Window de agregación (`SUM OVER`) para saldo acumulado por grupo sin colapsar filas.
- **O2** — "Lo último por grupo" con `ROW_NUMBER()` filtrado en subquery/CTE.
- **O3** — Explicar por qué la window reemplaza al self-join O(n²).

## Criterios y niveles

### C1 — Corrección (¿las queries dan los resultados esperados?) · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Alguna query no corre, o (A) colapsa las filas (devuelve 3 en vez de 6), o (B) devuelve más de una fila por cuenta. |
| **en-progreso** | Resultados correctos pero (B) entregada con self-join/correlacionada (cumple el resultado, no el objetivo O2/O3), o (A) usa un total no corriente. |
| **competente** | Las 3 queries dan exactamente las tablas esperadas; (A) conserva 6 filas con saldo corriente; (B) usa `ROW_NUMBER()` filtrado afuera; (C) usa `LAG` con NULL en la primera de cada cuenta. |
| **excelente** | (B) resuelve bien el caso de empate (entiende que `ROW_NUMBER` garantiza una sola fila) y/o añade un desempate explícito en el `ORDER BY`; etiqueta y comenta las queries. |

### C2 — Uso correcto de la window function · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Intenta `WHERE ROW_NUMBER() OVER (...) = 1` en el mismo nivel (error de SQL) o no usa `PARTITION BY`. |
| **en-progreso** | Usa window pero confunde el marco (p. ej. `SUM OVER (PARTITION BY ...)` sin `ORDER BY` → da el total de la cuenta repetido, no el corriente). |
| **competente** | `PARTITION BY` + `ORDER BY` correctos; el `WHERE rn = 1` va en una subquery/CTE externa. |
| **excelente** | Explicita el marco (`ROWS UNBOUNDED PRECEDING`) o explica por qué el default con `ORDER BY` ya da el total corriente; usa CTE por legibilidad. |

### C3 — Comprensión demostrada (`NOTAS.md` calza con el SQL) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `NOTAS.md`, o no menciona costo/complejidad. |
| **en-progreso** | Dice "la window es más rápida" sin explicar por qué (no cuenta pasadas ni nombra el bucle anidado). |
| **competente** | Explica que la correlacionada re-escanea la tabla por cada fila (≈O(n²)) y la window hace una pasada ordenada; lo liga al bucle anidado de DSA. |
| **excelente** | Además explica por qué `WHERE rn = 1` no puede ir en el nivel que calcula `rn` (orden de evaluación: window después del WHERE) y reconoce que en datos chicos la diferencia no se nota pero a escala sí. |

## Errores típicos a marcar
- **Entrega (B) con self-join/correlacionada** y la da por buena: resultado correcto, objetivo O2/O3 sin cumplir. Es el error central.
- **`SUM(monto) OVER (PARTITION BY cuenta_id)` sin `ORDER BY`** en (A): devuelve el total de la cuenta repetido en cada fila, no el saldo corriente.
- **`WHERE ROW_NUMBER() OVER (...) = 1`** directo: error de SQL; las window functions no se filtran en el WHERE.
- **`GROUP BY cuenta_id` con `MAX(fecha)` en (B)** y luego un JOIN para traer el monto: duplica si hay empate y no es lo pedido.
- (transversales) `NOTAS.md` que dice "más eficiente" sin contar pasadas; no conecta con el O(n²) ni con el N+1 de la Fase 3.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- SQL impecable con `ROWS BETWEEN ...` explícito pero `NOTAS.md` que no puede explicar por qué la window es más barata (sofisticación indefendible).
- (B) resuelta con window pero el alumno no sabe responder "¿qué pasa si dos transacciones comparten la fecha máxima?".
- Comentarios genéricos que no calzan con el SQL entregado.
- **Verificación sugerida:** pedir que explique, en voz alta, por qué `WHERE rn = 1` tuvo que ir en una subquery. Quien entendió habla del orden de evaluación (window después del WHERE); quien dependió de la IA se traba.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Tu (B) funciona, pero ¿cuántas veces lee la tabla? Si la subquery interna se evalúa por cada fila, estás en O(n²). ¿Puedes numerar las filas de cada cuenta en **una** pasada?"
- **Pregunta socrática (nivel 2):** "Si numeras las transacciones de cada cuenta del más reciente al más viejo, ¿con cuál te quedas? ¿Y por qué ese `WHERE rn = 1` no puede vivir en el mismo SELECT que crea `rn`?"
- **Dirección concreta (nivel 3, solo tras intento real):** "El patrón es: `ROW_NUMBER() OVER (PARTITION BY cuenta_id ORDER BY fecha DESC)` en una subquery, y afuera `WHERE rn = 1`. En `NOTAS.md`, cuenta las pasadas de ambas versiones para que el trade-off de costo quede explícito y conéctalo con el N+1 que verás en 3.5."

## Conexión con el proyecto / capstone
- El salto self-join → window function es el mismo refactor de rendimiento que aparece detrás de los endpoints de listado del **Capstone F3 — API de producción**, y es el germen del **problema N+1** (3.5): el bucle anidado escondido, ahora en consultas a la base. Documentarlo como ADR ("elegí window sobre N+1 queries porque pasa de O(n²) a una pasada") es trabajo de semi-senior.
