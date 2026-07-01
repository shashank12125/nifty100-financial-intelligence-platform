import pandas as pd
import sqlite3

from ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    debt_to_equity,
    interest_coverage_ratio,
    asset_turnover
)

from cashflow_kpis import (
    free_cash_flow,
    capex_intensity
)

from cagr import revenue_cagr


DB_PATH = "output/nifty100.db"

print("Loading datasets...")

# ----------------------------
# Read Excel Files
# ----------------------------

pnl = pd.read_excel(
    "data/raw/profitandloss.xlsx",
    header=1
)

bs = pd.read_excel(
    "data/raw/balancesheet.xlsx",
    header=1
)

cf = pd.read_excel(
    "data/raw/cashflow.xlsx",
    header=1
)

companies = pd.read_excel(
    "data/raw/companies.xlsx",
    header=1
)

print("Datasets Loaded")

# ----------------------------
# Normalize IDs
# ----------------------------

for df in [pnl, bs, cf]:

    df["company_id"] = (
        df["company_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

companies["id"] = (
    companies["id"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# ----------------------------
# Merge P&L + Balance Sheet
# ----------------------------

ratio_df = pnl.merge(

    bs,

    on=[
        "company_id",
        "year"
    ],

    how="inner",

    suffixes=(
        "",
        "_bs"
    )

)

# ----------------------------
# Merge Cash Flow
# ----------------------------

ratio_df = ratio_df.merge(

    cf,

    on=[
        "company_id",
        "year"
    ],

    how="left",

    suffixes=(
        "",
        "_cf"
    )

)

# ----------------------------
# Merge Company Master
# ----------------------------

ratio_df = ratio_df.merge(

    companies,

    left_on="company_id",

    right_on="id",

    how="left"

)

print("\nMerged Dataset")

print(ratio_df.head())

print()

print("Rows :", len(ratio_df))

print("Columns :", len(ratio_df.columns))

print("\nCalculating KPIs...")

ratio_df["net_profit_margin_pct"] = ratio_df.apply(
    lambda r: net_profit_margin(
        r["net_profit"],
        r["sales"]
    ),
    axis=1
)

ratio_df["operating_profit_margin_pct"] = ratio_df.apply(
    lambda r: operating_profit_margin(
        r["operating_profit"],
        r["sales"]
    ),
    axis=1
)

ratio_df["return_on_equity_pct"] = ratio_df.apply(
    lambda r: return_on_equity(
        r["net_profit"],
        r["equity_capital"],
        r["reserves"]
    ),
    axis=1
)

ratio_df["debt_to_equity"] = ratio_df.apply(
    lambda r: debt_to_equity(
        r["borrowings"],
        r["equity_capital"],
        r["reserves"]
    ),
    axis=1
)

ratio_df["interest_coverage"] = ratio_df.apply(
    lambda r: interest_coverage_ratio(
        r["operating_profit"],
        r["other_income"],
        r["interest"]
    ),
    axis=1
)

ratio_df["asset_turnover"] = ratio_df.apply(
    lambda r: asset_turnover(
        r["sales"],
        r["total_assets"]
    ),
    axis=1
)

ratio_df["free_cash_flow_cr"] = ratio_df.apply(
    lambda r: free_cash_flow(
        r["operating_activity"],
        r["investing_activity"]
    ),
    axis=1
)

ratio_df["capex_cr"] = ratio_df.apply(
    lambda r: capex_intensity(
        r["investing_activity"],
        r["sales"]
    ),
    axis=1
)

ratio_df["earnings_per_share"] = ratio_df["eps"]

ratio_df["book_value_per_share"] = (
    ratio_df["book_value"]
)

ratio_df["dividend_payout_ratio_pct"] = (
    ratio_df["dividend_payout"]
)

ratio_df["total_debt_cr"] = (
    ratio_df["borrowings"]
)

ratio_df["cash_from_operations_cr"] = (
    ratio_df["operating_activity"]
)

# Placeholder until full CAGR engine integration
ratio_df["revenue_cagr_5yr"] = None
ratio_df["pat_cagr_5yr"] = None
ratio_df["eps_cagr_5yr"] = None

ratio_df["composite_quality_score"] = None

print("\nKPIs Calculated Successfully")

print(
    ratio_df[
        [
            "company_id",
            "year",
            "net_profit_margin_pct",
            "return_on_equity_pct",
            "debt_to_equity"
        ]
    ].head()
)

# ----------------------------
# Save to SQLite
# ----------------------------

print("\nConnecting to SQLite...")

conn = sqlite3.connect(DB_PATH)

# Required columns for financial_ratios table
final_df = ratio_df[
    [
        "company_id",
        "year",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "return_on_equity_pct",
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",
        "free_cash_flow_cr",
        "capex_cr",
        "earnings_per_share",
        "book_value_per_share",
        "dividend_payout_ratio_pct",
        "total_debt_cr",
        "cash_from_operations_cr",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr",
        "composite_quality_score"
    ]
].copy()

# Remove old data
conn.execute("DELETE FROM financial_ratios")

# Load new data
final_df.to_sql(
    "financial_ratios",
    conn,
    if_exists="append",
    index=False
)

# Verify row count
cursor = conn.cursor()

cursor.execute(
    "SELECT COUNT(*) FROM financial_ratios"
)

count = cursor.fetchone()[0]

print(f"\nRows inserted: {count}")

conn.commit()
conn.close()

print("\nFinancial Ratio Engine Complete.")