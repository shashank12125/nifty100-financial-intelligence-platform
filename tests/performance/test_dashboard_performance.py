import time

from src.dashboard.utils.db import get_company_profile

TICKERS = [
    "TCS",
    "INFY",
    "RELIANCE",
    "HDFCBANK",
    "ICICIBANK",
]


def test_company_profile_load_time():
    for ticker in TICKERS:
        start = time.perf_counter()

        df = get_company_profile(ticker)

        elapsed = time.perf_counter() - start

        print(f"{ticker}: {elapsed:.3f} sec")

        assert not df.empty
        assert elapsed < 3