-- Fails if any user has a negative tot_amount (NVL handles nulls)

SELECT user_name, tot_amount
FROM {{ ref('rpt_user_stats') }}
WHERE tot_amount < 0
