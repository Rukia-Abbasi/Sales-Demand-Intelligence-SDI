
import pandas as pd
from pathlib import Path
import subprocess
import sys

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def download_sales():
    subprocess.run(
        [sys.executable, "scripts/download_sales.py"],
        check=True
    )

def load_data():
    master = pd.read_csv(DATA_DIR / "01_master_data.csv")
    sales = pd.read_csv(DATA_DIR / "05_pharmacy_sales_data.csv")
    demand = pd.read_csv(DATA_DIR / "06_hospital_demand_data.csv")

    print("DATA INGESTION SUMMARY")
    print("----------------------")
    print("Master records:", len(master))
    print("Sales records:", len(sales))
    print("Hospital demand records:", len(demand))

    return master, sales, demand

if __name__ == "__main__":
    download_sales()
    load_data()
