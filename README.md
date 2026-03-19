# WoW Economy Data Warehouse (ETL Pipeline)

A comprehensive Data Engineering project designed to Extract, Transform, and Load (ETL) real-time economic data from the World of Warcraft Auction House (Hyjal Server) into a local SQL Server Data Warehouse.

## Why World of Warcraft?
MMORPGs serve as massive sandbox environments that closely mirror real-world human behavior. Just as the infamous "Corrupted Blood" virtual epidemic in WoW was utilized by epidemiologists to model real-world disease spread in recognized scientific papers, the game's Auction House provides a highly consistent, data-rich ecosystem. It is an ideal testing ground to study real-world economic principles such as inflation, market manipulation, and supply/demand elasticity using millions of active, player-driven data points.

## Project Objective
Automate the extraction of massive transaction datasets to build a resilient data architecture, allowing for advanced analytics on a dynamic virtual economy.

## Technical Architecture
* **Extract:** Automated Python script querying the official Blizzard REST API (bypassing strict WAF restrictions via custom HTTP headers).
* **Transform:** SQL-based transformations in Silver layer (deduplication, type casting, normalization)
* **Load:** Massive data ingestion (`BULK INSERT`) of flat files into a local **SQL Server** database.
* **Orchestration:** Python-based daemon for hourly data collection (Local Data Lake creation).

### Data Modeling & Processing
- Implementation of a Medallion Architecture (Bronze, Silver, Gold)
- SQL-based data transformation (ELT approach)
- Data cleaning and deduplication in Silver layer

## Data Processing Strategy

This project follows an ELT approach:
- Raw data is ingested without modification
- Transformations are performed directly in SQL
- This ensures scalability and reproducibility of data pipelines

The database is structured using dedicated schemas:

- `bronze` → raw ingested data (no transformation)
- `silver` → cleaned, deduplicated, and normalized data
- `gold` → business-ready analytical models (in progress)



## Repository Structure

### Python Scripts

- `extract_erp_auctions.py`
  → Extracts live auction data from Blizzard API and saves it as CSV

- `extract_crm_items.py`
  → Builds a reference dataset mapping item IDs to names, quality, and class

- `auto_collector.py`
  → Runs continuously to collect auction snapshots over time (historical tracking)

- `lua_parser.py`
  → Parses Lua addon files and converts them into clean CSV datasets

---

### SQL Scripts

- `init_database.sql`
  → Creates the `wow_economy` database and initializes schemas:
  (`bronze`, `silver`, `gold`)

- `01_ddl_bronze_layer.sql`
  → Defines raw tables in the `bronze` schema:
  - `bronze.erp_auctions`
  - `bronze.crm_items`

- `02_load_bronze_layer.sql`
  → Loads CSV data into bronze tables using `BULK INSERT`


## How to Run
1. Clone the repository.
2. Add your Blizzard API credentials to a `.env` file.
3. Generate the static reference table: `python extract_crm_items.py`
4. Start the hourly data collection daemon: `python auto_collector.py`

*(Note: For security and storage optimization, raw data files (.csv, .json), and client tokens are excluded from this repository via `.gitignore`).*

## Current Progress: Medallion Architecture
* **[x] Bronze Layer:** Implemented automated massive data ingestion of flat CSV files into a local SQL Server database. The raw layer schema strictly mirrors the source API extracts to ensure zero data loss and historical tracking.
* **[ ] Silver Layer:** Pending (Data cleansing, deduplication, and type casting).
* **[ ] Gold Layer:** Pending (Star schema modeling for analytical consumption).

*(Note: The current DWH is built on SQL Server, but the raw layer ingestion logic and standard SQL syntax used are designed to be easily adaptable to PostgreSQL environments for future scaling or external datasets.)*
