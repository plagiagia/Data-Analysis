-- Create a function which returns whats was the most profitable month in each year

CREATE PROCEDURE FindBestMonthByYears
AS
WITH
    -- Create a temporal table to store the sums of profits for each month in each year
    table_sum_profit_per_month
    AS
    (
        SELECT
            YEAR(OrderDate) AS YEAR,
            MONTH(OrderDate) AS MONTH,
            SUM(orders.Profit) AS SUM_PROFIT
        FROM orders
            JOIN order_events
            ON orders.EventID = order_events.EventID
        GROUP BY YEAR(OrderDate),
                MONTH(OrderDate)
    ),
    table_max_profit_month_per_year
    AS
    /*Create a second temporal table which calculates with a window function 
    the max profit from the previous table for each year*/
    (
        SELECT
            YEAR,
            MONTH,
            MAX(SUM_PROFIT) OVER (PARTITION BY YEAR) AS MAX_PROFIT
        -- Window function
        FROM table_sum_profit_per_month
    )

-- Just join the two tables to filter out only the months and years with the max values
SELECT table_sum_profit_per_month.YEAR, table_sum_profit_per_month.MONTH, table_max_profit_month_per_year.MAX_PROFIT
FROM
    table_max_profit_month_per_year
    JOIN table_sum_profit_per_month
    ON table_max_profit_month_per_year.YEAR = table_sum_profit_per_month.YEAR
        AND table_max_profit_month_per_year.MONTH = table_sum_profit_per_month.MONTH
        AND table_max_profit_month_per_year.MAX_PROFIT = table_sum_profit_per_month.SUM_PROFIT
ORDER BY 1, 2
