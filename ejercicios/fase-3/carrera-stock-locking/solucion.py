"""Resuelve la carrera del stock con DOS estrategias de locking.

Implementa las dos funciones SIN dejar nunca el stock negativo ni vender más
unidades de las que había, aunque muchos hilos las llamen a la vez. NO uses un
SELECT y luego un UPDATE "normales" (sin FOR UPDATE, sin version, sin aritmética
atómica): eso es exactamente el bug que entrena este ejercicio (lost update).

Corre el test:
    export DATABASE_URL="postgresql://localhost/explain_lab"   # o tu URL
    uv run pytest        # o: pytest

Anota en bitacora.md en qué escenario de contención preferirías cada estrategia.
"""

from psycopg_pool import ConnectionPool


def comprar_pesimista(pool: ConnectionPool, evento_id: int) -> bool:
    """Compra 1 unidad usando locking PESIMISTA (SELECT ... FOR UPDATE).

    Devuelve True si vendió, False si no quedaba stock.

    Pista: dentro de `with pool.connection() as conn:`, bloquea la fila con
    FOR UPDATE, valida el stock en Python, y decrementa con un UPDATE. El lock
    se libera al salir del `with` (commit), así que el siguiente hilo espera y
    lee el valor ya actualizado.
    """
    raise NotImplementedError("implementa la versión pesimista")


def comprar_optimista(
    pool: ConnectionPool, evento_id: int, max_intentos: int = 1000
) -> bool:
    """Compra 1 unidad usando locking OPTIMISTA (columna `version` + reintento).

    Devuelve True si vendió, False si no quedaba stock.

    Pista: lee (stock, version) SIN bloquear; intenta el UPDATE condicionado a
    `version = <la que leíste>`. Si cur.rowcount == 0, alguien te ganó entre tu
    lectura y tu escritura: reintenta desde la lectura. No olvides el tope de
    intentos para no girar para siempre.
    """
    raise NotImplementedError("implementa la versión optimista")
