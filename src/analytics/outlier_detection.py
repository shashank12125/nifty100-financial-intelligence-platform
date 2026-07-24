import sqlite3
import pandas as pd
from scipy.stats import zscore

DB_PATH = "output/nifty100.db"

conn = sqlite3.connect(DB_PATH)

ratios = pd.read_sql("""
SELECT *
FROM financial_ratios
""", conn)

sectors = pd.read_sql("""
SELECT
company_id,
broad_sector
FROM sectors
""", conn)

conn.close()

# Latest year only
ratios = (
    ratios.sort_values("year", ascending=False)
          .drop_duplicates("company_id")
)

df = ratios.merge(sectors, on="company_id", how="left")

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

# Calculate Z-score within each broad sector
for col in kpis:
    df[f"{col}_z"] = (
        df.groupby("broad_sector")[col]
          .transform(lambda x: zscore(x, nan_policy="omit"))
    )

z_cols = [f"{c}_z" for c in kpis]

outliers = df[
    df[z_cols].abs().max(axis=1) > 3
]

outliers.to_csv("output/outlier_report.csv", index=False)

print(f"Outliers Found: {len(outliers)}")
print("Saved: output/outlier_report.csv")