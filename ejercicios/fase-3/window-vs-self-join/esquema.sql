-- Esquema + datos del ejercicio 3.2 — window functions sobre transacciones.
-- Carga: docker exec -i pg-ej psql -U postgres < esquema.sql

DROP TABLE IF EXISTS transacciones;
DROP TABLE IF EXISTS cuentas;

CREATE TABLE cuentas (
    id      INTEGER PRIMARY KEY,
    titular TEXT NOT NULL
);

CREATE TABLE transacciones (
    id        INTEGER PRIMARY KEY,
    cuenta_id INTEGER NOT NULL REFERENCES cuentas(id),
    fecha     DATE NOT NULL,
    monto     INTEGER NOT NULL    -- positivo = ingreso, negativo = gasto
);

INSERT INTO cuentas (id, titular) VALUES
    (1, 'Ana'),
    (2, 'Beto'),
    (3, 'Cora');

INSERT INTO transacciones (id, cuenta_id, fecha, monto) VALUES
    (1, 1, DATE '2026-01-02',  100),
    (2, 1, DATE '2026-01-05',  -30),
    (3, 1, DATE '2026-01-10',   50),
    (4, 2, DATE '2026-01-03',  200),
    (5, 2, DATE '2026-01-08',  -50),
    (6, 3, DATE '2026-01-04',   80);
