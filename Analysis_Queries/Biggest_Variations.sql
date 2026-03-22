SELECT 
    i.item_name,
    COUNT(a.unique_auction_id) AS listing_count,
    CAST(MIN(a.price_in_gold) AS DECIMAL(18,0)) AS minimum_price,
    CAST(MAX(a.price_in_gold) AS DECIMAL(18,0)) AS maximum_price,
    CAST(MAX(a.price_in_gold) - MIN(a.price_in_gold) AS DECIMAL(18,0)) AS price_gap
FROM gold.fact_auctions a
INNER JOIN gold.dim_items i 
    ON a.unique_item_id = i.item_id
GROUP BY i.item_name
HAVING COUNT(a.unique_auction_id) > 5
ORDER BY price_gap DESC;