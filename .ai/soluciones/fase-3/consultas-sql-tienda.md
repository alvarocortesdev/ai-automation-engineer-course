---
ejercicio_id: fase-3/consultas-sql-tienda
fase: fase-3
sub_unidad: "3.1"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Escribe SQL contra una base que corre

## Respuesta canónica

```sql
-- q1 — SELECT + WHERE
SELECT nombre, stock
FROM productos
WHERE categoria = 'periféricos' AND stock > 0;

-- q2 — ORDER BY + LIMIT
SELECT nombre, precio
FROM productos
ORDER BY precio DESC
LIMIT 3;

-- q3 — GROUP BY + COUNT
SELECT categoria, COUNT(*) AS cantidad
FROM productos
GROUP BY categoria;

-- q4 — GROUP BY + SUM
SELECT categoria, SUM(stock) AS suma_stock
FROM productos
GROUP BY categoria;

-- q5 — INSERT (sin id; la base lo asigna)
INSERT INTO productos (nombre, categoria, precio, stock)
VALUES ('Alfombrilla', 'accesorios', 9990, 50);

-- q6 — UPDATE (incrementa, no sobrescribe; con WHERE)
UPDATE productos
SET precio = precio + 1000
WHERE categoria = 'cables';

-- q7 — DELETE (con WHERE)
DELETE FROM productos
WHERE stock = 0;
```

## Resultados esperados (para verificar de un vistazo)

- **q1:** `(Teclado mecánico, 12)`, `(Mouse inalámbrico, 30)`, `(Audífonos, 7)`. Webcam HD queda fuera (stock 0).
- **q2 (en orden):** `(Monitor 27", 189990)`, `(Monitor 24", 129990)`, `(Audífonos, 49990)`.
- **q3:** `periféricos` 4, `pantallas` 2, `cables` 2, `accesorios` 2.
- **q4:** `periféricos` 49, `pantallas` 13, `cables` 100, `accesorios` 35.
- **q5:** tras el insert hay 11 filas; la nueva es `(Alfombrilla, accesorios, 9990, 50)`.
- **q6:** Cable HDMI 5990→6990, Cable USB-C 7990→8990.
- **q7:** se eliminan Cable USB-C y Webcam HD; quedan 8 filas.

## Razonamiento paso a paso

1. **q1** — dos condiciones unidas con `AND`. Pedir solo `nombre, stock` (no `SELECT *`) es lo que pide el enunciado y un hábito de claridad.
2. **q2** — `ORDER BY precio DESC` (de mayor a menor) y `LIMIT 3`. Sin `DESC` daría los más baratos; sin `LIMIT`, toda la tabla ordenada.
3. **q3/q4** — el patrón de agregación: agrupas por `categoria` y, por cada grupo, pides un agregado (`COUNT(*)` cuenta filas; `SUM(stock)` suma). La regla de oro: en el `SELECT` solo va la columna agrupada y agregados —nada de `nombre` suelto, porque cada grupo colapsa muchas filas en una.
4. **q5** — `INSERT` listando columnas y omitiendo `id`. Listar columnas hace el insert robusto a cambios de esquema; omitir `id` deja que la base lo genere.
5. **q6** — `SET precio = precio + 1000` lee el valor actual de cada fila y le suma; `WHERE categoria = 'cables'` limita el alcance. `SET precio = 1000` sería sobrescribir, no incrementar.
6. **q7** — `DELETE ... WHERE stock = 0`. El `WHERE` es lo único que separa "borrar los agotados" de "vaciar la tabla".

## Puntos resbalosos (donde el corrector debe mirar)

1. **Columna no agregada en q3/q4:** `SELECT categoria, nombre, COUNT(*) ... GROUP BY categoria`. SQLite lo acepta y devuelve un `nombre` arbitrario del grupo; PostgreSQL lo rechazaría. Es un error de comprensión aunque el test (si solo compara categoria+conteo) no lo atrape: revisar el SQL, no solo el verde.
2. **q2 sin `DESC`** → los 3 más baratos (test falla, pero conviene nombrar el porqué).
3. **q6 con precio absoluto** (`SET precio = 1000`) → pasa a 1000 en vez de +1000.
4. **q6/q7 sin `WHERE`** → modifican/borran toda la tabla. El test de q6 fallaría (otras categorías cambiarían); el de q7 también (total != 8). Marcar como el error más peligroso.
5. **q5 con `id` explícito** (`VALUES (11, ...)`) → funciona en este test, pero es frágil y mala práctica; señalarlo.

## Rango de soluciones aceptables

- Alias distintos (`AS n`, `AS total_productos`) o sin alias: el test compara valores, no nombres de columna. Aceptar.
- En q1, `stock > 0` o `stock >= 1` son equivalentes para enteros. Aceptar.
- En q5, `INSERT INTO productos (nombre, categoria, precio, stock) VALUES (...)` es lo esperado; `INSERT ... DEFAULT` u otras variantes que dejen el `id` automático también valen.
- En q7, `WHERE stock = 0` o `WHERE stock < 1` (enteros, stock >= 0 por el CHECK) son equivalentes.
- **No** es aceptable resolver q3/q4 sin `GROUP BY` (p. ej. siete consultas a mano con `WHERE`): el objetivo es la agregación. Si lo hacen, marcar que no cumple O1.
- **Variante de control para detectar dependencia-IA:** pedir que prediga, sin ejecutar, el resultado de `SELECT categoria, COUNT(*) FROM productos WHERE stock = 0 GROUP BY categoria`. Respuesta correcta: `periféricos` 1 (Webcam) y `cables` 1 (Cable USB-C). Quien entendió la agregación responde; quien copió, no.
