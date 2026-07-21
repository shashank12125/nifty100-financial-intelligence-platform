"""
Sprint 5 - Day 30
Auto Pros / Cons Generator
"""

from pathlib import Path
import pandas as pd


# Paths

ROOT = Path(__file__).resolve().parents[2]

RAW = ROOT / "data" / "raw"
SUPPORTING = ROOT / "data" / "supporting"
OUTPUT = ROOT / "output"

OUTPUT.mkdir(exist_ok=True)

# Load Data

ratios = pd.read_excel(
    SUPPORTING / "financial_ratios.xlsx",
    header=1
)

profit = pd.read_excel(
    RAW / "profitandloss.xlsx",
    header=1
)

analysis = pd.read_csv(
    OUTPUT / "analysis_parsed.csv"
)

# Clean

ratios = pd.read_excel(
    SUPPORTING / "financial_ratios.xlsx"
)


ratios = ratios.sort_values(
    ["company_id", "year"]
)

profit = profit.sort_values(
    ["company_id", "year"]
)

# Helper

rows = []


def add_rule(
        company,
        rule_type,
        rule_id,
        text,
        confidence
):

    if confidence < 60:
        return

    rows.append({

        "company_id": company,

        "type": rule_type,

        "rule_id": rule_id,

        "text": text,

        "confidence_pct": confidence

    })

# Company Loop

companies = sorted(
    ratios.company_id.unique()
)

for company in companies:

    r = ratios[
        ratios.company_id == company
    ].copy()

    p = profit[
        profit.company_id == company
    ].copy()

    a = analysis[
        analysis.company_id == company
    ].copy()

    if len(r) == 0:
        continue

    latest = r.iloc[-1]

    latest_profit = p.iloc[-1] if len(p) else None

    # PRO 1
    # ROE >20

    if latest.return_on_equity_pct > 20:

        add_rule(

            company,

            "pro",

            "P1",

            "Consistently high return on equity above 20% demonstrates exceptional capital efficiency.",

            95

        )

    # PRO 2
    # Debt Free

    if latest.debt_to_equity == 0:

        add_rule(

            company,

            "pro",

            "P2",

            "Debt-free balance sheet provides financial flexibility and eliminates interest burden.",

            92

        )

    # PRO 3
    # OPM


    if latest.operating_profit_margin_pct > 25:

        add_rule(

            company,

            "pro",

            "P3",

            "Operating profit margin above 25% indicates strong pricing power and cost discipline.",

            90

        )

    # PRO 4
    # Interest Coverage

    if latest.interest_coverage > 10:

        add_rule(

            company,

            "pro",

            "P4",

            "Very high interest coverage ratio reflects negligible financial stress from debt servicing.",

            88

        )

    # PRO 5
    # Positive FCF

    if latest.free_cash_flow_cr > 0:

        add_rule(

            company,

            "pro",

            "P5",

            "Positive free cash flow indicates healthy cash generation.",

            84

        )
    # PRO 6
    # Revenue CAGR

    rev = a[

        (a.metric_type == "compounded_sales_growth")

        &

        (a.period_years == 5)

    ]

    if len(rev):

        value = rev.iloc[0].value_pct

        if value > 15:

            add_rule(

                company,

                "pro",

                "P6",

                "Revenue growing above 15% CAGR over five years reflects strong business momentum.",

                91

            )

        # PRO 7
        # Dividend + Positive FCF

        if (
                latest.dividend_payout_ratio_pct > 0
                and latest.free_cash_flow_cr > 0
        ):
            add_rule(
                company,
                "pro",
                "P7",
                "Dividend payouts are supported by positive free cash flow.",
                82
            )

        # PRO 8
        # ROE improving

        if len(r) >= 3:

            roe = r["return_on_equity_pct"].tail(3).tolist()

            if roe[0] < roe[1] < roe[2]:
                add_rule(
                    company,
                    "pro",
                    "P8",
                    "Return on equity has improved consistently over the last three years.",
                    88
                )

        # PRO 9
        # EPS improving

        if len(p) >= 3:

            eps = p["eps"].tail(3).tolist()

            if eps[0] < eps[1] < eps[2]:
                add_rule(
                    company,
                    "pro",
                    "P9",
                    "Earnings per share have grown consistently over the last three years.",
                    86
                )

        # CON 1
        # High Debt

        if latest.debt_to_equity > 2:
            add_rule(
                company,
                "con",
                "C1",
                f"Debt to equity ratio of {latest.debt_to_equity:.2f} is elevated.",
                95
            )

        # CON 2
        # Negative FCF

        if latest.free_cash_flow_cr < 0:
            add_rule(
                company,
                "con",
                "C2",
                "Negative free cash flow raises concern over cash generation.",
                85
            )

        # CON 3
        # Low Interest Coverage

        if latest.interest_coverage < 1.5:
            add_rule(
                company,
                "con",
                "C3",
                "Interest coverage below 1.5x indicates financial stress.",
                92
            )

        # CON 4
        # Net Loss

        if latest_profit is not None:

            if latest_profit.net_profit < 0:
                add_rule(
                    company,
                    "con",
                    "C4",
                    "Company reported a net loss in the latest financial year.",
                    96
                )

        # CON 5
        # Revenue CAGR

        if len(rev):

            if value < 5:
                add_rule(
                    company,
                    "con",
                    "C5",
                    "Revenue CAGR below 5% reflects weak long-term growth.",
                    84
                )

        # CON 6
        # Dividend payout

        if latest.dividend_payout_ratio_pct > 100:
            add_rule(
                company,
                "con",
                "C6",
                "Dividend payout above 100% may not be sustainable.",
                90
            )

        # CON 7
        # OPM decline

        if len(p) >= 3:

            opm = p["opm_percentage"].tail(3).tolist()

            if opm[0] > opm[1] > opm[2]:
                add_rule(
                    company,
                    "con",
                    "C7",
                    "Operating profit margin has declined for three consecutive years.",
                    88
                )

        # CON 8
        # EPS decline

        if len(p) >= 3:

            eps = p["eps"].tail(3).tolist()

            if eps[0] > eps[1] > eps[2]:
                add_rule(
                    company,
                    "con",
                    "C8",
                    "Earnings per share have declined consistently.",
                    86
                )

        # Fallback

        company_rows = [x for x in rows if x["company_id"] == company]

        pros = [x for x in company_rows if x["type"] == "pro"]
        cons = [x for x in company_rows if x["type"] == "con"]

        if len(pros) == 0:
            add_rule(
                company,
                "pro",
                "PF",
                "Business has stable operating performance.",
                65
            )

        if len(cons) == 0:
            add_rule(
                company,
                "con",
                "CF",
                "Business should continue monitoring financial performance.",
                65
            )



    # Save

