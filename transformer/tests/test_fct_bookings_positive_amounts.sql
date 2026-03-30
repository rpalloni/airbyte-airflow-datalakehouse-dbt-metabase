-- Fails if any booking has a zero or negative total amount
SELECT booking_id, total_amount
FROM {{ ref('fct_bookings') }}
WHERE total_amount <= 0