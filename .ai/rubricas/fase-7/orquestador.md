---
ejercicio_id: fase-7/orquestador
fase: fase-7
sub_unidad: "7.5c"
version: 1
---

# Rúbrica — Pipeline asset-centric: la ingesta dispara dbt

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector la usa con `INSTRUCCIONES-CORRECTOR.md`. No es una nota numérica: es un mapa de qué observar y cómo dar feedback. **Nunca entregar el código de la solución de referencia.**

## Objetivos evaluados

- **O1:** Implementar un pipeline asset-centric en Dagster donde el asset de ingesta dispara `dbt build` después, con el DAG derivado del calce de asset keys (`["raw","orders"]` ↔ `source('raw','orders')`).
- **O2:** Explicar el trade-off task-centric (Airflow) vs asset-centric (Dagster) y por qué los reintentos exigen idempotencia.
- **O3:** Configurar scheduling (cron) + RetryPolicy y razonar qué significa un backfill por particiones.

## Criterios y niveles

### C1 — Corrección: el pipeline asset-centric conecta ingesta → dbt · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `definitions.py` no carga; o la ingesta y dbt aparecen como dos grafos separados (no calzan keys); o `@dbt_assets` no corre `dbt build`. |
| **en-progreso** | Carga, pero usa `dbt run` en vez de `dbt build`; o el asset de ingesta no tiene la key `["raw","orders"]` y conecta por casualidad/no conecta; o falta el recurso `dbt` en `Definitions`. |
| **competente** | Asset de ingesta con key `["raw","orders"]` + `@dbt_assets` con `dbt build`; en `dagster dev` el DAG es **uno solo** (raw.orders → stg → mart); `Definitions` con assets y recurso `dbt`. |
| **excelente** | Lo anterior + materializó el grafo completo en orden, adjunta metadata (`filas_ingestadas`) visible en la corrida, y entiende/explica el calce de asset keys (translator) por qué los une. |

### C2 — Calidad de ingeniería: retry coherente con idempotencia + schedule · mapea: O3, hilo testing/reliability
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin `RetryPolicy`; o la ingesta hace `INSERT` ciego (no idempotente) y `pytest tests/test_ingesta.py` está rojo. |
| **en-progreso** | Tiene `RetryPolicy` **pero** la ingesta no es idempotente (incoherencia peligrosa: retry duplicaría datos), o al revés (idempotente pero sin retry ni schedule). Test a veces rojo. |
| **competente** | Ingesta idempotente (`CREATE OR REPLACE` / upsert / DELETE+INSERT) **y** test verde; `RetryPolicy` con backoff; `define_asset_job` + `ScheduleDefinition` con cron válido. |
| **excelente** | Lo anterior + `@asset_check` bloqueante como ship-gate (`blocking=True`) sobre `customer_orders`; backoff con jitter; cron justificado por necesidad de frescura (no "cada 5 min por defecto"). |

### C3 — Comprensión demostrada (el WRITEUP calza con el pipeline) · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay WRITEUP, o describe el orquestador como "un cron con UI". |
| **en-progreso** | Explica *qué* hizo pero no el *por qué*: menciona asset-centric sin contrastar con task-centric, o no conecta retry con idempotencia. |
| **competente** | Articula task-centric (verbos) vs asset-centric (sustantivos/datos) y por qué retry ⇒ idempotencia, con su propio código como evidencia. |
| **excelente** | Lo anterior + explica backfill por particiones (rango acotado, no "re-correr todo") y cuándo Dagster vs Temporal (ADR); conecta con lineage/frescura como ventaja del modelo de datos. |

### C4 — Observabilidad (hilo transversal) · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No usa metadata ni checks; el pipeline es una caja negra. |
| **en-progreso** | Adjunta algo de metadata pero no la usa para razonar; sin asset checks. |
| **competente** | Metadata útil en materializaciones (filas) + sabe leer el linaje/run logs para diagnosticar. |
| **excelente** | Asset check bloqueante + WRITEUP que usa la observabilidad como herramienta de diagnóstico ("si X falla, lo veo en la materialización/check antes que el consumidor"). |

## Errores típicos a marcar

- **Retry sin idempotencia:** sube `max_retries` pero deja `INSERT` ciego → un fallo recuperable se vuelve duplicación silenciosa. **Es el error #1** y el corazón del ejercicio.
- **`dbt run` en vez de `dbt build`:** no corre los tests de dbt; el ship-gate de datos queda fuera (mismo antipatrón que en 7.5b).
- **Dos islas en el DAG:** la ingesta y dbt no calzan keys → aparecen desconectadas; "funciona" pero el orquestador no garantiza el orden ingesta→dbt.
- **Lógica de negocio dentro del asset de orquestación** (joins/agregaciones en Python) en vez de en dbt → orquestación gorda, pierde tests/linaje de dbt.
- **Confundir backfill con "re-correr todo":** no particiona y cree que rellenar el pasado es re-procesar el histórico completo.
- **Confundir el orquestador con cron:** no nombra las 4 capacidades (DAG, schedule, retry, observabilidad).
- **Confundir Dagster con Temporal:** propone Dagster para una saga transaccional o Temporal para correr dbt nocturno.
- (transversales) Cron "cada 5 min" sin necesidad de frescura (quema costo); confía en que el pipeline corrió sin mirar materializaciones/checks; persigue "muchos retries" sin pensar idempotencia (equivalente a perseguir coverage%).

## Señales de dependencia-IA

- `definitions.py` con **sensors, automation conditions avanzadas, IO managers custom o multi-código-location** impropios de un primer contacto, que el alumno **no puede defender** ("¿por qué un sensor aquí y no un schedule?" → silencio).
- WRITEUP pulido que afirma "asset-centric" correctamente pero **no calza con el código** (p. ej. dice "el DAG conecta ingesta y dbt" pero las keys no calzan y son dos islas).
- Tiene `RetryPolicy` perfecta pero la ingesta es `INSERT` ciego: copió el retry de un ejemplo sin entender la dependencia retry↔idempotencia (el ejercicio existe justo para exponer esto).
- Explica el calce de asset keys con la frase exacta de la doc pero no sabe responder "¿qué ves en `dagster dev` si las keys NO calzan?".

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Corre `pytest tests/test_ingesta.py`. ¿Verde o rojo? Si está rojo, tu ingesta duplica al re-ejecutarse — y un retry hace exactamente eso. Empieza por ahí, antes de tocar Dagster."
- **Pregunta socrática (nivel 2):** "En `dagster dev`, ¿ves UN grafo o DOS islas? Si son dos, ¿qué asset key le dio Dagster a la `source` de dbt, y cuál le pusiste a tu ingesta? ¿Por qué tendrían que ser la misma?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Tu retry duplica porque la ingesta hace `INSERT` y el retry re-ejecuta el asset entero. Cámbiala a `CREATE OR REPLACE TABLE raw.orders AS ...` (o DELETE del rango + INSERT). No bajes `max_retries` para 'esconder' el síntoma — la regla es retry ⇒ idempotencia. Verifica con el test antes de seguir."

## Conexión con el proyecto / capstone

- Este pipeline (ingesta → dbt, con retry/schedule/check) **es** el esqueleto de la capa de datos del capstone de F7: los datos que un agente extrae aterrizan en el warehouse, dbt los modela/testea, y el orquestador coordina todo en cada corrida. El asset check bloqueante es el mismo *ship-gate* que aplicarás a los evals del agente en 7.7; la observabilidad del orquestador es lo que vuelve el capstone auditable en vez de "corre en mi máquina".
