-- OPCIONAL: reproduce el escenario en tu propio Postgres para verificar tu análisis.
-- Crea la tabla `pedidos`, la puebla con ~1.5M filas (≈1% en estado 'pendiente'),
-- y deja listo para correr el EXPLAIN ANALYZE antes y después de tu índice.
--
-- Uso:
--   createdb explain_lab
--   psql explain_lab -f datos-sinteticos.sql
--   psql explain_lab -c "EXPLAIN ANALYZE SELECT id, cliente_id, total, creado_en
--                        FROM pedidos WHERE estado = 'pendiente'
--                        ORDER BY creado_en DESC LIMIT 20;"
--   -- ...luego aplica tu indice.sql y vuelve a correr el EXPLAIN ANALYZE.

DROP TABLE IF EXISTS pedidos;

CREATE TABLE pedidos (
    id          bigserial PRIMARY KEY,
    cliente_id  integer     NOT NULL,
    estado      text        NOT NULL,
    total       integer     NOT NULL,
    creado_en   timestamptz NOT NULL
);

-- 1.5M filas. Solo ~1% queda 'pendiente'; el resto 'entregado' o 'cancelado'.
INSERT INTO pedidos (cliente_id, estado, total, creado_en)
SELECT
    (random() * 50000)::int                                   AS cliente_id,
    CASE
        WHEN random() < 0.01 THEN 'pendiente'
        WHEN random() < 0.5  THEN 'cancelado'
        ELSE 'entregado'
    END                                                       AS estado,
    (random() * 100000)::int                                  AS total,
    now() - (random() * interval '365 days')                  AS creado_en
FROM generate_series(1, 1500000);

-- Importante: actualiza las estadísticas para que el planner no use números viejos.
ANALYZE pedidos;
