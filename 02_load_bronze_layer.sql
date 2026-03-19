/*
=============================================================
Load Data into Bronze Layer
=============================================================
*/

USE wow_economy;
GO

--clear existing data
TRUNCATE TABLE bronze.erp_auctions;
GO

TRUNCATE TABLE bronze.crm_items;
GO

--load erp data
BULK INSERT bronze.erp_auctions
FROM 'C:\Your\Local\Path\To\history_erp_auctions.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n'
);
GO

-- load crm data
BULK INSERT bronze.crm_items
FROM 'C:\Your\Local\Path\To\source_crm_items.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    CODEPAGE = '65001'
);
GO

--quick validation queries
SELECT TOP 10 * FROM bronze.erp_auctions;
SELECT TOP 10 * FROM bronze.crm_items;

SELECT COUNT(*) AS total_rows_erp FROM bronze.erp_auctions;
SELECT COUNT(*) AS total_rows_crm FROM bronze.crm_items;
GO