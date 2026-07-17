import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import (
    get_sectors,
    get_all_ratios,
    get_stock_prices,
)

st.title("🏭 Sector Analysis")
st.caption("Sector-wise comparison of Nifty 100 companies")
st.divider()

sectors_df = get_sectors()
ratios_df = get_all_ratios()
prices_df = get_stock_prices()

latest_ratios = (
    ratios_df
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
)

latest_prices = (
    prices_df
    .sort_values("date")
    .groupby("company_id")
    .tail(1)
)

sector_data = (
    sectors_df
    .merge(
        latest_ratios[
            [
                "company_id",
                "return_on_equity_pct"
            ]
        ],
        on="company_id",
        how="left"
    )
    .merge(
        latest_prices[
            [
                "company_id",
                "close_price"
            ]
        ],
        on="company_id",
        how="left"
    )
)

selected_sector = st.sidebar.selectbox(
    "Select Sector",
    sorted(sector_data["broad_sector"].dropna().unique())
)

filtered = sector_data[
    sector_data["broad_sector"] == selected_sector
]

st.subheader("Sector Bubble Chart")

fig = px.scatter(
    filtered,
    x="close_price",
    y="return_on_equity_pct",
    size="index_weight_pct",
    color="sub_sector",
    hover_name="company_id",
    title=f"{selected_sector} Companies",
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Median ROE by Sub Sector")

median_df = (
    filtered
    .groupby("sub_sector")["return_on_equity_pct"]
    .median()
    .reset_index()
)

fig2 = px.bar(
    median_df,
    x="sub_sector",
    y="return_on_equity_pct",
    title="Median ROE",
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.subheader("Sector Companies")

st.dataframe(
    filtered[
        [
            "company_id",
            "sub_sector",
            "return_on_equity_pct",
            "close_price",
            "index_weight_pct",
        ]
    ],
    use_container_width=True,
)