"""
Sprint 2 - Day 10
CAGR Engine
"""



def calculate_cagr(
    start_value: float,
    end_value: float,
    years: int
) -> tuple[float | None, str | None]:
    """
    CAGR Formula

    Returns:
    (value, flag)
    """

    if years <= 0:
        return None, "INVALID_PERIOD"

    if start_value == 0:
        return None, "ZERO_BASE"

    if start_value > 0 and end_value > 0:

        cagr = (
            (end_value / start_value)
            ** (1 / years)
            - 1
        ) * 100

        return round(cagr, 2), None

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    return None, None


def revenue_cagr(start, end, years):
    return calculate_cagr(start, end, years)


def pat_cagr(start, end, years):
    return calculate_cagr(start, end, years)


def eps_cagr(start, end, years):
    return calculate_cagr(start, end, years)


def insufficient_data():
    return None, "INSUFFICIENT"