SELECT COUNT(*) AS corrupted_rows
FROM silver.erp_auctions
WHERE scan_time IS NULL 
   OR item_id IS NULL 
   OR unit_price_gold IS NULL;