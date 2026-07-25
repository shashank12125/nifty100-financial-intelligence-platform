"""
Financial Ratio Engine
Sprint 2 - Day 8
"""



def net_profit_margin(net_profit: float, sales: float) -> float | None:
    """Calculate net profit margin."""

    if sales == 0:
        return None

    return round((net_profit / sales) * 100, 2)


def operating_profit_margin(operating_profit: float, sales: float) -> float | None:
    """Calculate operating profit margin."""

    if sales == 0:
        return None

    return round((operating_profit / sales) * 100, 2)


def check_opm(calculated_opm: float, source_opm: float) -> bool:
    """
    Validate operating profit margin.
    Returns True if difference >1%
    """

    return abs(calculated_opm - source_opm) > 1


def return_on_equity(
    net_profit: float,
    equity_capital: float,
    reserves: float
) -> float | None:
    """Calculate return on equity."""
    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round((net_profit / equity) * 100, 2)


def return_on_capital_employed(
    ebit: float,
    equity_capital: float,
    reserves: float,
    borrowings: float
) -> float | None:
    """Calculate return on capital employed."""
    capital = equity_capital + reserves + borrowings

    if capital <= 0:
        return None

    return round((ebit / capital) * 100, 2)


def return_on_assets(
    net_profit: float,
    total_assets: float
) -> float | None:
    """Calculate return on assets."""
    if total_assets == 0:
        return None

    return round((net_profit / total_assets) * 100, 2)

# ==========================
# Day 09 - Leverage & Efficiency Ratios
# ==========================

def debt_to_equity(
    borrowings: float,
    equity_capital: float,
    reserves: float
):
    """Calculate debt-to-equity ratio."""

    if borrowings == 0:
        return 0

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round(borrowings / equity, 2)


def high_leverage_flag(
    debt_equity: float,
    is_financial_sector: bool
):
    """Determine high leverage status."""

    if is_financial_sector:
        return False

    return debt_equity is not None and debt_equity > 5


def interest_coverage_ratio(
    operating_profit: float,
    other_income: float,
    interest: float
):
    """Calculate interest coverage ratio."""

    if interest == 0:
        return None

    return round(
        (operating_profit + other_income) / interest,
        2
    )


def icr_label(interest: float):
    """
    Label for debt-free companies
    """

    if interest == 0:
        return "Debt Free"

    return ""


def icr_warning(icr):
    """
    Warning if company cannot cover interest
    """

    if icr is None:
        return False

    return icr < 1.5


def net_debt(
    borrowings: float,
    investments: float
):
    """
    Net Debt
    """

    return round(
        borrowings - investments,
        2
    )


def asset_turnover(
    sales: float,
    total_assets: float
):
    """
    Asset Turnover
    """

    if total_assets == 0:
        return None

    return round(
        sales / total_assets,
        2
    )