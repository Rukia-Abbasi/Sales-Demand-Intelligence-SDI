
from pathlib import Path
import pandas as pd
import duckdb

DATA = Path("data")
OUT = Path("output")
OUT.mkdir(exist_ok=True)

print("Loading source datasets...")

master = pd.read_csv(DATA / "01_master_data.csv")
sales = pd.read_csv(DATA / "05_pharmacy_sales_data.csv")
demand = pd.read_csv(DATA / "06_hospital_demand_data.csv")

# 1. MEDICINE DIMENSION
medicine_columns = [
    "MedicineID",
    "GenericName",
    "FictionalBrandName",
    "DiseaseCategory",
    "TherapeuticClass"
]

dim_medicine = master[medicine_columns].drop_duplicates(
    subset=["MedicineID"]
).copy()

dim_medicine.insert(
    0, "MedicineKey", range(1, len(dim_medicine) + 1)
)

# 2. DATE DIMENSION
sales_dates = pd.to_datetime(sales["SalesDate"]).dt.normalize()

demand_dates = (
    pd.to_datetime(demand["DemandMonth"])
    .dt.to_period("M")
    .dt.to_timestamp()
)

all_dates = pd.concat(
    [sales_dates, demand_dates]
).drop_duplicates().sort_values()

dim_date = pd.DataFrame({"FullDate": all_dates})

dim_date.insert(
    0, "DateKey", range(1, len(dim_date) + 1)
)

dim_date["Year"] = dim_date["FullDate"].dt.year
dim_date["Month"] = dim_date["FullDate"].dt.month
dim_date["MonthName"] = dim_date["FullDate"].dt.month_name()
dim_date["Quarter"] = dim_date["FullDate"].dt.quarter

# 3. CHANNEL DIMENSION
channel = sales["PharmacyType"].copy()

channel = channel.where(
    channel != "Hospital Pharmacy", "Hospital"
)

channel = channel.where(
    sales["PharmacyType"] == "Hospital Pharmacy",
    sales["SalesChannel"]
)

channel = channel.replace({
    "Physical Pharmacy": "Retail"
})

sales["ChannelName"] = channel

dim_channel = pd.DataFrame({
    "ChannelName": sorted(channel.dropna().unique())
})

dim_channel.insert(
    0, "ChannelKey", range(1, len(dim_channel) + 1)
)

# 4. SALES FACT TABLE
sales["SalesDate"] = pd.to_datetime(
    sales["SalesDate"]
).dt.normalize()

sales = sales.merge(
    dim_medicine[["MedicineID", "MedicineKey"]],
    on="MedicineID",
    how="left"
)

sales = sales.merge(
    dim_date[["FullDate", "DateKey"]],
    left_on="SalesDate",
    right_on="FullDate",
    how="left"
)

sales = sales.merge(
    dim_channel,
    on="ChannelName",
    how="left"
)

sales["QuantitySoldPacks"] = pd.to_numeric(
    sales["QuantitySoldPacks"], errors="coerce"
).fillna(0)

sales["UnitRetailPriceUSD"] = pd.to_numeric(
    sales["UnitRetailPriceUSD"], errors="coerce"
).fillna(0)

if "NetSalesAmountUSD" not in sales.columns:
    sales["NetSalesAmountUSD"] = (
        sales["QuantitySoldPacks"] *
        sales["UnitRetailPriceUSD"]
    )

sales["NetSalesAmountUSD"] = pd.to_numeric(
    sales["NetSalesAmountUSD"], errors="coerce"
).fillna(0)

for col in ["CostOfGoodsSoldUSD", "GrossMarginUSD"]:
    if col not in sales.columns:
        sales[col] = 0

    sales[col] = pd.to_numeric(
        sales[col], errors="coerce"
    ).fillna(0)

if "GrossMarginUSD" not in sales.columns:
    sales["GrossMarginUSD"] = (
        sales["NetSalesAmountUSD"] -
        sales["CostOfGoodsSoldUSD"]
    )

if "SalesTransactionID" not in sales.columns:
    sales["SalesTransactionID"] = range(1, len(sales) + 1)

