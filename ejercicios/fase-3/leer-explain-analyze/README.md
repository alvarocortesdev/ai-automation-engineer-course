# Ejercicio 3.3 — Leer un plan EXPLAIN ANALYZE y arreglar la query

> **Modalidad: a mano (razonamiento + SQL, sin IA).** La herramienta #1 de diagnóstico de backend es leer un plan de ejecución. Muchas entrevistas te ponen una query lenta y te piden arreglarla en vivo. Aquí practicas exactamente eso, en seco.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.3` PostgreSQL a fondo
**Ruta:** crítica · **Timebox:** 30–45 min

## 🎯 Objetivo

Dado el `EXPLAIN ANALYZE` de una query lenta sobre una tabla grande, **identificar el cuello de botella** citando líneas concretas del plan, **proponer el índice** que lo arregla, y **predecir** cómo cambia el plan (y por qué baja el tiempo).

## 📋 Contexto

En el capstone, cuando un endpoint vaya lento, `EXPLAIN ANALYZE` es tu primer paso —no adivinar índices ni "agregar uno a cada columna". Saber leer `cost`, `rows`, `actual time`, `Seq Scan` y `Rows Removed by Filter` es la diferencia entre arreglar la causa y tapar el síntoma.

## 📏 Primero-Sin-IA

1. Lee el plan **tú**, línea por línea, antes de buscar nada. Marca qué número te alarma y por qué.
2. Solo entonces, consulta la **documentación oficial** (Using EXPLAIN de Postgres).
3. **Solo al final**, usa IA para *revisar* tu análisis — no para que te diga el índice.
4. Mañana, toma una query de tu propio proyecto y predice su plan antes de correrlo.

## 🛠️ Instrucciones

1. Abre `consulta.sql` (la query) y `plan-actual.txt` (su `EXPLAIN ANALYZE` sobre una tabla `pedidos` de ~1.5M filas).
2. Escribe `analisis.md` con:
   - **(1) Cuello de botella:** qué operación es y **qué líneas exactas** del plan lo prueban (cita `Seq Scan`, `Rows Removed by Filter`, `actual time`).
   - **(2) Por qué** el planner eligió ese plan.
   - **(3) El arreglo:** escribe el/los `CREATE INDEX` en `indice.sql`.
   - **(4) Predicción:** qué operación reemplaza al `Seq Scan` en el plan nuevo y por qué baja el tiempo.
   - **(Bonus)** la query también hace `ORDER BY`: ¿tu índice puede servir además para evitar el paso `Sort`?
3. (Opcional) Verifica con datos reales: `datos-sinteticos.sql` crea la tabla y la puebla; corre el `EXPLAIN ANALYZE` antes y después de tu índice.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] El cuello de botella está identificado citando líneas concretas, no "se ve lento".
- [ ] El `CREATE INDEX` apunta a la(s) columna(s) correcta(s) del `WHERE`/`ORDER BY`.
- [ ] Predices la operación del plan nuevo (`Index Scan` o `Bitmap Heap Scan`) y justificas la mejora.
- [ ] Explicas **sin notas** por qué `cost` no son milisegundos y qué significa una brecha grande entre `rows` estimado y real.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Lee el plan de arriba hacia abajo: la operación raíz sobre `pedidos` es un `Seq Scan` con un `Filter` y un `Rows Removed by Filter` enorme → no hay índice para ese filtro. Indexa la columna del `WHERE`. Si además filtras por una columna y ordenas por otra, un índice **compuesto** `(columna_filtro, columna_orden)` puede servir para filtrar **y** entregar las filas ya ordenadas, evitando un `Sort`. Predice `Index Scan` (pocas filas) o `Bitmap Heap Scan` (filas moderadas y dispersas). Revisa la sección 4.5 de la lección antes de mirar la referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `analisis.md` + `indice.sql` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-3/leer-explain-analyze.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/leer-explain-analyze.md` — no la mires antes de intentarlo.
