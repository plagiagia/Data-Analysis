/*Create a new boolean column in the customers' table called “is_top_customer” it will set to 1 if the customer is 
one of the company's top customers and to 0 if not*/

Select 
    customers.CustomerName,
    Sum(orders.Sales) As Sum_Sales,
    customers.CustomerID,
    CASE
    WHEN Sum(orders.Sales) BETWEEN 8804 AND 23661 THEN 1
    ELSE 0
    END AS is_top_customer
From
    customers Inner Join
    order_events On order_events.CustomerID = customers.CustomerID Inner Join
    orders On orders.EventID = order_events.EventID
Group By
    customers.CustomerName,
    customers.CustomerID
Order By
    Sum_Sales Desc;

