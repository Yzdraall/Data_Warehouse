# WoW Economy Data Warehouse (ETL Pipeline)

A comprehensive Data Engineering project designed to Extract, Transform, and Load (ETL) real-time economic data from the World of Warcraft Auction House (Hyjal Server) into a local SQL Server Data Warehouse.

## Why World of Warcraft?
MMORPGs serve as massive sandbox environments that closely mirror real-world human behavior. Just as the infamous "Corrupted Blood" virtual epidemic in WoW was utilized by epidemiologists to model real-world disease spread in recognized scientific papers, the game's Auction House provides a highly consistent, data-rich ecosystem. It is an ideal testing ground to study real-world economic principles such as inflation, market manipulation, and supply/demand elasticity using millions of active, player-driven data points.

## Project Objective
Automate the extraction of massive transaction datasets to build a resilient data architecture, allowing for advanced analytics on a dynamic virtual economy.

## Technical Architecture
* **Extract:** Automated Python script querying the official Blizzard REST API (bypassing strict WAF restrictions via custom HTTP headers).
* **Transform:** JSON payload parsing and creation of a static reference dictionary (CRM) mapping numeric IDs to readable item names and qualities.
* **Load:** Massive data ingestion (`BULK INSERT`) of flat files into a local **SQL Server** database.
* **Orchestration:** Python-based daemon for hourly data collection (Local Data Lake creation).

## Repository Structure
* `extract_crm_items.py` : Generates the static item dictionary (CRM).
* `extract_erp_auctions.py` : One-shot extraction of active Auction House transactions (ERP).
* `auto_collector.py` : Automated daemon for hourly historical data collection.
* `transform_lua.py` : Regex-based parsing script to convert third-party Lua add-on data into clean CSVs.

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

*Note: The current DWH is built on SQL Server, but the raw layer ingestion logic and standard SQL syntax used are designed to be easily adaptable to PostgreSQL environments for future scaling or external datasets.* 😉
