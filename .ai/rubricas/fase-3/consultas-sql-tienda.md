---
ejercicio_id: fase-3/consultas-sql-tienda
fase: fase-3
sub_unidad: "3.1"
version: 1
---

# Rúbrica — Escribe SQL contra una base que corre

> Rúbrica **analítica** atada a los `objetivos` del contrato. El test verde es necesario pero no
> suficiente: lo que se evalúa es que el alumno **entienda** lo que escribió (por qué `GROUP BY` deja
> ciertas columnas y no otras, por qué el `WHERE` no es opcional en `UPDATE`/`DELETE`). Un alumno puede
> pegar SQL de la IA y pasar los tests sin entender; la rúbrica busca esa señal.

## Objetivos evaluados
- **O1** — Escribir SELECT correctos con WHERE, ORDER BY + LIMIT y GROUP BY con agregados.
- **O2** — Escribir INSERT/UPDATE/DELETE con el WHERE correcto, sin tocar filas de más.
- **O3** — Predecir el resultado de cada consulta antes de ejecutarla (notional machine de SQL).

## Criterios y niveles

### C1 — Corrección de las consultas de lectura (q1–q4) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | q1–q4 no pasan, o hay `SELECT *` donde se pedían columnas específicas, o el `GROUP BY` agrupa por la columna equivocada. |
| **en-progreso** | Pasan algunas pero no todas: típicamente falla q2 (no respeta el orden o el `LIMIT`) o q3/q4 (cuenta/suma mal, o selecciona una columna no agregada). |
| **competente** | q1–q4 verdes: WHERE con `AND` correcto, ORDER BY DESC + LIMIT 3, GROUP BY con COUNT y SUM bien aplicados. |
| **excelente** | Además usa alias legibles (`AS total`, `AS suma_stock`) y devuelve exactamente las columnas pedidas en el orden pedido, sin extras. |

### C2 — Corrección y prudencia de las escrituras (q5–q7) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | q5 escribe el `id` a mano, o q6/q7 no llevan `WHERE` (tocan toda la tabla), o no pasan. |
| **en-progreso** | Pasan pero con descuidos: `INSERT` sin listar columnas, o `UPDATE` que fija un precio absoluto en vez de `precio + 1000`. |
| **competente** | q5 omite el `id` y lista columnas; q6 usa `precio = precio + 1000` con `WHERE categoria = 'cables'`; q7 `DELETE ... WHERE stock = 0`. Las tres verdes. |
| **excelente** | Dejó el `SELECT` de verificación (comentado) con el mismo `WHERE` antes de cada verbo destructivo —evidencia del hábito de "mirar antes de tocar". |

### C3 — Comprensión demostrada (predicción + defensa) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No predijo resultados; no sabe explicar por qué una consulta da lo que da. |
| **en-progreso** | Predice resultados simples (q1) pero no los de agregación (q3/q4) ni por qué. |
| **competente** | Puede explicar qué hace cada consulta y por qué `GROUP BY categoria` permite `COUNT(*)` pero no `nombre`. |
| **excelente** | Explica además por qué una tabla no tiene orden garantizado sin `ORDER BY`, y la diferencia entre filtrar filas (`WHERE`) y filtrar grupos (`HAVING`). |

## Errores típicos a marcar
- **q3/q4: poner `nombre` (u otra columna no agregada) en el `SELECT` junto al `GROUP BY`** → en SQLite "funciona" devolviendo un valor arbitrario del grupo; es un error de lógica que PostgreSQL rechazaría.
- **q2: olvidar `DESC`** (da los 3 más baratos) o **olvidar `LIMIT`** (devuelve todo ordenado).
- **q6: usar `SET precio = 1000`** en vez de `precio = precio + 1000` (sobrescribe en vez de incrementar).
- **q6/q7 sin `WHERE`** → toca toda la tabla. Error caro y real; marcar siempre.
- **q5 con `id` explícito** → frágil; el `id` lo asigna la base.
- **Comparar `NULL` con `=`** (no aplica a este dataset, pero si aparece, marcarlo: se usa `IS NULL`).
- (transversales) pasar los tests sin poder explicar ni una consulta; no predijo nada antes de correr.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Las 7 consultas perfectas y "de una", pero el alumno no puede decir qué devolvería q3 si cambiara `COUNT(*)` por `COUNT(stock)`, ni por qué.
- Uso de construcciones por encima del nivel (CTE, window functions, subconsultas correlacionadas) en un ejercicio de SQL básico, sin poder explicar la versión simple.
- Ausencia total de predicciones o de los `SELECT` de verificación, pese a que el enunciado los pide.
- **Verificación sugerida:** pedir, en voz alta, que prediga el resultado de `SELECT categoria, COUNT(*) FROM productos WHERE stock = 0 GROUP BY categoria` sin ejecutarlo. Quien entendió responde (`periféricos` 1, `cables` 1); quien dependió de la IA, no puede.

## Feedback sugerido (graduado)
> Nunca dar la consulta resuelta antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Para q3, ¿sobre qué columna quieres agrupar para contar? Y una vez agrupado por esa columna, ¿qué tiene sentido pedir en el `SELECT` además de ella: una columna suelta o un agregado?"
- **Pregunta socrática (nivel 2):** "Si `GROUP BY categoria` colapsa todos los productos de 'periféricos' en una sola fila de resultado, ¿qué `nombre` debería mostrar esa fila? ¿Ves por qué solo tiene sentido pedir la categoría y una función que resuma el grupo?"
- **Dirección concreta (nivel 3, solo tras intento real):** "El patrón de agregación es `SELECT <columna_de_grupo>, <agregado> FROM ... GROUP BY <columna_de_grupo>`. Para q6, recuerda que `SET precio = precio + 1000` usa el valor actual de cada fila; y que sin `WHERE` actualizas todas. Vuelve a correr `pytest` y predice cada resultado antes."

## Conexión con el proyecto / capstone
- Estas operaciones CRUD son exactamente las que tu API del **Capstone F3** ejecutará por cada endpoint (crear, listar con filtros, actualizar, borrar). Saber leer el SQL —aunque luego lo genere un ORM— es lo que te deja diagnosticar cuando un endpoint devuelve datos raros o va lento.
