---
ejercicio_id: fase-3/window-vs-self-join
fase: fase-3
sub_unidad: "3.2"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Reemplaza el self-join: window functions sobre transacciones

## Respuestas canónicas

### A) Saldo acumulado por cuenta (sin colapsar)

```sql
SELECT
    cuenta_id,
    fecha,
    monto,
    SUM(monto) OVER (PARTITION BY cuenta_id ORDER BY fecha
                     ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS saldo_corriente
FROM transacciones
ORDER BY cuenta_id, fecha;
```

El marco explícito `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` es lo que hace el total corriente; con solo `ORDER BY fecha` y sin marco, el default (`RANGE ... UNBOUNDED PRECEDING`) da el mismo resultado aquí porque no hay fechas empatadas dentro de una cuenta. Salen las **6 filas**; saldo de Ana: 100, 70, 120.

### B) La transacción más reciente de cada cuenta (window)

```sql
SELECT id, cuenta_id, fecha, monto
FROM (
    SELECT t.*,
           ROW_NUMBER() OVER (PARTITION BY cuenta_id ORDER BY fecha DESC) AS rn
    FROM transacciones t
) AS numeradas
WHERE rn = 1
ORDER BY cuenta_id;
```

Resultado: (id 3, cuenta 1, 50), (id 5, cuenta 2, -50), (id 6, cuenta 3, 80).

**La versión "obvia" que el alumno debe haber pensado primero (y descartado para la entrega):**

```sql
SELECT t.id, t.cuenta_id, t.fecha, t.monto
FROM transacciones t
WHERE t.fecha = (
    SELECT MAX(t2.fecha)
    FROM transacciones t2
    WHERE t2.cuenta_id = t.cuenta_id     -- correlacionada: re-escanea por cada fila
);
```

Misma respuesta con estos datos, pero re-escanea `transacciones` por cada fila (bucle anidado, ≈O(n²)) y, ante dos transacciones con la misma fecha máxima, devolvería **ambas**. `ROW_NUMBER` resuelve las dos cosas.

### C) Monto de la transacción anterior (LAG)

```sql
SELECT
    cuenta_id,
    fecha,
    monto,
    LAG(monto) OVER (PARTITION BY cuenta_id ORDER BY fecha) AS monto_anterior
FROM transacciones
ORDER BY cuenta_id, fecha;
```

La primera transacción de cada cuenta tiene `monto_anterior = NULL` (no hay anterior). Ana: NULL, 100, -30; Beto: NULL, 200; Cora: NULL.

## Razonamiento esperado en `NOTAS.md`

1. La subquery correlacionada de (B) se evalúa **una vez por cada fila** de `transacciones`: por cada transacción vuelve a recorrer las de su cuenta para sacar el `MAX`. Es el bucle anidado O(n²) de DSA, ahora en SQL.
2. La versión `ROW_NUMBER` numera todas las filas en **una pasada ordenada** (≈O(n log n) por la ordenación) y luego filtra; el motor está optimizado para esto.
3. `WHERE rn = 1` debe ir en una subquery/CTE externa porque las window functions se calculan **después** del `WHERE`/`GROUP BY` (orden de evaluación); no se pueden referenciar en el mismo nivel donde se definen.
4. (Puente) Es el mismo patrón del **N+1** de la Fase 3 (3.5): el bucle anidado escondido, ahí en queries del ORM.

## Puntos resbalosos (donde el corrector debe mirar)

1. **(B) entregada con self-join/correlacionada** → resultado correcto, objetivo O2/O3 incumplido. Error central.
2. **(A) sin `ORDER BY` en el `OVER`** → `SUM(monto) OVER (PARTITION BY cuenta_id)` da el total de la cuenta (Ana 120 en las 3 filas), no el corriente.
3. **`WHERE ROW_NUMBER() OVER (...) = 1`** directo → error de PostgreSQL; debe ir envuelto.
4. **`GROUP BY cuenta_id, MAX(fecha)`** + JOIN posterior → duplica ante empate y no es lo pedido.
5. **(C) sin `PARTITION BY`** → el `LAG` cruza cuentas (toma la última de la cuenta anterior como "anterior" de la primera de la siguiente). Debe particionar por `cuenta_id`.

## Rango de soluciones aceptables

- En (A), tanto el marco explícito `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` como el implícito (solo `ORDER BY fecha`) son correctos con estos datos; el nivel **excelente** explica por qué.
- En (B), una **CTE** (`WITH numeradas AS (...) SELECT ... WHERE rn = 1`) es equivalente a la subquery y igual de válida. Un desempate adicional en el `ORDER BY` (p. ej. `ORDER BY fecha DESC, id DESC`) es un plus, no un requisito con estos datos.
- En (C), `LAG(monto, 1)` explícito es equivalente a `LAG(monto)`.
- Cualquier formulación que dé exactamente las tablas esperadas del README **y** use window functions donde se pide es competente; la diferencia con "excelente" está en `NOTAS.md` (el porqué del costo y del orden de evaluación).
- **Variante de control para detectar dependencia-IA:** pedir que explique por qué `WHERE rn = 1` no puede vivir en el SELECT que calcula `rn`. Quien entendió habla del orden de evaluación; quien no, se traba.
