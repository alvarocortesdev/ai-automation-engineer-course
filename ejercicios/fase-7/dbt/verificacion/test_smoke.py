"""Smoke test opcional del mini-warehouse.

NO reemplaza a `dbt build` (los tests de dbt que TÚ escribes en schema.yml son la
verificación principal de este ejercicio). Este script es una red de seguridad
automatable que abre el warehouse ya construido y comprueba invariantes básicas.

Cómo usarlo:
    1) Primero construye el warehouse:   dbt build --profiles-dir .
    2) Instala las dependencias de test:  pip install pytest duckdb
    3) Corre:                             pytest verificacion/

Si `dev.duckdb` no existe (no corriste dbt build) o falta `duckdb`, los tests se
SALTAN con un mensaje claro en vez de fallar ruidosamente.
"""

from pathlib import Path

import pytest

duckdb = pytest.importorskip(
    "duckdb", reason="Instala con: pip install duckdb (y corre antes `dbt build`)."
)

# El warehouse vive en dev.duckdb, en la raíz del proyecto (carpeta padre de esta).
DB_PATH = Path(__file__).resolve().parent.parent / "dev.duckdb"


@pytest.fixture(scope="module")
def con():
    if not DB_PATH.exists():
        pytest.skip(
            f"No existe {DB_PATH.name}. Corre primero: dbt build --profiles-dir ."
        )
    connection = duckdb.connect(str(DB_PATH), read_only=True)
    yield connection
    connection.close()


def _table_exists(con, name: str) -> bool:
    rows = con.execute(
        "select 1 from information_schema.tables where lower(table_name) = ?",
        [name.lower()],
    ).fetchall()
    return len(rows) > 0


def test_mart_existe(con):
    assert _table_exists(con, "customer_orders"), (
        "Falta el modelo customer_orders. ¿Corriste `dbt build`?"
    )


def test_customer_id_no_nulo(con):
    nulos = con.execute(
        "select count(*) from customer_orders where customer_id is null"
    ).fetchone()[0]
    assert nulos == 0, f"customer_orders tiene {nulos} customer_id nulos."


def test_customer_id_unico(con):
    dups = con.execute(
        """
        select count(*) from (
            select customer_id from customer_orders
            group by customer_id having count(*) > 1
        )
        """
    ).fetchone()[0]
    assert dups == 0, (
        f"customer_orders tiene {dups} customer_id duplicados: "
        "probablemente un JOIN multiplicó filas (agrega antes de unir)."
    )


def test_number_of_orders_no_negativo(con):
    # Solo si la columna existe (parte obligatoria del enunciado).
    cols = [r[1].lower() for r in con.execute("pragma table_info('customer_orders')").fetchall()]
    if "number_of_orders" not in cols:
        pytest.skip("Aún no agregaste la columna number_of_orders.")
    malos = con.execute(
        "select count(*) from customer_orders where number_of_orders < 0"
    ).fetchone()[0]
    assert malos == 0, "number_of_orders nunca debería ser negativo."
