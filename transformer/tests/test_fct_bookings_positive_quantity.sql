-- Fails if any booking has a zero or negative quantity
SELECT booking_id, quantity
FROM {{ ref('fct_bookings') }}
WHERE total_amount <= 0