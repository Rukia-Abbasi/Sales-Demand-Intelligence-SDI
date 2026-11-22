
import pandas as pd

def prepare_medicine_dimension(master):
    dim = master[
        [
            "MedicineID",
            "GenericName",
            "FictionalBrandName",
            "DiseaseCategory",
            "TherapeuticClass"
        ]
    ].drop_duplicates(subset=["MedicineID"]).copy()

    dim.insert(0, "MedicineKey", range(1, len(dim) + 1))
    return dim


def prepare_date_dimension(sales, demand):
    sales_dates = pd.to_datetime(sales["SalesDate"])
    demand_dates = pd.to_datetime(demand["DemandMonth"])

    dates = pd.concat([
        sales_dates.dt.normalize(),
        demand_dates.dt.to_period("M").dt.to_timestamp()
    ]).drop_duplicates().sort_values()

    dim = pd.DataFrame({"FullDate": dates})
    dim.insert(0, "DateKey", range(1, len(dim) + 1))

    dim["Year"] = dim["FullDate"].dt.year
    dim["Month"] = dim["FullDate"].dt.month
    dim["MonthName"] = dim["FullDate"].dt.month_name()
    dim["Quarter"] = dim["FullDate"].dt.quarter

    return dim


def prepare_channel_dimension(sales):
    channels = sales["PharmacyType"].copy()

    channels = channels.where(
        channels != "Hospital Pharmacy",
        "Hospital"
    )

    channels = channels.where(
        sales["PharmacyType"] == "Hospital Pharmacy",
        sales["SalesChannel"]
    )

    channels = channels.replace({
        "Physical Pharmacy": "Retail"
    })

    dim = pd.DataFrame({
        "ChannelName": sorted(channels.dropna().unique())
    })

    dim.insert(0, "ChannelKey", range(1, len(dim) + 1))
    return dim
