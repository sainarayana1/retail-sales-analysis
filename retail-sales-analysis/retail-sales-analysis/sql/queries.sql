-- Retail Sales Performance Analysis - SQL queries (SQLite syntax, works in MySQL with minor changes)

-- Q1. Overall KPIs
SELECT ROUND(SUM(Sales),2) AS total_sales, ROUND(SUM(Profit),2) AS total_profit,
       COUNT(DISTINCT Order_ID) AS total_orders, ROUND(SUM(Profit)*100.0/SUM(Sales),2) AS profit_margin_pct
FROM orders;

-- Q2. Monthly sales and profit trend
SELECT Year_Month, ROUND(SUM(Sales),2) AS sales, ROUND(SUM(Profit),2) AS profit
FROM orders GROUP BY Year_Month ORDER BY Year_Month;

-- Q3. Year-over-year sales growth (window function LAG)
WITH yearly AS (SELECT Year, SUM(Sales) AS sales FROM orders GROUP BY Year)
SELECT Year, ROUND(sales,2) AS sales,
       ROUND((sales - LAG(sales) OVER (ORDER BY Year)) * 100.0 / LAG(sales) OVER (ORDER BY Year), 2) AS yoy_growth_pct
FROM yearly;

-- Q4. Top 10 products by sales
SELECT Product_Name, ROUND(SUM(Sales),2) AS sales, ROUND(SUM(Profit),2) AS profit
FROM orders GROUP BY Product_Name ORDER BY sales DESC LIMIT 10;

-- Q5. Profit by region and category
SELECT Region, Category, ROUND(SUM(Sales),2) AS sales, ROUND(SUM(Profit),2) AS profit,
       ROUND(SUM(Profit)*100.0/SUM(Sales),2) AS margin_pct
FROM orders GROUP BY Region, Category ORDER BY Region, profit DESC;

-- Q6. Loss-making sub-categories when discount is above 20%
SELECT Sub_Category, COUNT(*) AS line_items, ROUND(SUM(Profit),2) AS total_profit
FROM orders WHERE Discount > 0.2
GROUP BY Sub_Category HAVING SUM(Profit) < 0 ORDER BY total_profit;

-- Q7. Discount band vs profit (KEY INSIGHT)
SELECT CASE WHEN Discount = 0 THEN '0%' WHEN Discount <= .2 THEN '1-20%'
            WHEN Discount <= .4 THEN '21-40%' ELSE '>40%' END AS discount_band,
       COUNT(*) AS line_items, ROUND(SUM(Sales),2) AS sales, ROUND(SUM(Profit),2) AS profit,
       ROUND(SUM(Profit)*100.0/SUM(Sales),2) AS margin_pct
FROM orders GROUP BY discount_band ORDER BY MIN(Discount);

-- Q8. Top 10 customers by sales
SELECT Customer_ID, Customer_Name, COUNT(DISTINCT Order_ID) AS orders, ROUND(SUM(Sales),2) AS sales
FROM orders GROUP BY Customer_ID, Customer_Name ORDER BY sales DESC LIMIT 10;

-- Q9. Top 3 customers inside each segment (window function RANK)
SELECT * FROM (
  SELECT Segment, Customer_Name, ROUND(SUM(Sales),2) AS sales,
         RANK() OVER (PARTITION BY Segment ORDER BY SUM(Sales) DESC) AS rnk
  FROM orders GROUP BY Segment, Customer_ID, Customer_Name
) WHERE rnk <= 3;

-- Q10. Average shipping days by ship mode
SELECT Ship_Mode, ROUND(AVG(Ship_Days),2) AS avg_ship_days, COUNT(DISTINCT Order_ID) AS orders
FROM orders GROUP BY Ship_Mode ORDER BY avg_ship_days;
