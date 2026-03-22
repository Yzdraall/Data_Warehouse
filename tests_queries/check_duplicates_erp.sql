SELECT auction_id, COUNT(*) FROM silver.erp_auctions
GROUP BY auction_id
HAVING COUNT(*) > 1 OR COUNT(*) IS NULL;