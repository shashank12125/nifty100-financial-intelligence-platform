import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

DB_PATH = "output/nifty100.db"

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql("""
SELECT *
FROM financial_ratios
""", conn)

conn.close()

# Latest year per company
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

corr = df[kpis].corr(method="pearson")

plt.figure(figsize=(12,8))

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5
)

plt.title("Correlation Matrix (Latest Financial KPIs)")
plt.tight_layout()

plt.savefig("reports/correlation_heatmap.png", dpi=300)

print("Correlation heatmap generated successfully.")