---
ejercicio_id: fase-7/dbt
fase: fase-7
sub_unidad: "7.5b"
version: 1
---

# Rúbrica — Mini-warehouse con dbt: modelos en capas, tests y linaje

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector la usa con `INSTRUCCIONES-CORRECTOR.md`. No es una nota numérica: es un mapa de qué observar y cómo dar feedback. **Nunca entregar el código de la solución de referencia.**

## Objetivos evaluados

- **O1:** Construir un proyecto dbt en capas (staging → marts) con `ref()`, y explicar por qué `ref()` construye el DAG / da portabilidad / genera linaje.
- **O2:** Declarar tests de datos en YAML y dejar `dbt build` en verde, con el modelo mental correcto (test = query que cuenta filas inválidas; cero filas = verde).
- **O3:** Documentar el contrato del pipeline (sources/freshness, snapshots, exposures) + docs/lineage, argumentando qué resuelve cada uno.

## Criterios y niveles

### C1 — Corrección: modelado en capas con `ref()` · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Modelos no compilan, o `dbt build` no llega a verde; staging hace joins/agregaciones; el mart refiere seeds crudos en vez de staging. |
| **en-progreso** | `dbt build` corre los modelos, pero hay nombres de tabla escritos a mano (sin `ref()`), o el mart duplica la limpieza del staging, o falta una de las métricas pedidas. |
| **competente** | staging limpio (una fuente, renombrar/castear, sin lógica) + mart con las 4 métricas vía `ref()` a staging; `dbt build` en verde; join `inner`/`left` elegido y coherente. |
| **excelente** | Lo anterior + decisión `left join`+`coalesce` para incluir clientes sin pedidos **justificada por escrito**; CTEs nombrados con intención; estructura que hace el DAG legible. |

### C2 — Calidad de ingeniería: tests de datos reales · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin tests, o solo descripciones; o "arregló" un test rojo borrándolo en vez de corregir el dato/lógica. |
| **en-progreso** | Tiene algunos tests pero faltan los exigidos (p. ej. sin `relationships` o sin `accepted_values`), o usa `tests:` sin saber que `data_tests` es la clave actual. |
| **competente** | Cumple el mínimo: ≥2× `unique`, ≥2× `not_null`, 1× `relationships`, 1× `accepted_values`; todos verdes; sabe traducir cada test a la query que ejecuta. |
| **excelente** | Lo anterior + un **test singular** (`tests/*.sql`) que protege una invariante de negocio (p. ej. monto ≥ 0) + entiende `dbt build` vs `run`/`test` y por qué `build` corta cadenas con datos malos. |

### C3 — Comunicación del contrato: sources / snapshots / exposures · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No declara fuentes ni consumidores; el linaje empieza y termina sin contexto. |
| **en-progreso** | Declara un `source` o un `exposure` pero con errores (sintaxis vieja, `depends_on` mal, freshness sin `loaded_at_field`). |
| **competente** | `_sources.yml` con `freshness` correcto **y** `_exposures.yml` con `depends_on: [ref('customer_orders')]`; sabe explicar `source()` vs `ref()` (propiedad del dato). |
| **excelente** | Lo anterior + snapshot YAML válido (SCD2, estrategia justificada) + `dbt docs generate` + WRITEUP que **lee el linaje** como análisis de impacto ("si borro X se rompe el dashboard Y"). |

### C4 — Comprensión demostrada (el WRITEUP/explicación calza con el proyecto) · mapea: O1,O2,O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay write-up, o describe dbt como "una base de datos". |
| **en-progreso** | Explica *qué* hizo pero no *por qué* (p. ej. "usé ref" sin conectar con DAG/portabilidad/linaje). |
| **competente** | Conecta `ref()` ↔ DAG, test ↔ query de filas inválidas, y justifica el join. |
| **excelente** | Articula la tesis ("dbt trae ingeniería de software a los datos") con evidencia propia: versionado, tests en CI, linaje para cambiar con confianza. |

## Errores típicos a marcar

- El mart refiere los **seeds crudos** (`ref('raw_orders')`) en lugar de los **staging** → duplica limpieza y rompe la cadena de capas.
- **Nombres de tabla escritos a mano** en vez de `ref()`/`source()` → pierde DAG, portabilidad y linaje (aunque "funcione").
- Lógica de negocio (joins/agregaciones) metida en **staging** → staging debe ser aburrido.
- **`customer_id` duplicado en el mart** por un JOIN con pedidos sin agregar primero → el test `unique` lo delata; arreglar la lógica, no el test.
- Usa `dbt run` y cree que "pasó": no corrió los tests. El comando por defecto es `dbt build`.
- Trata un **test rojo como estorbo** (lo borra/comenta) en vez de señal de dato/lógica mala — el antipatrón exacto que dbt vino a matar.
- "Verde = datos perfectos": confunde "ninguna aserción declarada falló" con "los datos están bien".
- (transversales) Persigue *cantidad* de tests sin pensar qué invariante protege cada uno (el equivalente a perseguir coverage%); freshness sin `loaded_at_field`; confía en el output sin validar.

## Señales de dependencia-IA

- Proyecto con **macros, packages o materializaciones avanzadas** (incremental, snapshots con `timestamp` + `dbt_utils`) impropias de un primer contacto, que el alumno **no puede defender** ("¿por qué incremental aquí?" → silencio).
- WRITEUP pulido que afirma cosas correctas pero **no calzan con el SQL entregado** (p. ej. dice "left join para incluir clientes sin pedidos" pero el código tiene `inner`).
- Tests que cubren columnas que **no existen** en sus modelos (copiados de un ejemplo genérico).
- Explica `ref()` con la frase de marketing exacta de la doc pero no sabe responder "¿qué pasa en dev vs prod?".

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Corre `dbt build` y lee el primer error/rojo de arriba hacia abajo. ¿El problema está en un modelo (no compila) o en un test (dato inesperado)? Empieza por ahí."
- **Pregunta socrática (nivel 2):** "Tu mart refiere `stg_orders` o `raw_orders`. ¿Cuál? Dibuja el DAG que dbt deduciría de tus `ref()`: ¿la limpieza de staging está antes del mart, o la estás repitiendo?"
- **Dirección concreta (nivel 3, solo tras intento real):** "El `customer_id` se duplica porque unes pedidos sin agregar primero: un cliente con 2 pedidos produce 2 filas. Agrega a nivel `order_id` (pagos) y a nivel `customer_id` (métricas) en CTEs separados antes del `select` final. No toques el test — está señalando justo esto."

## Conexión con el proyecto / capstone

- Esta tabla testeada y con linaje **es** la capa de datos confiable del capstone de F7: los datos que un agente extrae aterrizan en un warehouse y se modelan/testean con dbt antes de alimentar una decisión o un dashboard (exposure). El test rojo que corta el `build` es el mismo *ship-gate* que aplicarás a los evals del agente en 7.7.
