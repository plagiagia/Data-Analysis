-- Create a function which return all the details of the transactions with Profit < 0%

Select
    categories.CategoryName,
    sub_categories.SubCategoryName,
    products.ProductName,
    manufactureres.Manufacturer,
    orders.Quantity,
    orders.Sales,
    orders.Discount,
    orders.Profit,
    order_events.OrderDate,
    order_events.ShipDate,
    customers.CustomerName,
    postal_codes.PostalCode,
    cities.CityName,
    states.StateName,
    regions.RegionName,
    countries.CountryName
From
    categories Inner Join
    sub_categories On sub_categories.CategoryID = categories.CategoryID Inner Join
    products On products.SubCategoryID = sub_categories.SubCategoryID Inner Join
    manufactureres On products.ManufacturerID = manufactureres.ManufacturerID Inner Join
    orders On orders.ProductID = products.ProductID Inner Join
    order_events On orders.EventID = order_events.EventID Inner Join
    customers On order_events.CustomerID = customers.CustomerID Inner Join
    postal_codes On customers.PostalCodeID = postal_codes.PostalCodeID Inner Join
    cities On postal_codes.CityID = cities.CityID Inner Join
    states On cities.StateID = states.StateID Inner Join
    regions On states.RegionID = regions.RegionID Inner Join
    countries On regions.CountyID = countries.CountryID
Where
    orders.Profit < 0
ORDER BY Profit;