fact_sales = sales[[
    "SalesTransactionID",
    "DateKey",
    "MedicineKey",
    "ChannelKey",
    "QuantitySoldPacks",
    "NetSalesAmountUSD",
    "CostOfGoodsSoldUSD",
    "GrossMarginUSD"
]].copy()

# 5. HOSPITAL DEMAND FACT TABLE
demand["DemandMonth"] = (
    pd.to_datetime(demand["DemandMonth"])
    .dt.to_period("M")
    .dt.to_timestamp()
)

demand = demand.merge(
    dim_medicine[["MedicineID", "MedicineKey"]],
    on="MedicineID",
    how="left"
)

demand = demand.merge(
    dim_date[["FullDate", "DateKey"]],
    left_on="DemandMonth",
    right_on="FullDate",
    how="left"
)

demand_measures = [
    "ForecastDemandPacks",
    "RequestedQuantityPacks",
    "ApprovedQuantityPacks",
    "ReceivedQuantityPacks",
    "ConsumedQuantityPacks",
    "UnfulfilledDemandPacks",
    "StockoutDays",
    "ServiceLevelPct"
]

for col in demand_measures:
    if col in demand.columns:
        demand[col] = pd.to_numeric(
            demand[col], errors="coerce"
        ).fillna(0)
    else:
        demand[col] = 0

if "UnfulfilledDemandPacks" not in demand.columns:
    demand["UnfulfilledDemandPacks"] = (
        demand["RequestedQuantityPacks"] -
        demand["ReceivedQuantityPacks"]
    ).clip(lower=0)

fact_demand = demand[[
    "DateKey",
    "MedicineKey",
    "HospitalID"
] + demand_measures].copy()

# 6. CREATE DUCKDB WAREHOUSE
print("Creating analytical warehouse...")

db = duckdb.connect(str(OUT / "sdi_warehouse.duckdb"))

tables = {
    "dim_medicine": dim_medicine,
    "dim_date": dim_date,
    "dim_channel": dim_channel,
    "fact_sales": fact_sales,
    "fact_hospital_demand": fact_demand
}

for name, frame in tables.items():
    db.register("temp_frame", frame)

    db.execute(
        f"CREATE OR REPLACE TABLE {name} AS "
        "SELECT * FROM temp_frame"
    )

    db.unregister("temp_frame")

# 7. ANALYTICAL QUERY LAYER
queries = {
    "revenue_by_channel": """
        SELECT
            c.ChannelName,
            SUM(f.NetSalesAmountUSD) AS NetSalesUSD,
            SUM(f.GrossMarginUSD) AS GrossMarginUSD
        FROM fact_sales f
        JOIN dim_channel c
            ON f.ChannelKey = c.ChannelKey
        GROUP BY c.ChannelName
        ORDER BY NetSalesUSD DESC
    """,

    "hospital_demand_summary": """
        SELECT
            d.Year,
            d.Month,
            SUM(f.ForecastDemandPacks) AS ForecastPacks,
            SUM(f.ConsumedQuantityPacks) AS ConsumedPacks,
            SUM(f.UnfulfilledDemandPacks) AS UnfulfilledPacks
        FROM fact_hospital_demand f
        JOIN dim_date d
            ON f.DateKey = d.DateKey
        GROUP BY d.Year, d.Month
        ORDER BY d.Year, d.Month
    """,

    "top_medicines": """
        SELECT
            m.GenericName,
            SUM(f.QuantitySoldPacks) AS PacksSold,
            SUM(f.NetSalesAmountUSD) AS NetSalesUSD
        FROM fact_sales f
        JOIN dim_medicine m
            ON f.MedicineKey = m.MedicineKey
        GROUP BY m.GenericName
        ORDER BY PacksSold DESC
        LIMIT 10
    """
}

for name, sql in queries.items():
    result = db.execute(sql).df()
    result.to_csv(OUT / f"{name}.csv", index=False)
    print(f"Created query output: {name}.csv")

print("\nWAREHOUSE BUILD SUCCESSFUL")
print("Medicine dimension:", len(dim_medicine))
print("Date dimension:", len(dim_date))
print("Channel dimension:", len(dim_channel))
print("Sales fact:", len(fact_sales))
print("Hospital demand fact:", len(fact_demand))
print("Database:", OUT / "sdi_warehouse.duckdb")

db.close()
