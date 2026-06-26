-- Esquema de referencia. El test crea esta tabla automáticamente; la dejamos
-- documentada aquí. La columna `version` habilita el locking OPTIMISTA.
CREATE TABLE IF NOT EXISTS eventos (
    id      integer PRIMARY KEY,
    stock   integer NOT NULL,
    version integer NOT NULL DEFAULT 0
);
