# dbt — Mini-warehouse con modelos en capas, tests y linaje

**Fase:** Fase 7 — Automatización, Orquestación y Data Engineering · **Lección:** `7.5b` dbt de verdad
**Ruta:** crítica · **Timebox:** 40 min (objetivo 25–45)

## 🎯 Objetivo

Construir un proyecto dbt que corre de verdad: transformar tres tablas crudas en un
warehouse en capas (staging → marts), referenciando con `ref()` para que dbt arme el
**DAG**, poniéndole **tests de datos** (unique/not_null/relationships/accepted_values), y
dejando `dbt build` en verde. Al terminar sabrás explicar por qué `ref()` es lo que hace a
dbt "ingeniería de software para datos".

## 📋 Contexto

Tienes tres CSVs crudos ya cargados como seeds (`raw_customers`, `raw_orders`,
`raw_payments`). Este ejercicio alimenta el **capstone de la Fase 7**: la capa de datos
confiable y testeada sobre la que un agente toma decisiones.

## ⚙️ Setup (una vez)

Necesitas dbt con el adaptador de DuckDB (warehouse local, gratis, sin cloud):

```bash
pip install dbt-duckdb       # o:  uv add dbt-duckdb
dbt --version                # confirma que dbt-duckdb aparece en la lista
```

Trabaja **desde esta carpeta** (`ejercicios/fase-7/dbt/`). El `profiles.yml` ya está aquí,
por eso todos los comandos llevan `--profiles-dir .`.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea lento y feo.
2. Solo entonces, consulta la **documentación oficial**: <https://docs.getdbt.com/docs/build/models>.
3. **Solo al final**, usa IA para *revisar y explicar* tu solución — nunca para *generarla*.
4. Mañana, reescribe `customer_orders.sql` y `schema.yml` **de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

### Parte obligatoria (nivel "competente")

1. **Staging** (`models/staging/`): completa `stg_customers.sql`, `stg_orders.sql`,
   `stg_payments.sql`. Cada uno: un `SELECT` desde el seed vía `ref()`, renombrando/casteando.
   **Sin joins ni agregaciones.**
2. **Mart** (`models/marts/customer_orders.sql`): una fila por cliente con
   `number_of_orders`, `total_amount` (suma de pagos de sus pedidos), `first_order_date`,
   `most_recent_order_date`. Refiere los **staging con `ref()`**, no los seeds. Decide
   `inner` vs `left join` y justifícalo.
3. **Tests** (`models/schema.yml`): como mínimo — `unique` + `not_null` en cada clave
   primaria; un `relationships` (pedido → cliente existente); un `accepted_values` sobre `status`.
4. Construye y verifica:

   ```bash
   dbt build --profiles-dir .
   ```

   Itera hasta que **todos los modelos y todos los tests** estén en verde.

### Parte de profundización (nivel "excelente" — hilos transversales)

5. **`source`** en `models/_sources.yml` para las tablas crudas, con un bloque `freshness`.
6. **Test singular** (un `.sql` en `tests/`) para una regla que los genéricos no cubren
   (p. ej. "ningún pago con monto negativo").
7. **`exposure`** en `models/_exposures.yml` para un dashboard que consuma `customer_orders`.
8. `dbt docs generate` y un `WRITEUP.md` (3–6 líneas): describe tu linaje, justifica el join
   elegido y di qué test atrapó (o atraparía) un dato malo.

### Verificación opcional automatable

Después de `dbt build`, como red de seguridad extra:

```bash
pip install pytest duckdb
pytest verificacion/
```

(Si no corriste `dbt build`, los tests se saltan con un mensaje claro.)

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `dbt build --profiles-dir .` termina en verde (seeds + 4 modelos + tests).
- [ ] Todos los modelos usan `ref()` — cero nombres de tabla escritos a mano.
- [ ] Staging sin joins ni agregaciones; la lógica vive en el mart.
- [ ] Al menos: 2× `unique`, 2× `not_null`, 1× `relationships`, 1× `accepted_values`.
- [ ] Puedes **explicar sin notas**: por qué `ref()` construye el DAG, y qué hace `dbt build`
      que `dbt run` no hace.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

- **Staging** es aburrido a propósito: `with source as ( select * from {{ ref('raw_X') }} ) select ... from source`, solo renombrar/castear.
- **El mart necesita pagos por pedido primero.** Dos agregaciones encadenadas: (a) suma de
  pagos agrupando por `order_id`; (b) unir a pedidos y agrupar por `customer_id`.
- **`left` vs `inner`:** ¿quieres clientes que aún no compraron en la tabla final? La cliente
  Elena (id 5) no tiene pedidos: si usas `left join` aparece con `number_of_orders = 0`
  (vía `coalesce`); con `inner` desaparece. Es decisión de negocio — defiéndela.
- Si un test `relationships` falla, **no borres el test**: mira qué fila lo viola. Está haciendo su trabajo.

Revisa la sección 4 de la lección `7.5b` antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (esta carpeta, con los modelos y `schema.yml` completos + la salida de `dbt build`),
- la **rúbrica**: `.ai/rubricas/fase-7/dbt.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** (`.ai/soluciones/fase-7/dbt/`) es material del corrector — no la
mires antes de intentarlo de verdad.
