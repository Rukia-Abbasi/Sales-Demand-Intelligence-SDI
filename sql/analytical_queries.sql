
-- QUERY 1: Revenue and gross margin by sales channel
SELECT
    c.ChannelName,
    SUM(f.NetSalesAmountUSD) AS TotalRevenueUSD,
    SUM(f.GrossMarginUSD) AS TotalGrossMarginUSD,
    SUM(f.QuantitySoldPacks) AS TotalPacksSold
FROM warehouse.fact_sales f
JOIN warehouse.dim_channel c
    ON f.ChannelKey = c.ChannelKey
GROUP BY c.ChannelName
ORDER BY TotalRevenueUSD DESC;


-- QUERY 2: Hospital demand vs actual consumption
SELECT
    d.Year,
    d.Month,
    SUM(h.ForecastDemandPacks) AS ForecastDemand,
    SUM(h.ConsumedQuantityPacks) AS ActualConsumption,
    SUM(h.UnfulfilledDemandPacks) AS UnfulfilledDemand
FROM warehouse.fact_hospital_demand h
JOIN warehouse.dim_date d
    ON h.DateKey = d.DateKey
GROUP BY d.Year, d.Month
ORDER BY d.Year, d.Month;


-- QUERY 3: Top 10 fast-moving medicines
SELECT
    m.GenericName,
    SUM(f.QuantitySoldPacks) AS TotalPacksSold
FROM warehouse.fact_sales f
JOIN warehouse.dim_medicine m
    ON f.MedicineKey = m.MedicineKey
GROUP BY m.GenericName
ORDER BY TotalPacksSold DESC
LIMIT 10;


-- QUERY 4: Medicines with highest unfulfilled hospital demand
SELECT
    m.GenericName,
    SUM(h.UnfulfilledDemandPacks) AS TotalUnfulfilledDemand
FROM warehouse.fact_hospital_demand h
JOIN warehouse.dim_medicine m
    ON h.MedicineKey = m.MedicineKey
GROUP BY m.GenericName
ORDER BY TotalUnfulfilledDemand DESC
LIMIT 10;