output = pd.DataFrame(rows)

# ----------------------------------------------------
# Ensure every company has at least one Pro and one Con
# ----------------------------------------------------

companies = pd.read_excel(
    RAW / "companies.xlsx",
    header=1
)

all_ids = set(companies["id"].astype(str))

for cid in all_ids:

    temp = output[output["company_id"] == cid]

    if temp.empty:

        output = pd.concat([
            output,
            pd.DataFrame([
                {
                    "company_id": cid,
                    "type": "pro",
                    "rule_id": "PF",
                    "text": "Business has stable operating performance.",
                    "confidence_pct": 65
                },
                {
                    "company_id": cid,
                    "type": "con",
                    "rule_id": "CF",
                    "text": "Business should continue monitoring financial performance.",
                    "confidence_pct": 65
                }
            ])
        ], ignore_index=True)

    else:

        if not (temp["type"] == "pro").any():
            output = pd.concat([
                output,
                pd.DataFrame([{
                    "company_id": cid,
                    "type": "pro",
                    "rule_id": "PF",
                    "text": "Business has stable operating performance.",
                    "confidence_pct": 65
                }])
            ], ignore_index=True)

        if not (temp["type"] == "con").any():
            output = pd.concat([
                output,
                pd.DataFrame([{
                    "company_id": cid,
                    "type": "con",
                    "rule_id": "CF",
                    "text": "Business should continue monitoring financial performance.",
                    "confidence_pct": 65
                }])
            ], ignore_index=True)


output = output.sort_values(
    ["company_id", "type"]
)

companies = pd.read_excel(
    RAW / "companies.xlsx",
    header=1
)

master = pd.read_excel(RAW / "companies.xlsx", header=1)

master_ids = set(master["id"].astype(str).str.strip())

output["company_id"] = output["company_id"].astype(str).str.strip()

output = output[output["company_id"].isin(master_ids)]

output.to_csv(
    OUTPUT / "pros_cons_generated.csv",
    index=False
)

print("=" * 50)
print("Pros & Cons Generator Completed")
print("=" * 50)
print("Companies :", output.company_id.nunique())
print("Rows :", len(output))
print("Output :", OUTPUT / "pros_cons_generated.csv")