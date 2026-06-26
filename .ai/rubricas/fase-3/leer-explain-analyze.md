---
ejercicio_id: fase-3/leer-explain-analyze
fase: fase-3
sub_unidad: "3.3"
version: 1
---

# Rúbrica — Leer un plan EXPLAIN ANALYZE y arreglar la query

> Rúbrica **analítica** atada a los `objetivos`. Evalúa el `analisis.md` y el `indice.sql`
> del alumno contra `plan-actual.txt`. Lo que separa al competente del que "sabe que falta
> un índice" es **citar las líneas** del plan que prueban el diagnóstico y **predecir** el
> plan nuevo, no solo escribir un `CREATE INDEX`.

## Objetivos evaluados
- **O1** — Identificar el cuello de botella citando líneas del plan (`Seq Scan`, `Rows Removed by Filter`, `actual time`).
- **O2** — Distinguir `cost` (estimado, arbitrario) de `actual time` (real, ms) y leer la brecha `rows` estimado/real.
- **O3** — Proponer el índice correcto y predecir la operación del plan nuevo, incluyendo el caso del `ORDER BY`.

## Criterios y niveles

### C1 — Diagnóstico del cuello de botella · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | "Está lento" sin citar el plan, o culpa al `Sort`/`Limit` en vez del `Seq Scan`. |
| **en-progreso** | Identifica el `Seq Scan` pero no cita el `Rows Removed by Filter: 1484789` ni los 305 ms del escaneo. |
| **competente** | Señala el `Seq Scan on pedidos` + `Rows Removed by Filter` enorme + el `actual time` del escaneo como la causa, citando líneas. |
| **excelente** | Además observa que el `Sort` es barato (top-N heapsort) y que el costo real vive en el escaneo, no en el orden. |

### C2 — Lectura de números del plan · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Trata el `cost` como milisegundos. |
| **en-progreso** | Sabe que `cost` y `actual time` son distintos pero no explica que `cost` es arbitrario/relativo. |
| **competente** | Explica `cost` = unidades arbitrarias para comparar planes; `actual time` = ms reales; y qué significaría una brecha grande `rows` estimado vs real (estadísticas viejas → `ANALYZE`). |
| **excelente** | Nota que aquí `rows` estimado (15500) y real (15211) calzan, así que el problema NO es estadística vieja sino la falta de índice. |

### C3 — Índice y predicción del plan nuevo · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Índice sobre la columna equivocada (ej. `id`), o ningún `CREATE INDEX`. |
| **en-progreso** | `CREATE INDEX ON pedidos(estado)` simple; predice mejora pero no nombra la operación nueva. |
| **competente** | Índice sobre `estado` (o parcial sobre `estado='pendiente'`); predice `Index Scan`/`Bitmap Heap Scan` y justifica la baja de tiempo. |
| **excelente** | Índice **compuesto** `(estado, creado_en DESC)` que sirve al filtro Y al `ORDER BY` (evita el `Sort`); explica el bonus correctamente. |

## Errores típicos a marcar
- **Confundir `cost` con tiempo:** `cost=28048.00` no son 28 segundos ni ms; son unidades del planner.
- **Indexar la PK o `id`:** no ayuda al filtro por `estado`.
- **No ver el `ORDER BY`:** un índice solo sobre `estado` deja el `Sort`; el compuesto `(estado, creado_en DESC)` lo elimina y además sirve al `LIMIT 20`.
- **"Agrega un índice a cada columna":** ignora el costo de escritura; el ejercicio pide el índice *que la query usa*.
- **Caso del filtro poco selectivo:** si `'pendiente'` fuera el 90% de las filas, el índice sobre `estado` no ayudaría (el planner preferiría `Seq Scan`). Un buen análisis menciona que el índice sirve **porque** 'pendiente' es ~1% (15.211 de 1.5M).
- (transversal observabilidad) no proponer correr `ANALYZE` ni `EXPLAIN (ANALYZE, BUFFERS)` para confirmar.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- `analisis.md` que describe un plan genérico de libro sin referirse a los números **concretos** de `plan-actual.txt` (los 1.484.789 descartados, los 312 ms).
- Propone un índice compuesto perfecto pero no puede explicar por qué el orden `(estado, creado_en)` y no `(creado_en, estado)` importa.
- **Verificación sugerida:** pídele que prediga, sin ejecutar, qué pasaría con el plan si el filtro fuera `estado = 'entregado'` (el 49% de las filas): el índice probablemente NO se usaría y volvería el `Seq Scan`. Si no lo ve, copió el diagnóstico.

## Feedback sugerido (graduado)
> Nunca dar el `CREATE INDEX` final antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Lee el plan de arriba hacia abajo. ¿Cuál operación toca la tabla `pedidos` directamente, y cuántas filas descarta el `Filter`?"
- **Pregunta socrática (nivel 2):** "Si Postgres pudiera saltar directo a las filas con `estado = 'pendiente'` sin mirar el millón restante, ¿qué estructura necesitaría? Y ya que las pides ordenadas por `creado_en DESC` con `LIMIT 20`, ¿podría esa misma estructura entregártelas ya ordenadas?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "El `Seq Scan` + `Rows Removed by Filter: 1484789` prueba que falta índice para `WHERE estado`. `CREATE INDEX ON pedidos (estado, creado_en DESC)` sirve al filtro y al orden, así que verás un `Index Scan` y desaparecerá el `Sort`. Funciona porque 'pendiente' es ~1% de las filas. Repasa 4.5 antes de la referencia."

## Conexión con el proyecto / capstone
- Cuando un endpoint del capstone vaya lento, este es el flujo exacto: `EXPLAIN ANALYZE` → leer el plan → índice dirigido → verificar. Es diagnóstico de observabilidad de base de datos, no adivinanza.
