"""
Sprint 2 - Day 11
Cash Flow KPI Engine
"""

from typing import Optional


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