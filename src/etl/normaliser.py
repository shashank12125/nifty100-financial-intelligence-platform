import re


def normalize_ticker(ticker):
    """
    Normalize company ticker/symbol.
    Example:
    ' abb ' -> 'ABB'
    'adanient' -> 'ADANIENT'
    """
    if ticker is None:
        return None

    return str(ticker).strip().upper()


def normalize_year(year):
    """
    Convert different year formats into YYYY-MM format.

    Examples:
    Mar 2014 -> 2014-03
    Dec 2012 -> 2012-12
    Mar-24   -> 2024-03
    FY24     -> 2024-03
    2023     -> 2023-03
    """

    if year is None:
        return None

    year = str(year).strip()

    # Mar 2014
    match = re.match(r"^(Mar|Dec)\s+(\d{4})$", year, re.IGNORECASE)
    if match:
        month = match.group(1).lower()
        yr = match.group(2)

        if month == "mar":
            return f"{yr}-03"
        elif month == "dec":
            return f"{yr}-12"

    # Mar-24
    match = re.match(r"^(Mar|Dec)-(\d{2})$", year, re.IGNORECASE)
    if match:
        month = match.group(1).lower()
        yr = int(match.group(2))

        yr = 2000 + yr

        if month == "mar":
            return f"{yr}-03"
        elif month == "dec":
            return f"{yr}-12"

    # FY24
    match = re.match(r"^FY(\d{2})$", year, re.IGNORECASE)
    if match:
        yr = 2000 + int(match.group(1))
        return f"{yr}-03"

    # 2023
    match = re.match(r"^\d{4}$", year)
    if match:
        return f"{year}-03"

    return year