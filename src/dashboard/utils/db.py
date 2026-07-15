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

st.subheader("Sector Breakdown")

sector_df = get_sector_breakdown()

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