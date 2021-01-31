/*Create a function to return the total revenue generated per vendor (Manufacturer) every year

Sales Revenue = Units Sold x Sales Price*/

Select
    manufactureres.Manufacturer,
    Sum(orders.Sales * orders.Quantity) As Revenue,
    Year(order_events.OrderDate) As OrderDate
From
    orders
    Inner Join
    products
    On orders.ProductID = products.ProductID
    Inner Join manufactureres
    On products.ManufacturerID = manufactureres.ManufacturerID
    Inner Join order_events
    On orders.EventID = order_events.EventID
Group By
    manufactureres.Manufacturer,
    Year(order_events.OrderDate)
Order By
    manufactureres.Manufacturer,
    OrderDate;