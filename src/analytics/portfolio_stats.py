import sqlite3

import pandas as pd

DB_PATH = "output/nifty100.db"

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql("""
SELECT *
FROM financial_ratios
""", conn)

conn.close()

# Latest year only
df = (
    df.sort_values("year", ascending=False)
      .drop_duplicates("company_id")
)

kpis = [
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "return_on_equity_pct",
    "debt_to_equity",
    "interest_coverage",
    "asset_turnover",
    "free_cash_flow_cr",
    "earnings_per_share",
    "book_value_per_share",
    "cash_from_operations_cr"
]

stats = []

for col in kpis:

    stats.append({
        "KPI": col,
        "P10": df[col].quantile(0.10),
        "P25": df[col].quantile(0.25),
        "P50": df[col].quantile(0.50),
        "P75": df[col].quantile(0.75),
        "P90": df[col].quantile(0.90),
        "Mean": df[col].mean(),
        "Std": df[col].std()
    })

stats = pd.DataFrame(stats)

stats.to_csv("output/portfolio_stats.csv", index=False)

print(stats)

print("\nSaved: output/portfolio_stats.csv")