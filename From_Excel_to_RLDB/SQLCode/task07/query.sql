/*Create a function which returns what is the most popular product in a specific category in a specific year*/



CREATE PROCEDURE FindPopularCategory
    @Category VARCHAR(50),
    @Year int
AS
-- Create a temporal table that holds all the information about the products in a specific year
WITH
    products_table    -- Temporal's table name
    AS
    (
        Select
            categories.CategoryName,
            products.ProductName,
            Year(order_events.OrderDate) AS order_year
        From
            categories
            -- Join all the tables to get the needed information
            Join sub_categories On sub_categories.CategoryID = categories.CategoryID
            Join products On products.SubCategoryID = sub_categories.SubCategoryID
            Join orders On orders.ProductID = products.ProductID
            Join order_events On orders.EventID = order_events.EventID
        Where
        categories.CategoryName = @Category And --Filter the category name (ex. Technology)
            Year(order_events.OrderDate) = @Year -- Filter the year (ex. 2018)
    )
Select
    TOP 1
    -- Take the first entry of the table
    Count(products_table.ProductName) As Popularity, -- Count how many times a product occurs in the specific year
    products_table.ProductName
-- Show the product's name
From products_table
GROUP BY
-- Groub the temporal table
products_table.ProductName,
products_table.order_year
Order By
    Popularity Desc;