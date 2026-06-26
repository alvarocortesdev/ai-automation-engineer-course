-- Datos de partida del ejercicio 3.1 — consultas-sql-tienda.
-- Una sola tabla `productos` (sin JOINs en esta lección).
-- Los tests cargan este archivo en una base SQLite en memoria antes de cada consulta.
-- NO edites este archivo: tus consultas viven en consultas/qN.sql.

CREATE TABLE productos (
    id         INTEGER PRIMARY KEY,
    nombre     TEXT    NOT NULL,
    categoria  TEXT    NOT NULL,
    precio     INTEGER NOT NULL CHECK (precio >= 0),   -- en pesos, entero
    stock      INTEGER NOT NULL CHECK (stock >= 0)
);

INSERT INTO productos (id, nombre, categoria, precio, stock) VALUES
    (1,  'Teclado mecánico',  'periféricos',  39990,  12),
    (2,  'Mouse inalámbrico', 'periféricos',  19990,  30),
    (3,  'Monitor 27"',       'pantallas',   189990,   5),
    (4,  'Monitor 24"',       'pantallas',   129990,   8),
    (5,  'Cable HDMI',        'cables',        5990, 100),
    (6,  'Cable USB-C',       'cables',        7990,   0),
    (7,  'Webcam HD',         'periféricos',  29990,   0),
    (8,  'Soporte monitor',   'accesorios',   24990,  15),
    (9,  'Audífonos',         'periféricos',  49990,   7),
    (10, 'Hub USB',           'accesorios',   15990,  20);
