# Azure ETL Pipeline — End-to-End Data Engineering Project

## Overview
A complete end-to-end batch ETL pipeline built on Azure using PySpark, 
Delta Lake, and the Medallion Architecture (Bronze/Silver/Gold).

## Architecture
- **Source data** — CSV, SQLite, JSON, FastAPI (reviews)
- **Storage** — Azure Data Lake Storage Gen2
- **Processing** — Azure Databricks + PySpark
- **Format** — Delta Lake (ACID transactions, time travel)
- **Orchestration** — Azure Data Factory
- **Secrets** — Azure Key Vault

## Medallion Architecture
- **Bronze** — Raw ingestion from all sources
- **Silver** — Cleaned, validated, deduplicated, joined
- **Gold** — Business aggregations ready for analytics

## Data Sources
| Source | Format | Rows |
|--------|--------|------|
| Orders | CSV | 1,000 |
| Customers | SQLite → CSV | 100 |
| Products | JSON | 50 |
| Reviews | FastAPI (paginated) | 5,220 |

## Data Quality
- Intentional dirty data added (null IDs, negative prices, null ratings)
- DQ checks flag invalid rows with specific issue codes
- Quarantine table stores bad rows for investigation

## Gold Tables
- `daily_sales` — Revenue, orders, unique customers per day
- `customer_ltv` — Lifetime value, tier, days since last order
- `product_performance` — Revenue, profit margin, avg rating per product

## Tech Stack
- Python 3.14
- PySpark / Apache Spark 3.4
- Delta Lake
- Azure ADLS Gen2
- Azure Databricks
- Azure Data Factory
- Azure Key Vault
- FastAPI + Uvicorn
- Git / GitHub