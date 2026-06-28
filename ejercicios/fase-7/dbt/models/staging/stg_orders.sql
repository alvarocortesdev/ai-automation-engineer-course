-- staging/stg_orders.sql
-- TODO: SELECT desde el seed raw_orders vía ref().
-- Expone: order_id, customer_id, order_date (casteado a date), status.
-- Sin joins ni agregaciones.

with source as (
    select * from {{ ref('raw_orders') }}
)

select
    -- TODO: order_id, customer_id, cast(order_date as date) as order_date, status
    order_id
from source
