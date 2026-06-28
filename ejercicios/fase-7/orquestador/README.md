# Ejercicio 7.5c — Pipeline asset-centric: la ingesta dispara dbt

> **Modalidad: código (Dagster + dbt + DuckDB).** Construyes el orquestador que faltaba en 7.5b: la pieza que, en cada corrida programada, ingesta los pedidos crudos y **luego** dispara `dbt build` — con retry, schedule y un asset check como ship-gate. Primero a mano, sin IA.

## Objetivos

- **O1** — Implementar un pipeline **asset-centric** en Dagster donde un asset de ingesta (la "E-L") dispara `dbt build` **después**, dejando que Dagster derive el DAG de las dependencias (calce de asset keys).
- **O2** — Explicar el trade-off **task-centric (Airflow) vs asset-centric (Dagster)** y por qué los **reintentos exigen idempotencia**.
- **O3** — Configurar **scheduling** (cron) y una **RetryPolicy**, y razonar qué significa un **backfill** por particiones (no "re-correr todo").

## Preparación

1. Instala las dependencias (en esta carpeta):
   ```bash
   uv sync         # o: pip install dagster dagster-dbt dbt-duckdb duckdb pytest
   ```
2. **Copia tu proyecto dbt de [7.5b]** dentro de esta carpeta como `mini_warehouse/` (los modelos en capas + `schema.yml` + `dbt_project.yml` + `profiles.yml`). El pipeline lo orquesta; no lo reescribes. Si no lo tienes, usa el de la carpeta `ejercicios/fase-7/dbt/`.
3. Compila el manifest de dbt una vez: `dbt parse --project-dir mini_warehouse --profiles-dir mini_warehouse` (o deja que `dbt_project.prepare_if_dev()` lo haga).

## Tu tarea (en este orden — Primero-Sin-IA, timebox 45 min)

### Parte obligatoria (nivel "competente")

1. **Ingesta idempotente** (`ingesta.py`): completa `cargar_ordenes_crudas(con, ordenes)` para que cargue `raw.orders` **sin duplicar** al re-ejecutarse. Deja **verde** `pytest tests/test_ingesta.py`.
2. **Asset de ingesta** (`definitions.py`, TODO 1): `@dg.asset` con key `["raw", "orders"]`, una `RetryPolicy` con backoff, y metadata `filas_ingestadas`.
3. **Assets de dbt** (TODO 2): `@dbt_assets` + `DbtProject` + `DbtCliResource` corriendo `dbt build` (no `dbt run`).
4. **Schedule** (TODO 3): `define_asset_job` (todo el grafo) + `ScheduleDefinition` con cron diario.
5. Levanta `dagster dev`, abre `http://localhost:3000`, y **materializa el grafo completo una vez**. Confirma que `raw.orders` está conectado a los assets de dbt (un solo grafo, no dos islas) y corre en orden.

### Parte de profundización (nivel "excelente")

6. **Asset check bloqueante** (TODO 4): `@dg.asset_check(asset="customer_orders", blocking=True)` que falle si la tabla queda vacía.
7. **Particiones**: añade `DailyPartitionsDefinition` a los assets de dbt y describe en el WRITEUP cómo lanzarías un **backfill** de los últimos 7 días.
8. **`WRITEUP.md`** (5–8 líneas): tu DAG, el trade-off asset-centric vs task-centric en tus palabras, por qué tu ingesta debe ser idempotente dado el retry, y qué significaría un backfill aquí.

## Qué entregar (deja estos archivos en esta carpeta)

- `ingesta.py` completado (idempotente) y `tests/test_ingesta.py` en verde.
- `definitions.py` completado (TODOs resueltos; al menos hasta el TODO 3).
- `WRITEUP.md` con tu razonamiento.
- (Opcional) captura del DAG en `dagster dev` mostrando ingesta → dbt conectados.

## Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest tests/test_ingesta.py` en verde (ingesta idempotente).
- [ ] En `dagster dev`, el DAG conecta `raw.orders` con los assets de dbt (un solo grafo).
- [ ] El asset de ingesta tiene `RetryPolicy` **y** la ingesta es idempotente (coherencia retry↔idempotencia).
- [ ] Hay `define_asset_job` + `ScheduleDefinition` con cron válido.
- [ ] Materializaste el grafo completo al menos una vez, en orden (ingesta → dbt).
- [ ] Puedes **explicar sin notas** el trade-off task-centric vs asset-centric y por qué retry exige idempotencia.

## Pedir corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-7/orquestador/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **modelo mental** (asset-centric, retry↔idempotencia, backfill), no solo si `dagster dev` levanta.
