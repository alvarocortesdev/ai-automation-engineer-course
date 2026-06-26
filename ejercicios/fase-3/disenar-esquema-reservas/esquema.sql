-- Ejercicio 3.1 — Esquema de reservas de coworking (Primero-Sin-IA)
--
-- Diseña el esquema A MANO primero, sin IA. Este archivo es tu entregable de DDL.
-- Usa SQL estándar / PostgreSQL. Recuerda:
--   * Toda tabla necesita una clave primaria (PK).
--   * Cada relación se implementa con una clave foránea declarada (REFERENCES).
--   * Usa el tipo de dato más específico que sirva (TEXT, INTEGER, DATE, TIME...).
--   * NOT NULL para lo obligatorio; UNIQUE para lo que no se repite; CHECK para reglas.
--
-- Pista de tipos PostgreSQL:
--   id autoincremental:  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY
--   fecha:               DATE
--   hora:                TIME
--   dinero:              NUMERIC(10, 2)   (nunca FLOAT para plata)

-- =====================================================================
-- TODO(estudiante): define las tablas. Hay tres entidades en el requisito.
-- =====================================================================

-- CREATE TABLE socios (
--     ...
-- );

-- CREATE TABLE salas (
--     ...
-- );

-- CREATE TABLE reservas (
--     ...
--     -- ¿qué claves foráneas necesita? ¿qué atributos propios tiene?
-- );


-- =====================================================================
-- TODO(estudiante): crea los índices que justifiques en NOTAS.md.
-- =====================================================================

-- CREATE INDEX ... ON ... (...);
