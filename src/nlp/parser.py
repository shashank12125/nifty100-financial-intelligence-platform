"""
Sprint 5 - Day 29
Analysis Text Parser
"""

import re
from pathlib import Path

import pandas as pd

# Paths

ROOT = Path(__file__).resolve().parents[2]

RAW = ROOT / "data" / "raw"

OUTPUT = ROOT / "output"

OUTPUT.mkdir(exist_ok=True)

# Load Analysis File

analysis = pd.read_excel(
    RAW / "analysis.xlsx",
    header=1
)

# remove empty rows
analysis = analysis.dropna(how="all")

# Regex Pattern

pattern = re.compile(r"(\d+)\s*Years?:?\s*([-\d.]+)%")

metrics = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe"
]

parsed_rows = []

failed_rows = []

# Parse

for _, row in analysis.iterrows():

    company = row["company_id"]

    for metric in metrics:

        value = row[metric]

        if pd.isna(value):
            continue

        value = str(value)

        match = pattern.search(value)

        if match:

            parsed_rows.append({

                "company_id": company,

                "metric_type": metric,

                "period_years": int(match.group(1)),

                "value_pct": float(match.group(2))

            })

        else:

            failed_rows.append({

                "company_id": company,

                "metric_type": metric,

                "original_text": value

            })

# Save

parsed_df = pd.DataFrame(parsed_rows)

failed_df = pd.DataFrame(failed_rows)

parsed_df.to_csv(
    OUTPUT / "analysis_parsed.csv",
    index=False
)

failed_df.to_csv(
    OUTPUT / "parse_failures.csv",
    index=False
)

# Summary

print("=" * 50)

print("Analysis Parser Completed")

print("=" * 50)

print(f"Parsed Records : {len(parsed_df)}")

print(f"Failed Records : {len(failed_df)}")

print()

print("Generated Files")

print("- analysis_parsed.csv")

print("- parse_failures.csv")