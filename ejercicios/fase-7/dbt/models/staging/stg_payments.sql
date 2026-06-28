-- staging/stg_payments.sql
-- TODO: SELECT desde el seed raw_payments vía ref().
-- Expone: payment_id, order_id, payment_method, amount.
-- (Pista: 'amount' viene en pesos enteros; déjalo como está o castea a decimal.)

with source as (
    select * from {{ ref('raw_payments') }}
)

select
    -- TODO: payment_id, order_id, payment_method, amount
    payment_id
from source
