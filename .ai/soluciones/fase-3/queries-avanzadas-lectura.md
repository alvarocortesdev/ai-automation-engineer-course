---
ejercicio_id: fase-3/queries-avanzadas-lectura
fase: fase-3
sub_unidad: "3.2"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Lee y diagnostica: JOINs, NULLs y window functions

## Respuestas canónicas

### 1. `LEFT JOIN` + `COUNT(p.id)` agrupado por socio

| nombre | total |
|---|---|
| Ana | 2 |
| Beto | 1 |
| Cora | 2 |
| Dani | 0 |

**Por qué:** Ana tiene 2 préstamos (Dune, Hyperion), Beto 1 (Solaris), Cora 2 (Dune, Neuromante). Dani no tiene préstamos: el `LEFT JOIN` le crea una fila con todas las columnas de `prestamos` en NULL, y `COUNT(p.id)` **ignora NULL** → 0. Con `COUNT(*)` Dani habría dado **1** (la fila fantasma). Ese contraste es el corazón de la pregunta.

### 2. El bug del outer join degradado a inner

**Causa:** la fila que el `LEFT JOIN` inventa para Dani tiene `p.fecha_devolucion = NULL`. La condición `WHERE p.fecha_devolucion IS NOT NULL` evalúa `NULL IS NOT NULL` → **falso**, así que esa fila se descarta. Al filtrar en el `WHERE` una columna de la tabla derecha, el `LEFT JOIN` se comporta como `INNER JOIN` y Dani desaparece (igual que cualquier socio cuyos préstamos estén todos sin devolver, como Ana perdería la fila de 'Hyperion').

**Corrección (mover la condición al `ON`):**

```sql
SELECT s.nombre, p.libro
FROM socios s
LEFT JOIN prestamos p
  ON p.socio_id = s.id
 AND p.fecha_devolucion IS NOT NULL
ORDER BY s.nombre;
```

Resultado (Dani vuelve, con `libro` NULL; Ana solo muestra 'Dune'):

| nombre | libro |
|---|---|
| Ana | Dune |
| Beto | Solaris |
| Cora | Dune |
| Cora | Neuromante |
| Dani | NULL |

**Regla general:** en un outer join, la condición que describe la tabla que quieres **conservar** va en el `ON`; lo que filtra el **resultado final** va en el `WHERE`.

### 3. Decisión de JOIN

- **(a) `LEFT JOIN`** (desde `socios`), con la condición "no devuelto" (`fecha_devolucion IS NULL`) en el **`ON`**, no en el `WHERE` — para conservar a los socios con 0 préstamos activos. Razón: deben sobrevivir las filas de socios sin pareja.
- **(b) `INNER JOIN`** — solo interesan préstamos que tienen socio y que ya fueron devueltos; las filas sin pareja no deben aparecer.
- **(c) `FULL JOIN`** (FULL OUTER JOIN) entre `socios` y `tarjetas` — para conservar huérfanos de **ambos** lados (socios sin tarjeta y tarjetas sin socio) en una sola pasada.

### 4. Window functions sobre `ventas`

| region | mes | monto | rnk | acumulado |
|---|---|---|---|---|
| Norte | 1 | 100 | 3 | 100 |
| Norte | 2 | 150 | 1 | 250 |
| Norte | 3 | 120 | 2 | 370 |
| Sur | 1 | 200 | 1 | 200 |
| Sur | 2 | 180 | 2 | 380 |

**Por qué:** `RANK() ... ORDER BY monto DESC` por región: Norte (150→1, 120→2, 100→3), Sur (200→1, 180→2). `SUM(monto) OVER (PARTITION BY region ORDER BY mes)` es un **total corriente** (el `ORDER BY` dentro del `OVER` crea el marco "desde el inicio hasta la fila actual"): Norte acumula 100, 250, 370; Sur 200, 380. El orden de salida pedido es por region y luego mes.

## Puntos resbalosos (donde el corrector debe mirar)

1. **Dani = 1 en P1** → no entiende `COUNT(columna)` vs `COUNT(*)`. Es el error #1.
2. **P2 "corregido" con `OR p.libro IS NULL`** en el WHERE → parche; lo idiomático es mover al `ON`.
3. **P4 acumulado = 370 (Norte) o 380 (Sur) en TODAS las filas de la región** → no entendió que el `ORDER BY` dentro del `OVER` hace el total corriente; cree que es el total global.
4. **No hay empates en `ventas`**, así que `RANK` y `ROW_NUMBER` coincidirían aquí; si el alumno no lo nota, preguntarle qué cambiaría con un empate (ahí `RANK` repite y salta, `ROW_NUMBER` no).
5. **(c) con LEFT en vez de FULL** → no ve que se piden huérfanos en ambos lados.

## Rango de soluciones aceptables

- En P2, cualquier corrección que recupere a Dani **y** mantenga la intención (préstamos devueltos por socio + socios sin préstamos) moviendo la condición al `ON` es válida. Una alternativa con subquery/`EXISTS` también puede ser correcta si conserva a Dani; evaluar la intención, no la forma exacta.
- En P3 (a), aceptar tanto "LEFT con condición en ON" como una formulación con subquery que cuente solo los no devueltos, siempre que conserve a los socios en 0.
- En P4, aceptar cualquier redacción de la salida que dé los 5 valores de `rnk` y `acumulado` correctos; el nivel **excelente** explica el marco (RANGE/ROWS por defecto con `ORDER BY`).
- **Variante de control para detectar dependencia-IA:** pedir que prediga P1 si fuera `COUNT(*)`. Quien entendió dice "Dani pasa a 1"; quien no, se traba.
