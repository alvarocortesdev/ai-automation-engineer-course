---
ejercicio_id: fase-7/dbt
fase: fase-7
sub_unidad: "7.5b"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). El alumno debe entregar su propio intento antes de que esto se discuta.

# Solución de referencia — Mini-warehouse con dbt

Esta es **una** solución canónica. Hay variantes aceptables (nombres de CTE, casteos, `inner` vs `left` con justificación). Lo que NO es negociable: `ref()` en todos lados, staging sin lógica, los tests exigidos en verde.

## Estructura final

```text
models/
├── staging/
│   ├── stg_customers.sql
│   ├── stg_orders.sql
│   └── stg_payments.sql
├── marts/
│   └── customer_orders.sql
├── schema.yml
├── _sources.yml        (profundización)
└── _exposures.yml      (profundización)
snapshots/
└── customers_snapshot.yml  (profundización)
tests/
└── assert_pagos_no_negativos.sql  (profundización)
```

## Modelos de staging

`stg_customers.sql`
```sql
with source as (
    select * from {{ ref('raw_customers') }}
)
select
    customer_id,
    first_name,
    last_name
from source
```

`stg_orders.sql`
```sql
with source as (
    select * from {{ ref('raw_orders') }}
)
select
    order_id,
    customer_id,
    cast(order_date as date) as order_date,
    status
from source
```

`stg_payments.sql`
```sql
with source as (
    select * from {{ ref('raw_payments') }}
)
select
    payment_id,
    order_id,
    payment_method,
    cast(amount as integer) as amount
from source
```

## Mart

`marts/customer_orders.sql` — dos agregaciones encadenadas, `left join` para incluir a Elena (id 5, sin pedidos):
```sql
with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

payments as (
    select * from {{ ref('stg_payments') }}
),

-- monto por pedido (suma de sus pagos)
order_amounts as (
    select
        order_id,
        sum(amount) as order_amount
    from payments
    group by order_id
),

-- métricas por cliente
customer_stats as (
    select
        o.customer_id,
        count(distinct o.order_id) as number_of_orders,
        sum(coalesce(a.order_amount, 0)) as total_amount,
        min(o.order_date) as first_order_date,
        max(o.order_date) as most_recent_order_date
    from orders o
    left join order_amounts a on o.order_id = a.order_id
    group by o.customer_id
)

select
    c.customer_id,
    c.first_name,
    c.last_name,
    coalesce(s.number_of_orders, 0) as number_of_orders,
    coalesce(s.total_amount, 0)     as total_amount,
    s.first_order_date,
    s.most_recent_order_date
from customers c
left join customer_stats s on c.customer_id = s.customer_id
```

**Resultado esperado** (con los seeds dados): 5 filas; Elena (id 5) con `number_of_orders = 0`, `total_amount = 0` y fechas nulas; Ana (id 1) con `number_of_orders = 2`, `total_amount = 21490`.

## Tests — `models/schema.yml`

```yaml
version: 2

models:
  - name: stg_customers
    description: "Clientes, una fila por cliente."
    columns:
      - name: customer_id
        description: "Clave primaria del cliente."
        data_tests: [unique, not_null]

  - name: stg_orders
    description: "Pedidos, una fila por pedido."
    columns:
      - name: order_id
        data_tests: [unique, not_null]
      - name: customer_id
        data_tests:
          - not_null
          - relationships:
              to: ref('stg_customers')
              field: customer_id
      - name: status
        data_tests:
          - accepted_values:
              values: ['placed', 'shipped', 'completed', 'returned']

  - name: stg_payments
    description: "Pagos, una fila por pago."
    columns:
      - name: payment_id
        data_tests: [unique, not_null]
      - name: order_id
        data_tests:
          - not_null
          - relationships:
              to: ref('stg_orders')
              field: order_id

  - name: customer_orders
    description: "Un cliente por fila, con métricas de sus pedidos."
    columns:
      - name: customer_id
        data_tests: [unique, not_null]
```

> Nota de versión: en dbt 1.10.5+/v2 los argumentos de `relationships`/`accepted_values` van anidados bajo `arguments:`. La forma de arriba funciona en toda la línea 1.x estable y es la más común. Ambas son aceptables.

## Profundización (nivel "excelente")

`models/_sources.yml`
```yaml
version: 2
sources:
  - name: raw
    description: "Tablas crudas cargadas por el pipeline EL (aquí simulado con seeds)."
    schema: main
    tables:
      - name: raw_orders
        config:
          loaded_at_field: order_date
          freshness:
            warn_after: {count: 48, period: hour}
            error_after: {count: 168, period: hour}
```

`tests/assert_pagos_no_negativos.sql` (test singular — devuelve filas que violan la regla)
```sql
-- Falla si existe cualquier pago con monto negativo.
select payment_id, amount
from {{ ref('stg_payments') }}
where amount < 0
```

`models/_exposures.yml`
```yaml
version: 2
exposures:
  - name: panel_clientes
    label: "Panel de retención de clientes"
    type: dashboard
    maturity: high
    url: https://bi.example.com/clientes
    description: "Dashboard de retención para el equipo comercial."
    depends_on:
      - ref('customer_orders')
    owner:
      name: Equipo de Datos
      email: datos@example.com
```

`snapshots/customers_snapshot.yml`
```yaml
snapshots:
  - name: customers_snapshot
    relation: ref('stg_customers')
    config:
      unique_key: customer_id
      strategy: check
      check_cols: ['first_name', 'last_name']
```

## Salida esperada de `dbt build --profiles-dir .`

Todos los nodos en `PASS`/`OK`: 3 seeds, 4 modelos (3 views de staging + 1 table mart), y los tests (≥6 genéricos + el singular si lo agregó). Cero `ERROR`, cero `FAIL`.

## Puntos resbalosos (donde el corrector debe mirar)

1. **`count(*)` vs `count(distinct order_id)`** al contar pedidos: si une pagos a pedidos *antes* de contar, un pedido con 2 pagos se cuenta doble. La solución agrega pagos por `order_id` primero, evitando el fan-out. Es el error de modelado más probable.
2. **`left join` final**: sin él, Elena (sin pedidos) desaparece. Con `inner join` el resultado tiene 4 filas, no 5. Aceptable solo si el alumno lo justifica como decisión de negocio; si es por accidente, es `en-progreso`.
3. **`total_amount` de clientes sin pedidos**: debe ser 0 (vía `coalesce`), no `null`, si el negocio pide "monto total". Cualquiera de las dos es defendible mientras sea consciente.
4. **El mart refiere staging, no seeds.** Si ve `ref('raw_orders')` en el mart, es la cadena de capas rota.

## Rango de soluciones aceptables

- Materializar el mart como `view` en vez de `table` es válido (cambia rendimiento, no corrección).
- Nombres de CTE distintos, casteos extra, o calcular `total_amount` con un solo nivel de agregación usando `count(distinct order_id)` + `sum(amount)` sobre un join — válido **si maneja el fan-out** y lo puede explicar.
- Para O3, declarar solo `source` + `exposure` (sin snapshot) ya es `competente`; el snapshot empuja a `excelente`.
- Cualquier `WRITEUP.md` que conecte `ref()`↔DAG, test↔query-de-filas-inválidas y justifique el join cuenta como comprensión demostrada.
