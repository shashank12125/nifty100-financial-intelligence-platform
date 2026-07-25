import pandas as pd

from src.etl.validator import *


def test_dq01():
    df = pd.DataFrame({"id": ["A", "A"]})
    r = dq01_pk_uniqueness(df, "companies", "id")
    assert r.iloc[0]["dq_rule"] == "DQ-01"


def test_dq02():
    df = pd.DataFrame({
        "company_id": ["A", "A"],
        "year": ["2024", "2024"]
    })
    r = dq02_company_year_uniqueness(df, "pnl")
    assert r.iloc[0]["dq_rule"] == "DQ-02"


def test_dq03():
    child = pd.DataFrame({"company_id": ["X"]})
    parent = pd.DataFrame({"id": ["A"]})
    r = dq03_fk_integrity(child, parent, "company_id", "id", "pnl")
    assert r.iloc[0]["dq_rule"] == "DQ-03"


def test_dq04():
    df = pd.DataFrame({
        "equity_capital":[100],
        "reserves":[100],
        "borrowings":[100],
        "other_liabilities":[100],
        "fixed_assets":[50],
        "cwip":[50],
        "investments":[50],
        "other_asset":[50],
        "total_liabilities":[500],
        "total_assets":[300],
    })
    r = dq04_balance_sheet_check(df)
    assert r.iloc[0]["dq_rule"] == "DQ-04"


def test_dq05():
    df = pd.DataFrame({
        "operating_profit":[100],
        "sales":[1000],
        "opm_percentage":[20]
    })
    r = dq05_opm_cross_check(df)
    assert r.iloc[0]["dq_rule"] == "DQ-05"


def test_dq06():
    df = pd.DataFrame({"sales":[-10]})
    r = dq06_positive_sales(df)
    assert r.iloc[0]["dq_rule"] == "DQ-06"