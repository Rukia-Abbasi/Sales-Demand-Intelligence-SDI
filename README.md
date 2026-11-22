# Sales & Demand Intelligence (SDI)

## Project Overview
Sales & Demand Intelligence (SDI) is a data warehousing project focused on analyzing pharmaceutical sales and hospital medicine demand.

## Phase 1 – Current Implementation

### 1. Data Sources
- `01_master_data.csv` – Medicine master data
- `05_pharmacy_sales_data.csv` – Pharmacy sales transactions
- `06_hospital_demand_data.csv` – Hospital demand records

The large sales dataset is downloaded from Google Drive during the automated workflow.

### 2. Data Ingestion and Validation
Python scripts are used to load the source datasets and validate important fields, including:
- Valid sales dates
- Non-null medicine IDs
- Positive retail prices
- Valid hospital demand dates and identifiers

### 3. Data Transformation and Warehouse
The project builds a dimensional analytical warehouse using DuckDB.

Warehouse tables:
- `dim_medicine`
- `dim_date`
- `dim_channel`
- `fact_sales`
- `fact_hospital_demand`

### 4. Analytical Query Layer
The project generates three analytical outputs:
- Revenue and gross margin by sales channel
- Hospital demand forecast, consumption and unfulfilled demand
- Top 10 medicines by packs sold

### 5. Automated Execution
GitHub Actions runs the data download, validation, warehouse-building and query-export steps.

The workflow also saves the database and query outputs as downloadable artifacts.

## Technology Stack
- Python
- Pandas
- DuckDB
- SQL
- GitHub
- GitHub Actions

## Current Status
The initial ingestion, validation, dimensional warehouse build and analytical query export have been executed successfully through GitHub Actions.

**Implementation note:** DuckDB is currently used for the working analytical warehouse. PostgreSQL and Apache Airflow have not yet been deployed.

## Repository Structure

```text
Sales-Demand-Intelligence-SDI/
├── data/
├── scripts/
│   ├── download_sales.py
│   ├── ingestion.py
│   ├── validation.py
│   ├── transformations.py
│   └── build_warehouse.py
├── sql/
│   ├── staging.sql
│   ├── star_schema.sql
│   └── analytical_queries.sql
├── .github/
│   └── workflows/
│       └── validate.yml
├── requirements.txt
└── README.md
```
