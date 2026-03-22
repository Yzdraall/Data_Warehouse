SELECT TOP 10
    i.item_name,
    i.category,
    i.rarity,
    COUNT(a.unique_auction_id) AS active_auctions
FROM gold.fact_auctions a
INNER JOIN gold.dim_items i 
    ON a.unique_item_id = i.item_id
GROUP BY i.item_name, i.category, i.rarity
ORDER BY active_auctions DESC;