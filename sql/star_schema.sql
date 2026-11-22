
CREATE SCHEMA IF NOT EXISTS warehouse;

CREATE TABLE IF NOT EXISTS warehouse.dim_medicine (
    MedicineKey INTEGER PRIMARY KEY,
    MedicineID TEXT UNIQUE,
    GenericName TEXT,
    FictionalBrandName TEXT,
    DiseaseCategory TEXT,
    TherapeuticClass TEXT
);

CREATE TABLE IF NOT EXISTS warehouse.dim_date (
    DateKey INTEGER PRIMARY KEY,
    FullDate DATE UNIQUE,
    Year INTEGER,
    Month INTEGER,
    MonthName TEXT,
    Quarter INTEGER
);

CREATE TABLE IF NOT EXISTS warehouse.dim_channel (
    ChannelKey INTEGER PRIMARY KEY,
    ChannelName TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS warehouse.fact_sales (
    SalesTransactionID TEXT,
    DateKey INTEGER,
    MedicineKey INTEGER,
    ChannelKey INTEGER,
    QuantitySoldPacks INTEGER,
    NetSalesAmountUSD NUMERIC(12,2),
    CostOfGoodsSoldUSD NUMERIC(12,2),
    GrossMarginUSD NUMERIC(12,2)
);

CREATE TABLE IF NOT EXISTS warehouse.fact_hospital_demand (
    HospitalDemandRecordID TEXT,
    DateKey INTEGER,
    MedicineKey INTEGER,
    HospitalID TEXT,
    ForecastDemandPacks INTEGER,
    RequestedQuantityPacks INTEGER,
    ApprovedQuantityPacks INTEGER,
    ReceivedQuantityPacks INTEGER,
    ConsumedQuantityPacks INTEGER,
    UnfulfilledDemandPacks INTEGER,
    StockoutDays INTEGER,
    ServiceLevelPct NUMERIC(8,2)
);
