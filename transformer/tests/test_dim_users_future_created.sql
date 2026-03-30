-- Fails if any user has a created_ts in the future
SELECT user_id, created_ts
FROM {{ ref('dim_users') }}
WHERE created_ts > CURRENT_TIMESTAMP
