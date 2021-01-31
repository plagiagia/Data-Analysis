/*Create a function which takes a state and returns the most profitable City in this State and the 
average annual profit for that city across all years in that city

Plan:

First, we have to look for the most profitable city in the given state. So after we join the needed tables we
take top 1 city from the t1 temporary table. (1)

Now we have the name of the city we can make another join on the city name and city ID to have only the relevant columns
in our new table (2)
*/





CREATE PROCEDURE FindAnnualProfit @StateName varchar(50) AS
-- ================================================================================ (2) 
SELECT cities.CityName,
       YEAR(order_events.OrderDate) AS YEAR,
       AVG(orders.Profit) AS AVG_PROFIT
FROM
-- ================================================================================ (1)
  (SELECT TOP 1 cities.CityName,
              SUM(orders.Profit) AS SUM_PROFIT,
              cities.CityID
   FROM states
   JOIN cities ON cities.StateID = states.StateID
   JOIN customers ON customers.CityID = cities.CityID
   JOIN order_events ON order_events.CustomerID = customers.CustomerID
   JOIN orders ON orders.EventID = order_events.EventID
   WHERE states.StateName = @StateName
   GROUP BY cities.CityName,
            cities.CityID
   ORDER BY SUM_PROFIT DESC) AS t1
-- ================================================================================ (1)
JOIN cities ON cities.CityID = t1.CityID
JOIN customers ON customers.CityID = cities.CityID
JOIN order_events ON order_events.CustomerID = customers.CustomerID
JOIN orders ON orders.EventID = order_events.EventID
GROUP BY YEAR(order_events.OrderDate),
         cities.CityName;   
-- ================================================================================ (2)