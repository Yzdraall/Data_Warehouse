/*
=============================================================
Create Bronze Tables (Raw Layer)
=============================================================
*/

USE wow_economy;
GO

--drop tables if they already exist
IF OBJECT_ID('bronze.erp_auctions', 'U') IS NOT NULL
    DROP TABLE bronze.erp_auctions;
GO

IF OBJECT_ID('bronze.crm_items', 'U') IS NOT NULL
    DROP TABLE bronze.crm_items;
GO

-- erp: Auction transactions
CREATE TABLE bronze.erp_auctions (
    scan_time DATETIME,
    auction_id BIGINT,
    item_id BIGINT,
    quantity INT,
    unit_price BIGINT,
    time_left VARCHAR(30)
);
GO

--crm: item reference data
CREATE TABLE bronze.crm_items (
    id INT,
    name VARCHAR(255),
    quality VARCHAR(50),
    item_class VARCHAR(100)
);
GO