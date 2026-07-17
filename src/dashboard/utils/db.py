import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "output/nifty100.db"


@st.cache_data(ttl=600)
def get_companies():
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

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM sectors",
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_peers(group_name):

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
            revenue_cagr_5yr,
            pat_cagr_5yr,
            eps_cagr_5yr,
            dividend_payout_ratio_pct,
            composite_quality_score
        FROM financial_ratios
        """,
        conn,
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_peer_groups():

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

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM analysis",
        conn
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_profit_loss(company_id):

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