
CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE IF NOT EXISTS staging.master_data (
    MedicineID TEXT,
    GenericName TEXT,
    FictionalBrandName TEXT,
    DiseaseCategory TEXT,
    TherapeuticClass TEXT
);

CREATE TABLE IF NOT EXISTS staging.pharmacy_sales (
    SalesTransactionID TEXT,
    SalesDate DATE,
    SalesChannel TEXT,
    PharmacyType TEXT,
    HospitalID TEXT,
    MedicineID TEXT,
    QuantitySoldPacks INTEGER,
    UnitRetailPriceUSD NUMERIC(12,2),
    GrossSalesAmountUSD NUMERIC(12,2),
    DiscountAmountUSD NUMERIC(12,2),
    NetSalesAmountUSD NUMERIC(12,2),
    CostOfGoodsSoldUSD NUMERIC(12,2),
    GrossMarginUSD NUMERIC(12,2)
);

CREATE TABLE IF NOT EXISTS staging.hospital_demand (
    HospitalDemandRecordID TEXT,
    DemandMonth DATE,
    HospitalID TEXT,
    MedicineID TEXT,
    ForecastDemandPacks INTEGER,
    RequestedQuantityPacks INTEGER,
    ApprovedQuantityPacks INTEGER,
    ReceivedQuantityPacks INTEGER,
    ConsumedQuantityPacks INTEGER,
    UnfulfilledDemandPacks INTEGER,
    StockoutDays INTEGER,
    ServiceLevelPct NUMERIC(8,2)
);
