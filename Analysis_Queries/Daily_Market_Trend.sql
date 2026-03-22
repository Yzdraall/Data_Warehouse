SELECT 
    CAST(a.collection_date AS DATE) AS auction_date,
    COUNT(a.unique_auction_id) AS daily_listings,
    CAST(AVG(a.price_in_gold) AS DECIMAL(18,0)) AS daily_average_price
FROM gold.fact_auctions a
GROUP BY CAST(a.collection_date AS DATE)
ORDER BY auction_date ASC;