-- Fails if any user from dim_users is missing from rpt_user_stats
-- The LEFT JOIN in rpt_user_stats guarantees all users are listed but the test makes it explicit

SELECT d.user_id, d.user_name
FROM {{ ref('dim_users') }} d
LEFT JOIN {{ ref('rpt_user_stats') }} r
ON d.user_id = r.user_id
WHERE r.user_id IS NULL