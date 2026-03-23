{{ config(materialized='table') }}

SELECT
    id                      AS user_id
    , name                  AS user_name
    , created_at            AS created_ts
    , _airbyte_extracted_at AS sync_ts
FROM {{source('pg-data', 'pg_users')}}