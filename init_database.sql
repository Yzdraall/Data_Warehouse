/*
=============================================================
Create Database and Schemas
=============================================================
*/

USE master;
GO

--drop & recreate database safely
IF EXISTS (SELECT 1 FROM sys.databases WHERE name = 'wow_economy')
BEGIN
    ALTER DATABASE wow_economy SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE wow_economy;
END;
GO

CREATE DATABASE wow_economy;
GO

USE wow_economy;
GO

--create medallion schemas
CREATE SCHEMA bronze;
GO

CREATE SCHEMA silver;
GO

CREATE SCHEMA gold;
GO