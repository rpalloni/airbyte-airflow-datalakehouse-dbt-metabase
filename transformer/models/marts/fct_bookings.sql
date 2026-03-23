{{ config(materialized='table') }}

SELECT
    booking_id
    , booking_dt
    , service_id
    , quantity
    , total_amount
    , 'EUR' AS currency
    , user_id
    , created_ts
    , sync_ts
FROM {{ref('stg_bookings')}}