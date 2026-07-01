"""
Financial Ratio Engine
Sprint 2 - Day 8
"""

from typing import Optional


def net_profit_margin(net_profit: float, sales: float) -> Optional[float]:
    """Net Profit Margin = Net Profit / Sales × 100"""

    if sales == 0:
        return None

    return round((net_profit / sales) * 100, 2)


def operating_profit_margin(operating_profit: float, sales: float) -> Optional[float]:
    """Operating Profit Margin = Operating Profit / Sales × 100"""

    if sales == 0:
        return None

    return round((operating_profit / sales) * 100, 2)


def check_opm(calculated_opm: float, source_opm: float) -> bool:
    """
    Returns True if difference >1%
    """

    return abs(calculated_opm - source_opm) > 1


def return_on_equity(
    net_profit: float,
    equity_capital: float,
    reserves: float
) -> Optional[float]:

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round((net_profit / equity) * 100, 2)


def return_on_capital_employed(
    ebit: float,
    equity_capital: float,
    reserves: float,
    borrowings: float
) -> Optional[float]:

    capital = equity_capital + reserves + borrowings

    if capital <= 0:
        return None

    return round((ebit / capital) * 100, 2)


def return_on_assets(
    net_profit: float,
    total_assets: float
) -> Optional[float]:

    if total_assets == 0:
        return None

    return round((net_profit / total_assets) * 100, 2)