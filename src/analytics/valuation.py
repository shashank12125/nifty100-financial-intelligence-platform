from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

SUPPORTING = ROOT / "data" / "supporting"

OUTPUT = ROOT / "output"

OUTPUT.mkdir(exist_ok=True)

market = pd.read_excel(SUPPORTING / "market_cap.xlsx")

ratios = pd.read_excel(SUPPORTING / "financial_ratios.xlsx")

sectors = pd.read_excel(SUPPORTING / "sectors.xlsx")

market = (
    market
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
)

ratios = (
    ratios
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
)

df = market.merge(
    ratios[
        [
            "company_id",
            "free_cash_flow_cr"
        ]
    ],
    on="company_id",
    how="left"
)

df = df.merge(
    sectors[
        [
            "company_id",
            "broad_sector"
        ]
    ],
    on="company_id",
    how="left"
)

df["fcf_yield_pct"] = (
    df["free_cash_flow_cr"]
    /
    df["market_cap_crore"]
) * 100

sector_pe = (
    df.groupby("broad_sector")["pe_ratio"]
      .median()
      .reset_index()
      .rename(
          columns={
              "pe_ratio": "sector_median_pe"
          }
      )
)

df = df.merge(
    sector_pe,
    on="broad_sector",
    how="left"
)

df["pe_vs_sector_median_pct"] = (
    (
        df["pe_ratio"]
        -
        df["sector_median_pe"]
    )
    /
    df["sector_median_pe"]
) * 100

def valuation_flag(row):

    if row["pe_ratio"] > row["sector_median_pe"] * 1.5:
        return "Caution"

    elif row["pe_ratio"] < row["sector_median_pe"] * 0.7:
        return "Discount"

    else:
        return "Fair"


df["flag"] = df.apply(
    valuation_flag,
    axis=1
)

summary = df[
    [
        "company_id",
        "broad_sector",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "market_cap_crore",
        "free_cash_flow_cr",
        "fcf_yield_pct",
        "sector_median_pe",
        "pe_vs_sector_median_pct",
        "flag"
    ]
]

summary.to_excel(
    OUTPUT / "valuation_summary.xlsx",
    index=False
)

summary[
    summary["flag"] != "Fair"
].to_csv(
    OUTPUT / "valuation_flags.csv",
    index=False
)

print("valuation_summary.xlsx created")
print("valuation_flags.csv created")

