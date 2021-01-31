-- For each product category the company wants to know what is the total profit per region

Select
    regions.RegionName,
    categories.CategoryName,
    Sum(orders.Profit) As Sum_Profit
From
    regions
    Inner Join states On states.RegionID = regions.RegionID
    Inner Join cities On cities.StateID = states.StateID
    Inner Join postal_codes On postal_codes.CityID = cities.CityID
    Inner Join customers On customers.PostalCodeID = postal_codes.PostalCodeID
    Inner Join order_events On order_events.CustomerID = customers.CustomerID
    Inner Join orders On orders.EventID = order_events.EventID
    Inner Join products On orders.ProductID = products.ProductID
    Inner Join sub_categories On products.SubCategoryID = sub_categories.SubCategoryID
    Inner Join categories On sub_categories.CategoryID = categories.CategoryID
Group By
    regions.RegionName,
    categories.CategoryName
Order By
    regions.RegionName,
    categories.CategoryName



