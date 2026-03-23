{{ config(materialized='table') }}

SELECT
    user_id
    , user_name
    , CASE 
        WHEN user_name LIKE 'M%' THEN 'Marketplace'
        WHEN user_name LIKE 'U%' THEN 'Store'
        ELSE 'Unknown'
    END                     AS source
    , created_ts
    , sync_ts
FROM {{ref('stg_users')}}