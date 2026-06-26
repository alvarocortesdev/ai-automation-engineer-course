"""Starter del ejercicio — Primero-Sin-IA.

Implementa una migración reversible en miniatura sobre `sqlite3` (stdlib). La misma
mecánica de una migración Alembic real: cambiar el esquema, mover los datos, y poder
revertir todo sin pérdida.

NO cambies las firmas de `upgrade` ni `downgrade`: los tests dependen de ellas.

Recibes una conexión `sqlite3.Connection` ya abierta, con la tabla `usuarios` creada
y poblada:

    CREATE TABLE usuarios (
        id              INTEGER PRIMARY KEY,
        nombre_completo TEXT NOT NULL
    );

Contrato del split (para el backfill):
    - la primera palabra de `nombre_completo` es `nombre`,
    - el resto (si lo hay) es `apellido`,
    - si no hay resto, `apellido = ""`.
"""

import sqlite3


def upgrade(conn: sqlite3.Connection) -> None:
    """Aplica la migración: agrega `nombre` y `apellido`, y los rellena desde `nombre_completo`.

    Orden obligatorio: primero el cambio de ESQUEMA (ADD COLUMN), luego la migración
    de DATOS (UPDATE). No puedes escribir en una columna que todavía no existe.

    NO toques ni borres `nombre_completo`.
    """
    raise NotImplementedError("Implementa el upgrade a mano, sin IA.")


def downgrade(conn: sqlite3.Connection) -> None:
    """Revierte la migración: deja la tabla con solo `id` y `nombre_completo`, intactos.

    Pista: `ALTER TABLE usuarios DROP COLUMN <col>` (SQLite 3.35+).
    """
    raise NotImplementedError("Implementa el downgrade a mano, sin IA.")


if __name__ == "__main__":
    # Prueba rápida manual (Predict–Run): ¿qué columnas tendrá la tabla tras upgrade?
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE usuarios (id INTEGER PRIMARY KEY, nombre_completo TEXT NOT NULL)")
    conn.execute("INSERT INTO usuarios (id, nombre_completo) VALUES (1, 'Ada Lovelace')")
    conn.commit()
    upgrade(conn)
    print(list(conn.execute("SELECT id, nombre, apellido FROM usuarios")))
