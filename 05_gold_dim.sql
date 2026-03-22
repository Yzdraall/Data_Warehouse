

USE wow_economy;
GO

IF OBJECT_ID('gold.dim_items', 'V') IS NOT NULL
    DROP VIEW gold.dim_items;
GO

CREATE VIEW gold.dim_items AS
SELECT
    item_id        AS item_id,
    item_name      AS item_name,
    quality        AS rarity,
    item_class     AS category
FROM silver.crm_items;
GO