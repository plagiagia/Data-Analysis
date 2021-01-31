/*Create a function which returns what’s the most profitable product 
category on average in a specific state across all years*/

CREATE PROCEDURE FindBestCategory
    @StateName VARCHAR(50)
AS
Select
    TOP 1 -- Take the first entry in table
    states.StateName,
    Year(order_events.OrderDate) As ORDER_YEAR,
    Avg(orders.Profit) As Avg_Profit,
    categories.CategoryName
From categories
    -- Join all the tables 
    Join sub_categories On sub_categories.CategoryID = categories.CategoryID
    Join products On products.SubCategoryID = sub_categories.SubCategoryID
    Join orders On orders.ProductID = products.ProductID
    Join order_events On orders.EventID = order_events.EventID
    Join customers On order_events.CustomerID = customers.CustomerID
    Join cities On customers.CityID = cities.CityID
    Join states On cities.StateID = states.StateID
    
Where
         states.StateName = @StateName -- Filter out the state's name
Group By -- Group by state, years and categories
         states.StateName,
         Year(order_events.OrderDate),
         categories.CategoryName
ORDER BY Avg_Profit DESC -- Order by AVERAGE profit in DESCENDING order;
