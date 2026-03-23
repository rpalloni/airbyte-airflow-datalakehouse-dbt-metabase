{{ config(materialized='table') }}

SELECT
    id                      AS booking_id
    , booking_date          AS booking_dt
    , service_id            AS service_id
    , quantity              AS quantity
    , total_amount          AS total_amount
    , user_id               AS user_id
    , created_at            AS created_ts
    , _airbyte_extracted_at AS sync_ts
FROM {{source('pg-data', 'pg_bookings')}}