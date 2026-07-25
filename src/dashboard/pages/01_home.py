import plotly.express as px
import streamlit as st
from utils.db import (
    get_all_ratios,
    get_companies,
    get_sectors,
)

st.title("📊 Nifty 100 Analytics Dashboard")
st.caption("Overview of all Nifty 100 companies")
st.divider()

companies_df = get_companies()
ratios_df = get_all_ratios()

# upadated
annual_ratios = ratios_df[
    ratios_df["year"].str.startswith("Mar")
]
available_years = sorted(
    annual_ratios["year"].unique(),
    reverse=True
)

selected_year = st.sidebar.selectbox(
    "Financial Year",
    available_years
)

latest_ratios = annual_ratios[
    annual_ratios["year"] == selected_year
]


sectors_df = get_sectors()

filtered_roe = latest_ratios[
    latest_ratios["return_on_equity_pct"].between(0, 100)
]

avg_roe = filtered_roe["return_on_equity_pct"].mean()

median_de = latest_ratios["debt_to_equity"].median()

debt_free = (
    latest_ratios["debt_to_equity"] <= 0
).sum()

avg_net_profit_margin = latest_ratios[
    "net_profit_margin_pct"
].mean()


if latest_ratios["composite_quality_score"].notna().any():
    avg_quality_score = latest_ratios["composite_quality_score"].mean()
else:
    avg_quality_score = None

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)


with col1:
    st.metric(
        "Total Companies",
        len(companies_df)
    )

with col2:
    st.metric(
        "Average ROE",
        f"{avg_roe:.2f}%"
    )

with col3:
    st.metric(
        "Median D/E",
        f"{median_de:.2f}"
    )

with col4:
    st.metric(
        "Debt-Free Companies",
        debt_free
    )

with col5:
    st.metric(
        "Avg Net Profit Margin",
        f"{avg_net_profit_margin:.2f}%"
    )

with col6:
    st.metric(
        "Financial Year",
        selected_year
    )

st.divider()

st.subheader("🏭 Sector Breakdown")

sector_count = (
    sectors_df
    .groupby("broad_sector")
    .size()
    .reset_index(name="Companies")
)

fig = px.pie(
    sector_count,
    names="broad_sector",
    values="Companies",
    hole=0.5,
    title="Companies by Broad Sector"
)

st.plotly_chart(
    fig,
    use_container_width=True
)