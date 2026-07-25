import plotly.express as px
import streamlit as st
from utils.db import (
    get_companies,
    get_company_profile,
    get_revenue_profit,
    get_roe_roce_trend,
)

st.title("🏢 Company Profile")

companies = get_companies()

ticker = st.selectbox(
    "Select Company",
    companies["id"].tolist()
)

profile = get_company_profile(ticker)

if profile.empty:
    st.warning("Ticker not found.")
else:
    st.title(profile.iloc[0]["company_name"])

    st.caption(f"Ticker : {ticker}")

    st.divider()
    
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Face Value",
            profile.iloc[0]["face_value"]
        )

        st.metric(
            "ROE",
            profile.iloc[0]["roe_percentage"]
        )

        st.caption(f"Ticker : {ticker}")

        st.divider()

    with col2:
        st.metric(
            "Book Value",
            profile.iloc[0]["book_value"]
        )

        st.metric(
            "ROCE",
            profile.iloc[0]["roce_percentage"]
        )

    st.link_button(
        "Visit Company Website",
        profile.iloc[0]["website"]
    )

    st.subheader("Revenue & Net Profit Trend")

    trend_df = get_revenue_profit(ticker)

    if trend_df.empty:
        st.info("No financial data available.")
    else:
        fig = px.bar(
            trend_df,
            x="year",
            y=["sales", "net_profit"],
            barmode="group",
            title="Revenue vs Net Profit"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("ROE Trend")

    roe_df = get_roe_roce_trend(ticker)

    if roe_df.empty:
        st.info("No ROE trend available.")
    else:
        fig = px.line(
            roe_df,
            x="year",
            y=[
                "return_on_equity_pct",
                "operating_profit_margin_pct"
            ],
            markers=True,
            title="ROE vs Operating Profit Margin Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )