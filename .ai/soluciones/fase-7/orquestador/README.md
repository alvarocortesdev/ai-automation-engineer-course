---
ejercicio_id: fase-7/orquestador
fase: fase-7
sub_unidad: "7.5c"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). El alumno debe entregar su propio intento antes de que esto se discuta.

# Solución de referencia — Pipeline asset-centric: la ingesta dispara dbt

Esta es **una** solución canónica. Hay variantes aceptables (idempotencia vía `CREATE OR REPLACE` vs upsert vs DELETE+INSERT; cron distinto; key map vía translator explícito). Lo que NO es negociable: **ingesta idempotente + RetryPolicy coherente**, **`dbt build` (no `run`)**, y el DAG **conectado** (ingesta y dbt en un solo grafo).

## 1. Ingesta idempotente — `ingesta.py`

La forma más simple e idempotente: reemplazar la tabla en cada corrida.

```python
def cargar_ordenes_crudas(con, ordenes):
    con.execute("create schema if not exists raw")
    # Idempotente: CREATE OR REPLACE deja siempre el mismo estado, corra 1 o N veces.
    con.execute(
        """
        create or replace table raw.orders (
            order_id integer, customer_id integer, order_date varchar, status varchar
        )
        """
    )
    con.executemany(
        "insert into raw.orders values (?, ?, ?, ?)",
        [(o["order_id"], o["customer_id"], o["order_date"], o["status"]) for o in ordenes],
    )
    return con.execute("select count(*) from raw.orders").fetchone()[0]
```

**Por qué es idempotente:** `CREATE OR REPLACE` borra y recrea la tabla cada vez; dos llamadas seguidas dejan exactamente `len(ordenes)` filas. Un retry del orquestador no duplica. Variantes igual de válidas:
- **Upsert por clave:** `INSERT ... ON CONFLICT (order_id) DO UPDATE` (requiere PK en `order_id`).
- **DELETE + INSERT del rango:** `delete from raw.orders where order_date between ...; insert ...` (la forma típica con particiones por fecha).

## 2. Pipeline completo — `definitions.py`

```python
from pathlib import Path

import duckdb
import dagster as dg
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets

from ingesta import ORDENES_DEMO, cargar_ordenes_crudas

DBT_DIR = Path(__file__).parent / "mini_warehouse"
DB_PATH = DBT_DIR / "dev.duckdb"

dbt_project = DbtProject(project_dir=DBT_DIR)
dbt_project.prepare_if_dev()

# 1) Ingesta (E-L): asset key calza con source('raw','orders') de dbt -> Dagster los conecta.
@dg.asset(
    key=["raw", "orders"],
    retry_policy=dg.RetryPolicy(
        max_retries=3,
        delay=10,
        backoff=dg.Backoff.EXPONENTIAL,
        jitter=dg.Jitter.PLUS_MINUS,
    ),
)
def raw_orders(context: dg.AssetExecutionContext) -> None:
    con = duckdb.connect(str(DB_PATH))
    try:
        n = cargar_ordenes_crudas(con, ORDENES_DEMO)  # idempotente -> seguro con retry
    finally:
        con.close()
    context.add_output_metadata({"filas_ingestadas": dg.MetadataValue.int(n)})

# 2) dbt: cada modelo es un asset; depende de la source raw.orders. `dbt build` (no run).
@dbt_assets(manifest=dbt_project.manifest_path)
def warehouse_dbt(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

# 3) Job + schedule diario.
warehouse_job = dg.define_asset_job("warehouse_job", selection=dg.AssetSelection.all())
warehouse_schedule = dg.ScheduleDefinition(job=warehouse_job, cron_schedule="0 6 * * *")

# 4) (profundización) Asset check bloqueante: ship-gate de datos.
@dg.asset_check(asset="customer_orders", blocking=True)
def hay_clientes(context) -> dg.AssetCheckResult:
    con = duckdb.connect(str(DB_PATH))
    try:
        n = con.execute("select count(*) from customer_orders").fetchone()[0]
    finally:
        con.close()
    return dg.AssetCheckResult(passed=bool(n > 0), metadata={"n_clientes": int(n)})

# 5) Definitions: junta todo.
defs = dg.Definitions(
    assets=[raw_orders, warehouse_dbt],
    asset_checks=[hay_clientes],
    jobs=[warehouse_job],
    schedules=[warehouse_schedule],
    resources={"dbt": DbtCliResource(project_dir=dbt_project)},
)
```

> **Nota sobre el calce de keys:** que `["raw","orders"]` calce con `source('raw','orders')` depende del `DagsterDbtTranslator`. El comportamiento por defecto suele derivar la key del nombre source/tabla; si en `dagster dev` aparecen como dos islas, se alinea con un translator explícito que sobreescribe `get_asset_key` para las sources. Ambas (calce por defecto o translator explícito) son aceptables.

## 3. Variante con particiones (profundización — backfill)

```python
import json

@dbt_assets(
    manifest=dbt_project.manifest_path,
    partitions_def=dg.DailyPartitionsDefinition(start_date="2025-01-01"),
)
def warehouse_dbt(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    inicio, fin = context.partition_time_window
    dbt_vars = {"min_date": inicio.isoformat(), "max_date": fin.isoformat()}
    yield from dbt.cli(["build", "--vars", json.dumps(dbt_vars)], context=context).stream()
```

**Backfill de 7 días:** en la UI, seleccionar el asset particionado → "Backfill" → rango de las últimas 7 particiones → lanzar. Dagster materializa **solo** esas 7, no el histórico. Conceptualmente correcto también: `dagster asset backfill` por CLI con el rango.

## 4. Resultado esperado

- `pytest tests/test_ingesta.py` → **2 passed** (ambos tests verdes; idempotencia OK).
- `dagster dev` carga sin error; el grafo muestra `raw.orders` (Python) conectado a `stg_orders`/`stg_customers` (dbt) → `customer_orders` → exposure. **Un solo DAG**, no dos islas.
- Materializar el grafo: la ingesta corre primero (deja metadata `filas_ingestadas: 4`), luego `dbt build` corre modelos + tests; el asset check `hay_clientes` pasa.

## 5. WRITEUP esperado (lo que debe articular)

- **DAG:** `raw.orders → stg_* → customer_orders → exposure`, conectado por el calce de asset keys.
- **Asset-centric vs task-centric:** task-centric (Airflow) orquesta *verbos* (tareas) y sabe "qué tarea corrió"; asset-centric (Dagster) declara *sustantivos* (datos) y sabe *qué dato* es cada nodo → frescura, linaje, "¿qué está stale?".
- **Retry ⇒ idempotencia:** una `RetryPolicy` re-ejecuta el asset entero; con `INSERT` ciego, el retry duplica. Por eso la ingesta usa `CREATE OR REPLACE` (o upsert / DELETE+INSERT).
- **Backfill:** rellenar un **rango acotado de particiones** (los 7 días), no re-correr el histórico — eso es lo que evita particionar por fecha.

## Puntos resbalosos (donde el corrector debe mirar)

1. **Retry sin idempotencia.** Lo más probable: `RetryPolicy` presente + `INSERT` ciego. Si el test está rojo o la ingesta acumula, es incoherencia peligrosa → marcar fuerte (es el aprendizaje central).
2. **`dbt run` vs `dbt build`.** `run` no corre tests → el ship-gate de dbt queda fuera. Debe ser `build`.
3. **Dos islas.** Si la ingesta y dbt no calzan keys, el orquestador no garantiza el orden ingesta→dbt aunque "ambos corran". Verde aparente, patrón roto.
4. **Lógica de negocio en Python.** Si el asset de ingesta hace joins/agregaciones (trabajo de dbt), es orquestación gorda → pierde tests/linaje de dbt.
5. **Cron sin criterio.** "*/5 * * * *" para datos que se ven una vez al día = quema costo; debe justificar la cadencia por frescura.

## Rango de soluciones aceptables

- Idempotencia vía `CREATE OR REPLACE`, upsert `ON CONFLICT`, o DELETE+INSERT — todas válidas si el test queda verde y la entiende.
- Calce de keys por defecto **o** translator explícito — ambas correctas.
- Sin particiones/backfill ni asset check ya es `competente` (son profundización para `excelente`).
- Cron distinto (diario, horario) es válido si lo justifica por necesidad de frescura.
- Cualquier `WRITEUP.md` que conecte asset-centric vs task-centric, retry↔idempotencia y backfill-por-particiones cuenta como comprensión demostrada.
