-- marts/customer_orders.sql
-- Objetivo: UNA fila por cliente con métricas de sus pedidos.
-- Columnas: customer_id, first_name, last_name,
--           number_of_orders, total_amount, first_order_date, most_recent_order_date.
--
-- Reglas:
--   - Refiere los STAGING con ref() (stg_customers, stg_orders, stg_payments), NUNCA los seeds.
--   - total_amount = suma de los pagos de los pedidos de ese cliente.
--   - Decide inner vs left join y justifícalo en WRITEUP.md.
--     (¿Quieres clientes sin pedidos en tu tabla final? -> left join + coalesce.)
--
-- Pista de estructura: necesitas agregaciones encadenadas:
--   1) pagos por order_id   2) unir a pedidos   3) agrupar por customer_id.

-- TODO: reemplaza este placeholder por tu modelo real.
select
    customer_id
from {{ ref('stg_customers') }}
