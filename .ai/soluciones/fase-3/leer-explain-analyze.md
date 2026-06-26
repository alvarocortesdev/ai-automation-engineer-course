---
ejercicio_id: fase-3/leer-explain-analyze
fase: fase-3
sub_unidad: "3.3"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Leer un plan EXPLAIN ANALYZE y arreglar la query

## Diagnóstico canónico

**Cuello de botella:** el `Seq Scan on pedidos`. Líneas que lo prueban en `plan-actual.txt`:

- `Seq Scan on pedidos ... (actual time=0.018..305.114 rows=15211 loops=1)` — escanea la tabla completa, ~305 ms.
- `Filter: (estado = 'pendiente'::text)` y `Rows Removed by Filter: 1484789` — miró 1,5M filas y descartó casi todas para quedarse con 15.211.
- El `Sort` (top-N heapsort, 27kB) y el `Limit` son **baratos**: el tiempo total (312 ms) está casi todo en el escaneo. No hay que tocarlos.

**Por qué el planner eligió `Seq Scan`:** no existe ningún índice sobre `estado` (solo la PK sobre `id`). Sin índice, la única forma de aplicar `WHERE estado = 'pendiente'` es leer toda la tabla y filtrar.

**Lectura de números:** `cost=0.00..28048.00` son unidades **arbitrarias** del planner (no ms); sirven para comparar planes. El tiempo real es `actual time`. Aquí `rows` estimado (15500) y real (15211) **calzan**, así que las estadísticas están al día: el problema es estructural (falta de índice), no estadística vieja.

## El arreglo (`indice.sql`)

Mejor opción — índice **compuesto** que sirve al filtro Y al orden:

```sql
CREATE INDEX idx_pedidos_estado_creado ON pedidos (estado, creado_en DESC);
```

Aceptable también un índice **parcial** (más pequeño, solo indexa lo que la query busca):

```sql
CREATE INDEX idx_pedidos_pendientes ON pedidos (creado_en DESC) WHERE estado = 'pendiente';
```

## Plan nuevo esperado

Con el índice compuesto, el `Seq Scan` desaparece y aparece un `Index Scan` (o `Index Scan Backward`) que:
- usa el índice para saltar directo a las filas con `estado = 'pendiente'` (`Index Cond: (estado = 'pendiente')`),
- las entrega **ya ordenadas** por `creado_en DESC`, eliminando el paso `Sort`,
- con el `LIMIT 20`, lee solo las primeras ~20 entradas del índice.

El `actual time` cae de ~312 ms a fracciones de ms.

```text
 Limit  (actual time=0.03..0.09 rows=20 loops=1)
   ->  Index Scan using idx_pedidos_estado_creado on pedidos
             (actual time=0.02..0.07 rows=20 loops=1)
         Index Cond: (estado = 'pendiente'::text)
 -- sin nodo Sort, sin Seq Scan, sin Rows Removed by Filter
```

## Bonus — el `ORDER BY`
Sí: el índice compuesto `(estado, creado_en DESC)` sirve al `ORDER BY creado_en DESC` **porque** `estado` está fijado por una igualdad en el `WHERE`. Dentro de las filas con `estado = 'pendiente'`, el índice ya las tiene ordenadas por `creado_en DESC`, así que Postgres las lee en orden y se salta el `Sort`. El orden de las columnas importa: `(creado_en, estado)` NO serviría igual para filtrar por `estado`.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Selectividad.** El índice ayuda **porque** 'pendiente' es ~1% (15.211 de 1,5M). Si fuera el 49% (como 'entregado'/'cancelado'), el planner probablemente seguiría con `Seq Scan` —leer el índice + saltar a la tabla para casi medio millón de filas es más caro que un escaneo secuencial. Un análisis excelente menciona esto.
2. **`cost` ≠ ms.** Marcar si el alumno trató `28048.00` como tiempo.
3. **Indexar `estado` solo vs compuesto.** `CREATE INDEX ON pedidos(estado)` ya quita el `Seq Scan` (competente), pero deja el `Sort`. El compuesto es la respuesta excelente.
4. **Estadísticas.** Si el alumno dice "corre `ANALYZE`", está bien como hábito, pero aquí las estimaciones ya calzan: el fix es el índice, no `ANALYZE`.

## Rango de soluciones aceptables
- **Índice compuesto `(estado, creado_en DESC)`** — óptimo, sirve filtro + orden.
- **Índice parcial `WHERE estado = 'pendiente'`** — excelente, aún más pequeño; válido si la query siempre filtra por ese estado.
- **Índice simple `(estado)`** — competente: elimina el `Seq Scan` pero deja el `Sort`.
- **Predecir `Bitmap Heap Scan`** en vez de `Index Scan` — aceptable; con ~15k filas dispersas y sin el `LIMIT`, Postgres podría elegir bitmap. Con `LIMIT 20` + índice ordenado, `Index Scan` es lo más probable. Cualquiera de los dos, bien justificado, cuenta.
- ❌ **No aceptable:** indexar `id` o `total`; afirmar que el `Sort`/`Limit` es el cuello de botella; tratar `cost` como milisegundos.
