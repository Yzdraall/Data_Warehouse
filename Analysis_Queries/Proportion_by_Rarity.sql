SELECT 
    i.rarity,
    COUNT(a.unique_auction_id) AS total_listings
FROM gold.fact_auctions a
INNER JOIN gold.dim_items i 
    ON a.unique_item_id = i.item_id
GROUP BY i.rarity
ORDER BY total_listings DESC;