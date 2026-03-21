/*
===============================================================================
Stored Procedure: Load Silver Layer

Script Purpose:
    This stored procedure performs the ETL (Extract, Transform, Load) process to 
    populate the 'silver' schema tables from the 'bronze' schema.
	Actions Performed:
		- Truncates Silver tables.
		- Inserts transformed and cleansed data from Bronze into Silver tables.

Usage: EXEC silver.load_silver;
===============================================================================
*/

CREATE OR ALTER PROCEDURE silver.load_silver AS
BEGIN
    DECLARE @start_time DATETIME, @end_time DATETIME, @batch_start_time DATETIME, @batch_end_time DATETIME; 
    
    BEGIN TRY
        SET @batch_start_time = GETDATE();
        PRINT '================================================';
        PRINT 'Loading Silver Layer (Cleansing & Transformation)';
        PRINT '================================================';

        --crm load&transform
        SET @start_time = GETDATE();
        PRINT '>> Truncating & Loading: silver.crm_items';
        TRUNCATE TABLE silver.crm_items;
        
        INSERT INTO silver.crm_items (item_id, item_name, quality, item_class)
        SELECT 
            ID,
            TRIM(Name),
            CASE WHEN Quality IS NULL OR Quality = '' THEN 'Unknown' ELSE TRIM(Quality) END,
            CASE WHEN item_class IS NULL OR item_class = '' THEN 'Unknown' ELSE TRIM(item_class) END
        FROM (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY ID ORDER BY ID) AS flag_last
            FROM bronze.crm_items
            WHERE ID IS NOT NULL
        ) t
        WHERE flag_last = 1; --no double id
        
        SET @end_time = GETDATE();
        PRINT '>> Duration: ' + CAST(DATEDIFF(second, @start_time, @end_time) AS NVARCHAR) + 's';

        --erp load&transform
        SET @start_time = GETDATE();
        PRINT '>> Truncating & Loading: silver.erp_auctions';
        TRUNCATE TABLE silver.erp_auctions;
        
        INSERT INTO silver.erp_auctions (scan_time, auction_id, item_id, quantity, unit_price_gold, time_left)
        SELECT 
            scan_time,
            auction_id,
            item_id,
            quantity,
            CAST(unit_price AS DECIMAL(18,4)) / 10000 AS unit_price_gold, --/10000 to set bronze to gold 
            TRIM(time_left)
        FROM (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY auction_id ORDER BY scan_time DESC) AS flag_last
            FROM bronze.erp_auctions
            WHERE auction_id IS NOT NULL
        ) t
        WHERE flag_last = 1; --We only keep the last flag
        
        SET @end_time = GETDATE();
        PRINT '>> Duration: ' + CAST(DATEDIFF(second, @start_time, @end_time) AS NVARCHAR) + 'seconds';

        SET @batch_end_time = GETDATE();
        PRINT '================================================';
        PRINT 'SUCCESS: Total Time ' + CAST(DATEDIFF(SECOND, @batch_start_time, @batch_end_time) AS NVARCHAR) + 'seconds';
    END TRY

    BEGIN CATCH
		PRINT '=========================================='
		PRINT 'ERROR OCCURED DURING LOADING SILVER LAYER'
		PRINT 'Error Message' + ERROR_MESSAGE();
		PRINT '=========================================='
	END CATCH
END