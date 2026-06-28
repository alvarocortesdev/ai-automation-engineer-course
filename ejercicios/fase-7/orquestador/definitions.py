"""Pipeline asset-centric (Dagster): la ingesta dispara `dbt build`.

Completa los TODOs y levanta con:  dagster dev
La UI queda en http://localhost:3000 — materializa el grafo completo.

El patrón clave de la Fase 7: tu asset de ingesta tiene la asset key ["raw","orders"],
que CALZA con source('raw','orders') de dbt. Por ese calce, Dagster une la ingesta y
todo el grafo de dbt en UN solo DAG, y `dbt build` corre DESPUÉS de la ingesta.
"""

from pathlib import Path

import duckdb
import dagster as dg
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets

from ingesta import ORDENES_DEMO, cargar_ordenes_crudas

# El mini-warehouse dbt de 7.5b vive en esta subcarpeta (cópialo o symlinkéalo).
DBT_DIR = Path(__file__).parent / "mini_warehouse"
DB_PATH = DBT_DIR / "dev.duckdb"

dbt_project = DbtProject(project_dir=DBT_DIR)
dbt_project.prepare_if_dev()  # compila target/manifest.json en desarrollo


# ── TODO 1 — Asset de ingesta (la "E-L") ───────────────────────────────────────
#  - asset key ["raw", "orders"]  (para que calce con source('raw','orders') de dbt)
#  - RetryPolicy con backoff (max_retries, delay, Backoff.EXPONENTIAL)
#  - llama cargar_ordenes_crudas(con, ORDENES_DEMO) — ¡que tu ingesta sea IDEMPOTENTE!
#  - adjunta metadata con context.add_output_metadata({"filas_ingestadas": ...})
@dg.asset(key=["raw", "orders"])
def raw_orders(context: dg.AssetExecutionContext) -> None:
    raise NotImplementedError("TODO 1: implementa la ingesta idempotente del asset raw.orders")


# ── TODO 2 — Assets de dbt ──────────────────────────────────────────────────────
#  Usa @dbt_assets(manifest=dbt_project.manifest_path) y corre `dbt build` (NO `dbt run`):
#      yield from dbt.cli(["build"], context=context).stream()


# ── TODO 3 — Schedule ─────────────────────────────────────────────────────────
#  - define_asset_job("warehouse_job", selection=dg.AssetSelection.all())
#  - ScheduleDefinition(job=..., cron_schedule="0 6 * * *")


# ── TODO 4 (profundización) — Asset check bloqueante sobre customer_orders ──────
#  @dg.asset_check(asset="customer_orders", blocking=True) -> dg.AssetCheckResult(passed=...)


# ── TODO 5 — Definitions (junta todo) ───────────────────────────────────────────
#  Añade warehouse_dbt a assets, y el job + schedule + (opcional) asset_checks.
defs = dg.Definitions(
    assets=[raw_orders],  # TODO: + warehouse_dbt
    resources={"dbt": DbtCliResource(project_dir=dbt_project)},
)
