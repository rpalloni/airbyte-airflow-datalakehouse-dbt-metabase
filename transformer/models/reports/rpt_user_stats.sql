{{ config(materialized='table') }}

SELECT
   d.user_id                    AS user_id 
    , user_name                 AS user_name
    , COUNT(booking_id)         AS tot_bookings
    , NVL(SUM(total_amount),0)  AS tot_amount
FROM {{ref('dim_users')}} d
LEFT JOIN {{ref('fct_bookings')}} f
ON d.user_id = f.user_id
GROUP BY 1, 2
ORDER BY 3 DESC