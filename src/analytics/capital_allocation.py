import pandas as pd
from pathlib import Path

from cashflow_kpis import (
    cfo_quality_score,
    capital_allocation_pattern
)

RAW_PATH = Path("data/raw")
OUTPUT_PATH = Path("output")

OUTPUT_PATH.mkdir(exist_ok=True)

# Load Cash Flow data
cashflow = pd.read_excel(
    RAW_PATH / "cashflow.xlsx",
    header=1
)

records = []

for _, row in cashflow.iterrows():

    cfo = row["operating_activity"]
    cfi = row["investing_activity"]
    cff = row["financing_activity"]

    # PAT available nahi hai cashflow sheet me,
    # isliye placeholder quality use kar rahe hain.
    quality = "Moderate"

    pattern = capital_allocation_pattern(
        cfo,
        cfi,
        cff,
        quality
    )

    records.append({

        "company_id": row["company_id"],
        "year": row["year"],

        "cfo_sign":
            "+" if cfo >= 0 else "-",

        "cfi_sign":
            "+" if cfi >= 0 else "-",

        "cff_sign":
            "+" if cff >= 0 else "-",

        "pattern_label": pattern

    })

output = pd.DataFrame(records)

output.to_csv(
    OUTPUT_PATH / "capital_allocation.csv",
    index=False
)

print(output.head())

print(
    f"\nCapital Allocation Report Generated: {len(output)} rows"
)