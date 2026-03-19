USE wow_economy;
GO


CREATE TABLE erp_auctions (
    scan_time DATETIME, 
    auction_id BIGINT,
    item_id BIGINT,
    quantity INT,
    unit_price BIGINT,
    time_left VARCHAR(30)
);
GO

CREATE TABLE crm_items (
    ID INT,
    Name VARCHAR(255),
    Quality VARCHAR(50),
    ItemClass VARCHAR(100)
);
GO


TRUNCATE TABLE erp_auctions;
GO

BULK INSERT erp_auctions
FROM 'C:\Your\Local\Path\To\source_crm_items.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n'
);
GO


TRUNCATE TABLE crm_items;
GO

BULK INSERT crm_items
FROM 'C:\Your\Local\Path\To\history_erp_auctions.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    CODEPAGE = '65001'
);
GO




SELECT TOP 10 * FROM erp_auctions;
SELECT TOP 10 * FROM crm_items;

SELECT COUNT(*) AS total_rows_erp FROM erp_auctions;
GO