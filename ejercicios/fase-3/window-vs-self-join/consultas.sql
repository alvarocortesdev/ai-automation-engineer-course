-- Starter del ejercicio 3.2 — window functions sobre transacciones (Primero-Sin-IA).
-- Escribe cada query a mano, sin IA. Verifica contra los resultados esperados del README.
-- Corre con:  docker exec -i pg-ej psql -U postgres < consultas.sql   (tras cargar esquema.sql)
--
-- Piensa el CONTRATO antes de escribir cada una: ¿qué columnas, cuántas filas, qué orden?

-- A) Saldo acumulado por cuenta, ordenado por fecha, SIN colapsar las filas.
--    Cada transacción con su `saldo_corriente` (suma de esa cuenta hasta la fila actual).
--    Usa una window function de agregación (SUM ... OVER (...)).
-- TODO:


-- B) La transacción más reciente (fecha máxima) de cada cuenta: id, cuenta_id, fecha, monto.
--    Entrega la versión con ROW_NUMBER() filtrada AFUERA (subquery o CTE; WHERE rn = 1).
--    (Piensa primero la versión "obvia" con self-join/correlacionada y anótala en NOTAS.md.)
-- TODO:


-- C) Cada transacción con el monto de la ANTERIOR de la misma cuenta (ordenadas por fecha).
--    Columnas: cuenta_id, fecha, monto, monto_anterior. Usa LAG().
-- TODO:
