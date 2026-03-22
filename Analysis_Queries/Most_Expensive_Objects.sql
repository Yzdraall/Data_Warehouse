SELECT TOP 10
    i.item_name,
    i.rarity,
    CAST(AVG(a.price_in_gold) AS DECIMAL(18,0)) AS average_price
FROM gold.fact_auctions a
INNER JOIN gold.dim_items i 
    ON a.unique_item_id = i.item_id
GROUP BY i.item_name, i.rarity
ORDER BY average_price DESC;