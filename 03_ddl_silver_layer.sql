/*
=============================================================
Create silver Tables 
=============================================================
*/

USE wow_economy;
GO

-- Table des enchères nettoyées
IF OBJECT_ID('silver.erp_auctions', 'U') IS NOT NULL
    DROP TABLE silver.erp_auctions;
GO

CREATE TABLE silver.erp_auctions (
    scan_time       DATETIME,
    auction_id      BIGINT,
    item_id         BIGINT,
    quantity        INT,
    unit_price_gold DECIMAL(18, 4),
    time_left       VARCHAR(30),
    dwh_create_date DATETIME2 DEFAULT GETDATE()
);
GO

-- Table du référentiel objets nettoyée
IF OBJECT_ID('silver.crm_items', 'U') IS NOT NULL
    DROP TABLE silver.crm_items;
GO

CREATE TABLE silver.crm_items (
    item_id         INT,
    item_name       VARCHAR(255),
    quality         VARCHAR(50),
    item_class      VARCHAR(100),
    dwh_create_date DATETIME2 DEFAULT GETDATE()
);
GO