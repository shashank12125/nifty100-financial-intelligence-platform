import pandas as pd

from src.dashboard.utils.db import get_screener_data
from src.api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_dashboard_matches_api():

    dashboard_df = get_screener_data()

    response = client.get("/api/v1/screener")

    assert response.status_code == 200

    api_df = pd.DataFrame(response.json())

    assert len(dashboard_df) > 0
    assert len(api_df) > 0

from src.dashboard.utils.db import get_screener_data


def test_dashboard_data():

    df = get_screener_data()

    assert not df.empty

    required_columns = [
        "company_id",
        "year",
        "return_on_equity_pct",
        "debt_to_equity",
        "interest_coverage",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "asset_turnover",
        "free_cash_flow_cr",
        "capex_cr",
        "earnings_per_share",
        "book_value_per_share",
        "dividend_payout_ratio_pct",
        "total_debt_cr",
        "cash_from_operations_cr",
    ]

    for column in required_columns:
        assert column in df.columns