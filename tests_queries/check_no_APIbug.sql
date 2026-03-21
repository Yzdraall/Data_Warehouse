SELECT auction_id, item_id, quantity, unit_price_gold
FROM silver.erp_auctions
WHERE quantity <= 0 
   OR unit_price_gold <= 0;