-- Fill categories
INSERT INTO categories
    (CategoryName)
SELECT DISTINCT(Category)
FROM RAW_data
WHERE Category IS NOT NULL;

-- Fill sub_categories
INSERT INTO sub_categories
    (SubCategoryName, CategoryID)
Select
    t1.[Sub-Category],
    categories.CategoryID
From
    (Select
        RAW_data.[Sub-Category],
        RAW_data.Category
    From
        RAW_data
    Group By
         RAW_data.[Sub-Category],
         RAW_data.Category) As t1 Inner Join
    categories On t1.Category = categories.CategoryName

-- Fill Manufacturers
INSERT INTO manufactureres
    (Manufacturer)
SELECT DISTINCT(Manufacturer)
FROM RAW_data
WHERE Manufacturer IS NOT NULL;

-- Fill Products
INSERT INTO products
    (ProductName, ManufacturerID, SubCategoryID)
Select
    t1.[Product Name],
    manufactureres.ManufacturerID,
    sub_categories.SubCategoryID
From
    (Select
        RAW_data.[Product Name],
        RAW_data.Manufacturer,
        RAW_data.[Sub-Category]
    From
        RAW_data
    Group By
         RAW_data.[Product Name],
         RAW_data.Manufacturer,
         RAW_data.[Sub-Category]) As t1 Inner Join
    manufactureres On t1.Manufacturer = manufactureres.Manufacturer Inner Join
    sub_categories On t1.[Sub-Category] = sub_categories.SubCategoryName

-- Fill countries
INSERT INTO countries
    (CountryName)
SELECT DISTINCT(Country)
FROM RAW_data
WHERE Country IS NOT NULL;

-- Fill Regions
INSERT INTO regions
    (RegionName,CountyID)
SELECT t1.Region, countries.CountryID
FROM(SELECT Region, Country
    FROM RAW_data
    GROUP BY Region, Country) AS t1 INNER JOIN
    countries ON t1.Country=countries.CountryName;

-- Fill States
INSERT INTO states
    (StateName, RegionID)
SELECT [State], RegionID
FROM (SELECT DISTINCT[State], Region
    FROM RAW_data) AS t1
    INNER JOIN regions
    ON regions.RegionName = t1.Region

-- Fill cities
INSERT INTO cities
    (CityName, StateID)
SELECT t1.City, StateID
FROM (SELECT DISTINCT [City], [State]
    FROM RAW_data) AS t1
    INNER JOIN states
    ON states.StateName = t1.[State]


-- Fill postal codes
INSERT INTO postal_codes
    (PostalCode, postal_codes.CityID)
Select t1.[Postal Code], cities.CityID
From
    (Select Distinct
        RAW_data.City,
        RAW_data.State,
        RAW_data.[Postal Code]
    From
        RAW_data) As t1
    Inner Join cities On t1.City = cities.CityName
    Inner Join states On cities.StateID = states.StateID And t1.State = states.StateName

-- FIll customers
INSERT INTO customers
    (CustomerName, PostalCodeID)
Select
    t1.[Customer Name],
    postal_codes.PostalCodeID
From
    postal_codes Inner Join
    cities On postal_codes.CityID = cities.CityID Inner Join
    (Select
        RAW_data.[Customer Name],
        RAW_data.[Postal Code],
        RAW_data.City
    From
        RAW_data
    Group By
         RAW_data.[Customer Name],
         RAW_data.[Postal Code],
         RAW_data.City) t1 On t1.[Postal Code] = postal_codes.PostalCode
        And t1.City = cities.CityName

-- Fill order_events
INSERT INTO order_events
    (EventID, OrderDate, ShipDate, CustomerID)
Select
    t1.[Order ID],
    t1.[Order Date],
    t1.[Ship Date],
    customers.CustomerID
From
    (Select
        RAW_data.[Order ID],
        RAW_data.[Order Date],
        RAW_data.[Ship Date],
        RAW_data.[Customer Name],
        RAW_data.[Postal Code]
    From
        RAW_data
    Group By
         RAW_data.[Order ID],
         RAW_data.[Order Date],
         RAW_data.[Ship Date],
         RAW_data.[Customer Name],
         RAW_data.[Postal Code]) t1 Inner Join
    customers On t1.[Customer Name] = customers.CustomerName Inner Join
    postal_codes On customers.PostalCodeID = postal_codes.PostalCodeID
        And t1.[Postal Code] = postal_codes.PostalCode

-- Fill orders
INSERT INTO orders
    (EventID, ProductID, Quantity, Sales, Discount, Profit)
Select
    order_events.EventID,
    products.ProductID,
    t1.Quantity,
    t1.Sales,
    t1.Discount,
    t1.Profit
From
    (Select
        RAW_data.[Order ID],
        RAW_data.[Product Name],
        RAW_data.Quantity,
        RAW_data.Sales,
        RAW_data.Discount,
        RAW_data.Profit
    From
        RAW_data) As t1 Inner Join
    order_events On t1.[Order ID] = order_events.EventID Inner Join
    products On t1.[Product Name] = products.ProductName
    