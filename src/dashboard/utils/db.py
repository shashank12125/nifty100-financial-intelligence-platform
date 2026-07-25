import sqlite3

import pandas as pd
import streamlit as st

DB_PATH = "output/nifty100.db"


@st.cache_data(ttl=600)
def get_companies():
    """Return all companies."""
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM companies",
        conn
    )

    conn.close()

    return df

    # function for singel company
@st.cache_data(ttl=600)
def get_ratios(ticker, year=None):
    """Return financial ratios for a company."""
    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT *
    FROM financial_ratios
    WHERE company_id = ?
    """

    params = [ticker]

    if year is not None:
        query += " AND year = ?"
        params.append(year)

    df = pd.read_sql(
        query,
        conn,
        params=params
    )

    conn.close()

    return df

    # function for entire companies
@st.cache_data(ttl=600)
def get_all_ratios(year=None):
    """Return financial ratios for all companies."""
    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT *
    FROM financial_ratios
    """

    params = []

    if year is not None:
        query += " WHERE year = ?"
        params.append(year)

    df = pd.read_sql(
        query,
        conn,
        params=params
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_pl(ticker):
    """Return profit and loss data."""
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM profitandloss WHERE company_id = ?",
        conn,
        params=[ticker]
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_bs(ticker):
    """Return balance sheet data."""
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM balancesheet WHERE company_id = ?",
        conn,
        params=[ticker]
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_cf(ticker):
    """Return cash flow data."""
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM cashflow WHERE company_id = ?",
        conn,
        params=[ticker]
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_sectors():
    """Return sector information."""
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM sectors",
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_peers(group_name):
    """Return peer group information."""
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM peer_groups WHERE peer_group_name = ?",
        conn,
        params=[group_name]
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_valuation(ticker):
    """Return valuation data."""
    conn = sqlite3.connect(DB_PATH)

    try:
        df = pd.read_sql(
            "SELECT * FROM valuation WHERE company_id = ?",
            conn,
            params=[ticker]
        )
    except Exception:
        df = pd.DataFrame()

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_dashboard_summary():
    """Return dashboard summary."""
    conn = sqlite3.connect(DB_PATH)

    summary = {}

    summary["total_companies"] = pd.read_sql(
        "SELECT COUNT(*) AS total FROM companies",
        conn
    ).iloc[0]["total"]

    summary["avg_roe"] = pd.read_sql(
        """
        SELECT ROUND(AVG(return_on_equity_pct),2) AS value
        FROM financial_ratios
        """,
        conn
    ).iloc[0]["value"]

    summary["median_de"] = pd.read_sql(
        """
        SELECT ROUND(AVG(debt_to_equity),2) AS value
        FROM financial_ratios
        """,
        conn
    ).iloc[0]["value"]

    summary["debt_free"] = pd.read_sql(
        """
        SELECT COUNT(DISTINCT company_id) AS total
        FROM financial_ratios
        WHERE debt_to_equity = 0
        """,
        conn
    ).iloc[0]["total"]

    conn.close()

    return summary

@st.cache_data(ttl=600)
def get_sector_breakdown():
    """Return sector-wise breakdown."""
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql("""
        SELECT
            broad_sector,
            COUNT(*) AS company_count
        FROM sectors
        GROUP BY broad_sector
        ORDER BY company_count DESC
    """, conn)

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_top_companies():
    """Return top performing companies."""
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql("""
        SELECT
            company_id,
            year,
            return_on_equity_pct,
            debt_to_equity
        FROM financial_ratios
        ORDER BY return_on_equity_pct DESC
        LIMIT 5
    """, conn)

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_company_profile(ticker):
    """Return company profile."""
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT *
        FROM companies
        WHERE id = ?
        """,
        conn,
        params=[ticker]
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_revenue_profit(ticker):
    """Return revenue and profit trend."""
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT
            year,
            sales,
            net_profit
        FROM profitandloss
        WHERE company_id = ?
        ORDER BY year
        """,
        conn,
        params=[ticker]
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_roe_roce_trend(ticker):
    """Return ROE and ROCE trend."""
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT
            year,
            return_on_equity_pct,
            operating_profit_margin_pct
        FROM financial_ratios
        WHERE company_id = ?
        ORDER BY year
        """,
        conn,
        params=[ticker]
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_screener_data():
    """Return screener data."""
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            return_on_equity_pct,
            debt_to_equity,
            interest_coverage,
            net_profit_margin_pct,
            operating_profit_margin_pct,
            asset_turnover,
            free_cash_flow_cr,
            capex_cr,
            earnings_per_share,
            book_value_per_share,
            dividend_payout_ratio_pct,
            total_debt_cr,
            cash_from_operations_cr
        FROM financial_ratios
        """,
        conn,
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_peer_groups():
    """Return peer groups."""
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT DISTINCT peer_group_name
        FROM peer_groups
        ORDER BY peer_group_name
        """,
        conn
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_company_metrics(company_id):
    """Return company metrics."""
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            return_on_equity_pct,
            debt_to_equity,
            interest_coverage,
            net_profit_margin_pct,
            operating_profit_margin_pct,
            asset_turnover
        FROM financial_ratios
        WHERE company_id = ?
        ORDER BY year DESC
        LIMIT 1
        """,
        conn,
        params=[company_id]
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_benchmark_company(peer_group):
    """Return benchmark company."""
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT company_id
        FROM peer_groups
        WHERE peer_group_name = ?
        AND is_benchmark = 1
        LIMIT 1
        """,
        conn,
        params=[peer_group]
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_analysis():
    """Return analysis data."""
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM analysis",
        conn
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_profit_loss(company_id):
    """Return profit and loss statement."""
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT *
        FROM profitandloss
        WHERE company_id = ?
        ORDER BY year
        """,
        conn,
        params=(company_id,)
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_stock_prices():
    """Return stock price data."""
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT *
        FROM stock_prices
        """,
        conn
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_cashflow():
    """Return cash flow records."""
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT *
        FROM cashflow
        """,
        conn
    )

    conn.close()

    return df