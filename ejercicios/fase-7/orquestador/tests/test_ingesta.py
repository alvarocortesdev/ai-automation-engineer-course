"""Test de idempotencia de la ingesta (corre offline, solo necesita duckdb).

Modela un retry del orquestador: una `RetryPolicy` re-ejecuta el asset ENTERO.
Si la ingesta no es idempotente, la segunda corrida duplica filas -> rojo.
Este test debe quedar en VERDE cuando completes `cargar_ordenes_crudas`.
"""

import duckdb

from ingesta import ORDENES_DEMO, cargar_ordenes_crudas


def test_primera_carga_tiene_todas_las_filas(tmp_path):
    con = duckdb.connect(str(tmp_path / "t.duckdb"))
    try:
        n = cargar_ordenes_crudas(con, ORDENES_DEMO)
    finally:
        con.close()
    assert n == len(ORDENES_DEMO), f"esperaba {len(ORDENES_DEMO)} filas, obtuve {n}"


def test_carga_es_idempotente(tmp_path):
    con = duckdb.connect(str(tmp_path / "t.duckdb"))
    try:
        primera = cargar_ordenes_crudas(con, ORDENES_DEMO)
        segunda = cargar_ordenes_crudas(con, ORDENES_DEMO)  # "retry"
    finally:
        con.close()
    assert segunda == primera == len(ORDENES_DEMO), (
        f"ingesta NO idempotente: 1ra corrida={primera}, 2da={segunda}. "
        "Un retry duplicaría datos. Hazla idempotente (CREATE OR REPLACE / upsert / DELETE+INSERT)."
    )
