import sqlite3
import pandas as pd

DB_PATH = "output/nifty100.db"

conn = sqlite3.connect(DB_PATH)

clusters = pd.read_csv("output/cluster_labels.csv")

ratios = pd.read_sql("""
SELECT *
FROM financial_ratios
""", conn)

ratios = (
    ratios
    .sort_values("year", ascending=False)
    .drop_duplicates("company_id")
)

analysis = pd.read_sql("""
SELECT
company_id,
compounded_sales_growth,
compounded_profit_growth
FROM analysis
""", conn)

analysis = analysis[
    analysis["compounded_sales_growth"].str.contains("TTM", na=False)
].copy()

for col in [
    "compounded_sales_growth",
    "compounded_profit_growth"
]:
    analysis[col] = (
        analysis[col]
        .str.extract(r'(-?\d+)%')[0]
        .astype(float)
    )

df = (
    clusters
    .merge(ratios, on="company_id")
    .merge(analysis, on="company_id")
)

features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "operating_profit_margin_pct",
    "compounded_sales_growth",
    "compounded_profit_growth"
]

profile = (
    df
    .groupby("cluster_id")[features]
    .agg(["mean", "median"])
)

profile.to_csv("output/cluster_profile.csv")

print(profile)

conn.close()