-- Datos del ejercicio 3.2 — Lee y diagnostica (biblioteca + ventas).
-- Carga: docker exec -i pg-ej psql -U postgres < datos.sql
-- Solo para VERIFICAR tus predicciones; predícelas a mano primero.

DROP TABLE IF EXISTS prestamos;
DROP TABLE IF EXISTS socios;
DROP TABLE IF EXISTS ventas;

CREATE TABLE socios (
    id     INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE prestamos (
    id               INTEGER PRIMARY KEY,
    socio_id         INTEGER NOT NULL REFERENCES socios(id),
    libro            TEXT NOT NULL,
    fecha_devolucion DATE          -- NULL = el libro sigue prestado
);

CREATE TABLE ventas (
    mes    INTEGER NOT NULL,
    region TEXT NOT NULL,
    monto  INTEGER NOT NULL
);

INSERT INTO socios (id, nombre) VALUES
    (1, 'Ana'),
    (2, 'Beto'),
    (3, 'Cora'),
    (4, 'Dani');   -- sin préstamos

INSERT INTO prestamos (id, socio_id, libro, fecha_devolucion) VALUES
    (10, 1, 'Dune',       DATE '2026-05-01'),
    (11, 1, 'Hyperion',   NULL),
    (12, 2, 'Solaris',    DATE '2026-04-20'),
    (13, 3, 'Dune',       DATE '2026-05-10'),
    (14, 3, 'Neuromante', DATE '2026-05-12');

INSERT INTO ventas (mes, region, monto) VALUES
    (1, 'Norte', 100),
    (2, 'Norte', 150),
    (3, 'Norte', 120),
    (1, 'Sur',   200),
    (2, 'Sur',   180);
