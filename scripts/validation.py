
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")

def validate_sales(df):
    required = [
        "SalesDate",
        "MedicineID",
        "QuantitySoldPacks",
        "UnitRetailPriceUSD"
    ]

    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing sales column: {col}")

    df["SalesDate"] = pd.to_datetime(df["SalesDate"], errors="coerce")

    assert df["SalesDate"].notna().all(), "Invalid sales dates found"
    assert df["MedicineID"].notna().all(), "Null MedicineID found"
    assert (df["UnitRetailPriceUSD"] > 0).all(), "Invalid sales prices found"

    return df


def validate_hospital_demand(df):
    required = [
        "DemandMonth",
        "HospitalID",
        "MedicineID",
        "ForecastDemandPacks",
        "ConsumedQuantityPacks"
    ]

    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing hospital demand column: {col}")

    df["DemandMonth"] = pd.to_datetime(
        df["DemandMonth"], errors="coerce"
    )

    assert df["DemandMonth"].notna().all(), "Invalid demand months found"
    assert df["HospitalID"].notna().all(), "Null HospitalID found"
    assert df["MedicineID"].notna().all(), "Null MedicineID found"

    return df


if __name__ == "__main__":
    sales_path = DATA_DIR / "05_pharmacy_sales_data.csv"
    demand_path = DATA_DIR / "06_hospital_demand_data.csv"

    sales = pd.read_csv(sales_path)
    demand = pd.read_csv(demand_path)

    validate_sales(sales)
    validate_hospital_demand(demand)

    print("Sales and hospital demand validation passed.")
