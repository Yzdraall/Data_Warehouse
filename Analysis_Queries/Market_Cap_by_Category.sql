SELECT
    i.category,
    COUNT(a.unique_auction_id) AS total_items_listed,
    CAST(SUM(a.price_in_gold) AS DECIMAL(18,0)) AS total_market_value
FROM gold.fact_auctions a
INNER JOIN gold.dim_items i 
    ON a.unique_item_id = i.item_id
GROUP BY i.category
ORDER BY total_market_value DESC;