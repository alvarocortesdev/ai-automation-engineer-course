-- staging/stg_customers.sql
-- Regla de oro del staging: UNA fuente, renombrar/castear, SIN joins ni agregaciones.
-- Refiere el seed con ref() (dbt también crea los seeds, así que se referencian con ref).
--
-- TODO: completa el SELECT. Debe exponer: customer_id, first_name, last_name.

with source as (
    select * from {{ ref('raw_customers') }}
)

select
    -- TODO: lista las columnas (renombra si quieres nombres más claros)
    customer_id
from source
