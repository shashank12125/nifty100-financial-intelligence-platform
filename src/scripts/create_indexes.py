import sqlite3

conn = sqlite3.connect("output/nifty100.db")
cur = conn.cursor()

indexes = [
    ("idx_financial_company", "financial_ratios", "company_id"),
    ("idx_financial_year", "financial_ratios", "year"),
    ("idx_pl_company", "profitandloss", "company_id"),
    ("idx_bs_company", "balancesheet", "company_id"),
    ("idx_cf_company", "cashflow", "company_id"),
]

for name, table, column in indexes:
    cur.execute(
        f"CREATE INDEX IF NOT EXISTS {name} ON {table}({column})"
    )

conn.commit()
conn.close()

print("All indexes created successfully.")