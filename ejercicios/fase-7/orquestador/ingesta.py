"""Ingesta de pedidos crudos a DuckDB (la "E-L" del pipeline).

TODO (ejercicio 7.5c): `cargar_ordenes_crudas` NO es idempotente: re-ejecutarla
DUPLICA filas. Un orquestador con `RetryPolicy` re-ejecuta el asset ENTERO cuando
falla, así que una ingesta no idempotente convierte un retry en datos duplicados.
Tu trabajo: hazla idempotente para que `pytest tests/test_ingesta.py` quede en verde.
"""

from __future__ import annotations

import duckdb

# Datos crudos de ejemplo. En producción vendrían de una API / SFTP / archivo del día.
ORDENES_DEMO: list[dict] = [
    {"order_id": 1, "customer_id": 1, "order_date": "2025-06-01", "status": "placed"},
    {"order_id": 2, "customer_id": 1, "order_date": "2025-06-02", "status": "shipped"},
    {"order_id": 3, "customer_id": 2, "order_date": "2025-06-03", "status": "completed"},
    {"order_id": 4, "customer_id": 3, "order_date": "2025-06-04", "status": "returned"},
]


def cargar_ordenes_crudas(con: duckdb.DuckDBPyConnection, ordenes: list[dict]) -> int:
    """Carga `ordenes` en la tabla raw.orders y devuelve el conteo final de filas.

    TODO: HAZLA IDEMPOTENTE. Hoy hace un INSERT ciego: cada llamada acumula filas,
    así que dos llamadas seguidas (como un retry) DUPLICAN los datos.
    Pista: `CREATE OR REPLACE TABLE`, o DELETE+INSERT del rango, o upsert por order_id.
    Ejecutarla N veces debe dejar el mismo estado que ejecutarla una.
    """
    con.execute("create schema if not exists raw")
    con.execute(
        """
        create table if not exists raw.orders (
            order_id integer,
            customer_id integer,
            order_date varchar,
            status varchar
        )
        """
    )

    # ❌ No idempotente: INSERT ciego. Reemplaza esta lógica por una idempotente.
    for o in ordenes:
        con.execute(
            "insert into raw.orders values (?, ?, ?, ?)",
            [o["order_id"], o["customer_id"], o["order_date"], o["status"]],
        )

    return con.execute("select count(*) from raw.orders").fetchone()[0]
