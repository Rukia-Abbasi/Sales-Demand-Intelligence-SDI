# Sales-Demand-Intelligence-SDI
Pharmaceutical Sales and Demand Intelligence Data Mart – Phase 1
# Sales & Demand Intelligence (SDI)

## Project Overview
Sales & Demand Intelligence is a pharmaceutical data warehousing project designed to analyze medicine sales, hospital demand, and supply chain performance.

## Phase 1 – Milestone 1
**Scope:** Data ingestion, validation, staging, transformation, dimensional modeling, and analytical SQL query layer.

## Datasets
- `01_master_data.csv` – Medicine master data.
- `05_pharmacy_sales_data.csv` – Pharmacy sales transactions (hosted on Google Drive because of its file size).
- `06_hospital_demand_data.csv` – Monthly hospital demand records.

## Technology Stack
- Python and Pandas
- PostgreSQL
- SQL
- DuckDB
- Apache Airflow
- GitHub

## Repository Structure
```text
data/
scripts/
    download_sales.py
    ingestion.py
    validation.py
    transformations.py
sql/
    staging.sql
    star_schema.sql
    analytical_queries.sql
requirements.txt
```

## Analytical Objectives
1. Analyze revenue and gross margin by sales channel.
2. Compare hospital forecast demand with actual consumption.
3. Identify fast-moving medicines.
4. Identify medicines with the highest unfulfilled hospital demand.

## Project Status
Initial source files and SQL designs have been committed. Execution, integration, and validation remain to be completed.

