import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

OUTPUT = ROOT / "output"

capital = pd.read_csv(OUTPUT / "capital_allocation.csv")
cash = pd.read_excel(OUTPUT / "cashflow_intelligence.xlsx")

# ------------------------------------------------
# Verify company coverage
# ------------------------------------------------

print("=" * 50)
print("Verification")
print("=" * 50)

print("Companies :", capital["company_id"].nunique())
print("Rows :", len(capital))

# ------------------------------------------------
# Latest year distribution
# ------------------------------------------------

latest_year = capital["year"].iloc[-1]

latest = capital[
    capital["year"] == latest_year
]

distribution = (
    latest["pattern_label"]
    .value_counts()
    .reset_index()
)

distribution.columns = [
    "pattern_label",
    "company_count"
]

distribution.to_csv(
    OUTPUT / "capital_allocation_distribution.csv",
    index=False
)

# ------------------------------------------------
# Update cashflow intelligence
# ------------------------------------------------

cash = cash.drop(
    columns=["capital_allocation_label"],
    errors="ignore"
)

cash = cash.merge(

    latest[
        [
            "company_id",
            "pattern_label"
        ]
    ],

    on="company_id",

    how="left"

)

cash.rename(

    columns={

        "pattern_label":
        "capital_allocation_label"

    },

    inplace=True

)

cash.to_excel(

    OUTPUT /
    "cashflow_intelligence.xlsx",

    index=False

)

# ------------------------------------------------
# Pattern Changes
# ------------------------------------------------

capital = capital.sort_values(

    [
        "company_id",
        "year"
    ]

)

changes = []

for company, g in capital.groupby("company_id"):

    if len(g) < 2:
        continue

    prev = g.iloc[-2]
    curr = g.iloc[-1]

    if prev["pattern_label"] != curr["pattern_label"]:

        changes.append(

            {

                "company_id": company,

                "previous_pattern": prev["pattern_label"],

                "current_pattern": curr["pattern_label"]

            }

        )

pd.DataFrame(changes).to_csv(

    OUTPUT / "pattern_changes.csv",

    index=False

)

print("=" * 50)
print("Capital Allocation Report Completed")
print("=" * 50)
print("Latest Year :", latest_year)
print("Distribution :", len(distribution))
print("Pattern Changes :", len(changes))