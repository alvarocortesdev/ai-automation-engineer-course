"""Test de aceptación: NO debe haber overselling bajo concurrencia.

Crea un evento con stock=50, lanza 100 compras concurrentes con threads, y
verifica que se vendieron EXACTAMENTE 50 y el stock quedó en 0 — para ambas
estrategias (pesimista y optimista). Si una versión tiene un lost update,
se venderán más de 50 y/o el stock quedará negativo, y el test falla.

Requiere un Postgres corriendo y la variable de entorno DATABASE_URL.
Si no la hay, el módulo entero se SALTA con un mensaje claro.

NO abras este archivo para "adivinar" la solución: solo verifica la tuya.
"""

import os
import threading

import pytest

# Si las dependencias o la base no están, saltamos todo el módulo en la colección.
pytest.importorskip("psycopg")
pytest.importorskip("psycopg_pool")
from psycopg_pool import ConnectionPool  # noqa: E402

from solucion import comprar_optimista, comprar_pesimista  # noqa: E402

DATABASE_URL = os.environ.get("DATABASE_URL")
STOCK_INICIAL = 50
N_COMPRAS = 100


def _pool_o_skip() -> ConnectionPool:
    if not DATABASE_URL:
        pytest.skip(
            "define DATABASE_URL (ej: postgresql://localhost/explain_lab) "
            "y ten un Postgres corriendo para este test"
        )
    try:
        pool = ConnectionPool(DATABASE_URL, min_size=2, max_size=20, open=True)
        with pool.connection() as conn:
            conn.execute("SELECT 1")
        return pool
    except Exception as exc:  # conexión imposible: skip, no error
        pytest.skip(f"no se pudo conectar a Postgres ({exc}); levanta uno y exporta DATABASE_URL")


def _reset(pool: ConnectionPool) -> None:
    with pool.connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS eventos (
                id      integer PRIMARY KEY,
                stock   integer NOT NULL,
                version integer NOT NULL DEFAULT 0
            )
            """
        )
        conn.execute("DELETE FROM eventos")
        conn.execute(
            "INSERT INTO eventos (id, stock, version) VALUES (1, %s, 0)",
            (STOCK_INICIAL,),
        )


def _correr_concurrente(pool: ConnectionPool, fn) -> list[bool]:
    resultados: list[bool] = []
    lock = threading.Lock()

    def worker() -> None:
        vendio = fn(pool, 1)
        with lock:
            resultados.append(vendio)

    hilos = [threading.Thread(target=worker) for _ in range(N_COMPRAS)]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    return resultados


def _stock_final(pool: ConnectionPool) -> int:
    with pool.connection() as conn:
        cur = conn.execute("SELECT stock FROM eventos WHERE id = 1")
        return cur.fetchone()[0]


@pytest.mark.parametrize(
    "estrategia",
    [comprar_pesimista, comprar_optimista],
    ids=["pesimista", "optimista"],
)
def test_no_hay_overselling(estrategia) -> None:
    pool = _pool_o_skip()
    try:
        _reset(pool)
        resultados = _correr_concurrente(pool, estrategia)
        ventas = sum(1 for r in resultados if r)
        stock = _stock_final(pool)

        assert stock >= 0, f"el stock NUNCA debe quedar negativo (quedó {stock})"
        assert ventas == STOCK_INICIAL, f"se vendieron {ventas}, se esperaban {STOCK_INICIAL}"
        assert stock == 0, f"stock final {stock}, se esperaba 0"
    finally:
        pool.close()
