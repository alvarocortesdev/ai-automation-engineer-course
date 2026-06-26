-- Diseña aquí la tabla que hace idempotente al POST /pagos.
-- No hay tests automáticos: esto se evalúa por el razonamiento del diseño.
--
-- Pistas de lo que debe permitir tu esquema (NO es la solución, son requisitos):
--   - una columna CLAVE que sea el árbitro de la carrera (PRIMARY KEY o UNIQUE)
--   - el ALCANCE de la clave (¿basta la clave, o va atada a usuario + endpoint?)
--   - dónde guardas la RESPUESTA para devolverla en el reintento
--     (y cómo distingues "aún en vuelo" de "ya terminó")
--   - un TIMESTAMP que te permita expirar claves viejas (TTL)
--
-- Reemplaza este stub por tu tabla:

CREATE TABLE idempotency_keys (
    -- TODO: define las columnas y el constraint que arbitra la carrera
);
