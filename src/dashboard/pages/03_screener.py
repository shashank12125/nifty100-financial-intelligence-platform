import streamlit as st
import pandas as pd

from utils.db import get_screener_data

st.title("📈 Stock Screener")

# Load data
df = get_screener_data()

if df.empty:
    st.warning("No screener data available.")
    st.stop()

# Remove unrealistic values
df = df[
    (df["return_on_equity_pct"] >= 0)
    & (df["return_on_equity_pct"] <= 100)
    & (df["debt_to_equity"] <= 10)
    & (df["interest_coverage"] >= 0)
]

st.sidebar.subheader("Quick Screeners")

preset = st.sidebar.radio(
    "Choose a Preset",
    [
        "Custom",
        "Quality Compounder",
        "Value Pick",
        "Growth Accelerator",
        "Dividend Champion",
        "Debt-Free Blue Chip",
    ],
)
# st.write("Selected Preset:", preset)

st.sidebar.header("Filters")

min_roe = st.sidebar.slider(
    "Minimum ROE (%)",
    0,
    50,
    10
)

max_de = st.sidebar.slider(
    "Maximum Debt to Equity",
    0.0,
    10.0,
    2.0
)

min_interest = st.sidebar.slider(
    "Minimum Interest Coverage",
    0.0,
    50.0,
    2.0
)

min_revenue_cagr = st.sidebar.slider(
    "Minimum Revenue CAGR (%)",
    0.0,
    50.0,
    0.0
)

min_profit_margin = st.sidebar.slider(
    "Minimum Net Profit Margin (%)",
    0.0,
    50.0,
    5.0
)


if preset == "Quality Compounder":
    st.success("Quality Compounder Applied")

    filtered = df[
        (df["return_on_equity_pct"] >= 15)
        & (df["debt_to_equity"] <= 2)
        & (df["interest_coverage"] >= 2)
    ]

elif preset == "Value Pick":
    st.success("Value Pick Applied")

    filtered = df[df["debt_to_equity"] <= 1]

elif preset == "Growth Accelerator":
    st.success("Growth Accelerator Applied")

    filtered = df[
        (df["return_on_equity_pct"] >= 20)
        & (df["net_profit_margin_pct"] >= 15)
        & (df["interest_coverage"] >= 5)
    ]

elif preset == "Dividend Champion":
    st.success("Dividend Champion Applied")

    filtered = df[df["dividend_payout_ratio_pct"].fillna(0) >= 20]

elif preset == "Debt-Free Blue Chip":
    st.success("Debt-Free Blue Chip Applied")

    filtered = df[df["debt_to_equity"] == 0]

else:
    filtered = df[
        (df["return_on_equity_pct"] >= min_roe)
        & (df["debt_to_equity"] <= max_de)
        & (df["interest_coverage"] >= min_interest)
        & (df["revenue_cagr_5yr"].fillna(0) >= min_revenue_cagr)
        & (df["net_profit_margin_pct"] >= min_profit_margin)
    ]

st.subheader(f"Matching Companies ({len(filtered)})")

display_df = filtered[
    [
        "company_id",
        "year",
        "return_on_equity_pct",
        "debt_to_equity",
        "interest_coverage",
        "revenue_cagr_5yr",
        "net_profit_margin_pct",
    ]
].sort_values(
    by="return_on_equity_pct",
    ascending=False
)

st.dataframe(
    display_df,
    use_container_width=True
)

csv = display_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Results",
    data=csv,
    file_name="screened_companies.csv",
    mime="text/csv",
)