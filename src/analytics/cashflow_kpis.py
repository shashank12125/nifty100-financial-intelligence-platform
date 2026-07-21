"""
Sprint 2 - Day 11
Cash Flow KPI Engine
"""

from typing import Optional
import pandas as pd
from pathlib import Path

def free_cash_flow(
    operating_activity: float,
    investing_activity: float
) -> float:
    """
    Free Cash Flow = CFO + CFI
    """
    return round(
        operating_activity + investing_activity,
        2
    )


def cfo_quality_score(
    cfo: float,
    pat: float
):
    """
    CFO / PAT
    """

    if pat == 0:
        return None

    ratio = cfo / pat

    if ratio > 1:
        return "High Quality"

    if ratio >= 0.5:
        return "Moderate"

    return "Accrual Risk"


def capex_intensity(
    investing_activity: float,
    sales: float
):
    """
    CapEx %
    """

    if sales == 0:
        return None

    value = abs(investing_activity) / sales * 100

    if value < 3:
        return "Asset Light"

    if value <= 8:
        return "Moderate"

    return "Capital Intensive"


def fcf_conversion_rate(
    fcf: float,
    operating_profit: float
):
    """
    FCF / Operating Profit
    """

    if operating_profit == 0:
        return None

    return round(
        (fcf / operating_profit) * 100,
        2
    )


def capital_allocation_pattern(
    cfo,
    cfi,
    cff,
    quality="Moderate"
):

    s1 = "+" if cfo >= 0 else "-"
    s2 = "+" if cfi >= 0 else "-"
    s3 = "+" if cff >= 0 else "-"

    pattern = f"{s1}{s2}{s3}"

    mapping = {

        "+--": (
            "Shareholder Returns"
            if quality == "High Quality"
            else "Reinvestor"
        ),

        "++-": "Liquidating Assets",

        "-++": "Distress Signal",

        "--+": "Growth Funded by Debt",

        "+++": "Cash Accumulator",

        "---": "Pre-Revenue",

        "+-+": "Mixed"

    }

    return mapping.get(
        pattern,
        "Unknown"
    )

def cfo_quality_score(cfo: float, pat: float):
    if pat == 0:
        return None, None

    ratio = round(cfo / pat, 2)

    if ratio > 1:
        label = "High Quality"
    elif ratio >= 0.5:
        label = "Moderate"
    else:
        label = "Accrual Risk"

    return ratio, label

def capex_intensity(investing_activity: float, sales: float):
    if sales == 0:
        return None, None

    value = round(abs(investing_activity) / sales * 100, 2)

    if value < 3:
        label = "Asset Light"
    elif value <= 8:
        label = "Moderate"
    else:
        label = "Capital Intensive"

    return value, label

def deleveraging_flag(cff, current_borrowings, previous_borrowings):
    return (
        cff < 0
        and current_borrowings < previous_borrowings
    )

ROOT = Path(__file__).resolve().parents[2]

RAW = ROOT / "data" / "raw"
OUTPUT = ROOT / "output"

if __name__ == "__main__":

    cash = pd.read_excel(RAW / "cashflow.xlsx", header=1)
    pnl = pd.read_excel(RAW / "profitandloss.xlsx", header=1)
    bs = pd.read_excel(RAW / "balancesheet.xlsx", header=1)
    companies = pd.read_excel(RAW / "companies.xlsx", header=1)

    df = (
        cash.merge(
            pnl[["company_id", "year", "sales", "net_profit", "operating_profit"]],
            on=["company_id", "year"],
            how="left",
        )
        .merge(
            bs[["company_id", "year", "borrowings"]],
            on=["company_id", "year"],
            how="left",
        )
        .merge(
            companies[["id", "company_name"]],
            left_on="company_id",
            right_on="id",
            how="left",
        )
    )

    df["fcf"] = (
        df["operating_activity"]
        + df["investing_activity"]
    )

    rows = []

    distress_rows = []

    for company, g in df.groupby("company_id"):

        g = g.sort_values("year")

        latest = g.iloc[-1]

        last5 = g.tail(5)

        ratio = (
            last5["operating_activity"]
            / last5["net_profit"]
        ).replace([float("inf"), -float("inf")], pd.NA)

        avg_ratio = ratio.mean()

        if pd.isna(avg_ratio):
            quality = None
        elif avg_ratio > 1:
            quality = "High Quality"
        elif avg_ratio >= 0.5:
            quality = "Moderate"
        else:
            quality = "Accrual Risk"

        capex_pct = abs(
            latest["investing_activity"]
        ) / latest["sales"] * 100 if latest["sales"] else None

        if capex_pct is None:
            capex_label = None
        elif capex_pct < 3:
            capex_label = "Asset Light"
        elif capex_pct <= 8:
            capex_label = "Moderate"
        else:
            capex_label = "Capital Intensive"

        distress = (
            latest["operating_activity"] < 0
            and latest["financing_activity"] > 0
        )

        deleveraging = False

        if len(g) >= 2:

            prev = g.iloc[-2]

            deleveraging = (
                latest["financing_activity"] < 0
                and latest["borrowings"] < prev["borrowings"]
            )

        fcf_conversion = None

        if latest["operating_profit"] != 0:

            fcf_conversion = round(
                latest["fcf"]
                / latest["operating_profit"]
                * 100,
                2,
            )

        allocation = capital_allocation_pattern(
            latest["operating_activity"],
            latest["investing_activity"],
            latest["financing_activity"],
            quality or "Moderate",
        )

        rows.append(
            {
                "company_id": company,
                "sector": "",
                "cfo_quality_score": round(avg_ratio, 2)
                if pd.notna(avg_ratio)
                else None,
                "cfo_quality_label": quality,
                "capex_intensity_pct": round(capex_pct, 2)
                if capex_pct
                else None,
                "capex_label": capex_label,
                "fcf_cagr_5yr": None,
                "fcf_conversion_pct": fcf_conversion,
                "distress_flag": distress,
                "deleveraging_flag": deleveraging,
                "capital_allocation_label": allocation,
            }
        )

        if distress:

            distress_rows.append(
                {
                    "company_id": company,
                    "CFO": latest["operating_activity"],
                    "CFF": latest["financing_activity"],
                    "latest_net_profit": latest["net_profit"],
                }
            )

    pd.DataFrame(rows).to_excel(
        OUTPUT / "cashflow_intelligence.xlsx",
        index=False,
    )

    pd.DataFrame(distress_rows).to_csv(
        OUTPUT / "distress_alerts.csv",
        index=False,
    )

    print("=" * 50)
    print("Cashflow Intelligence Completed")
    print("=" * 50)
    print("Companies :", len(rows))
    print("Distress Alerts :", len(distress_rows))