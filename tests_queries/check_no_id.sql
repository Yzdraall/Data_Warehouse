SELECT a.item_id, COUNT(*) AS missing_count
FROM silver.erp_auctions a
LEFT JOIN silver.crm_items c ON a.item_id = c.item_id
WHERE c.item_id IS NULL
GROUP BY a.item_id;