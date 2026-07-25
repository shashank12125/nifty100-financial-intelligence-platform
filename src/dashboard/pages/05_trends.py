import plotly.express as px
import streamlit as st
from utils.db import (
    get_companies,
    get_profit_loss,
)

st.title("📈 Trend Analysis")
st.caption("Visualize financial performance over time")
st.divider()

companies_df = get_companies()

selected_company = st.selectbox(
    "Select Company",
    companies_df["id"].tolist()
)

pl_df = get_profit_loss(selected_company)

if pl_df.empty:
    st.warning("No financial data available for this company.")
    st.stop()

metric = st.selectbox(
    "Select Metric",
    {
        "Sales": "sales",
        "Operating Profit": "operating_profit",
        "Net Profit": "net_profit",
        "EPS": "eps",
    }
)

metric_column = {
    "Sales": "sales",
    "Operating Profit": "operating_profit",
    "Net Profit": "net_profit",
    "EPS": "eps",
}[metric]

fig = px.line(
    pl_df,
    x="year",
    y=metric_column,
    markers=True,
    title=f"{metric} Trend"
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title=metric,
    template="plotly_white"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Financial Data")

st.dataframe(
    pl_df[
        [
            "year",
            metric_column
        ]
    ],
    use_container_width=True
)