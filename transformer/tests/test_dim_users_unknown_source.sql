{{ config(severity='warn') }}

-- Warns if any user falls into 'Unknown' source category (unexpected user_id prefix)
-- As 'Unknown' is a valid fallback, it is only a warning

SELECT user_id, source
FROM {{ ref('dim_users') }}
WHERE source = 'Unknown'
