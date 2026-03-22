/*
===============================================================================
Create Fact: gold.fact_auctions
===============================================================================
*/

USE wow_economy;
GO

IF OBJECT_ID('gold.fact_auctions', 'V') IS NOT NULL
    DROP VIEW gold.fact_auctions;
GO

CREATE VIEW gold.fact_auctions AS
SELECT 
    scan_time AS collection_date,
    auction_id AS unique_auction_id,
    item_id AS unique_item_id,
    quantity AS in_sale_quantity,
    unit_price_gold AS price_in_gold,
    time_left AS time_before_end
FROM silver.erp_auctions;
GO