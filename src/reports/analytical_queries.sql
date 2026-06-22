-- Q1 Top 10 Companies by ROE
SELECT company_name, roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;

-- Q2 Top 10 Companies by ROCE
SELECT company_name, roce_percentage
FROM companies
ORDER BY roce_percentage DESC
LIMIT 10;

-- Q3 Top 10 Companies by Book Value
SELECT company_name, book_value
FROM companies
ORDER BY book_value DESC
LIMIT 10;

-- Q4 Highest Net Profit
SELECT company_id, year, net_profit
FROM profitandloss
ORDER BY net_profit DESC
LIMIT 10;

-- Q5 Highest Sales
SELECT company_id, year, sales
FROM profitandloss
ORDER BY sales DESC
LIMIT 10;

-- Q6 Highest Borrowings
SELECT company_id, year, borrowings
FROM balancesheet
ORDER BY borrowings DESC
LIMIT 10;

-- Q7 Highest Total Assets
SELECT company_id, year, total_assets
FROM balancesheet
ORDER BY total_assets DESC
LIMIT 10;

-- Q8 Sector Wise Company Count
SELECT broad_sector,
COUNT(*) AS company_count
FROM sectors
GROUP BY broad_sector
ORDER BY company_count DESC;

-- Q9 Average Closing Price by Company
SELECT company_id,
AVG(close_price) AS avg_close_price
FROM stock_prices
GROUP BY company_id
ORDER BY avg_close_price DESC
LIMIT 10;

-- Q10 Companies with Highest Market Capitalization
SELECT company_id,
MAX(market_cap_cr) AS market_cap
FROM market_cap
GROUP BY company_id
ORDER BY market_cap DESC
LIMIT 10;
