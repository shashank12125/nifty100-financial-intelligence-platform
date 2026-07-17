import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import get_cashflow

st.title("💰 Capital Allocation Map")
st.caption("Cash Flow based capital allocation patterns")
st.divider()

cash_df = get_cashflow()

latest = (
    cash_df
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
)
def classify(row):

    op = row["operating_activity"]
    inv = row["investing_activity"]
    fin = row["financing_activity"]

    if op > 0 and inv < 0:
        return "Growth"

    elif op > 0 and fin < 0:
        return "Shareholder Return"

    elif op < 0:
        return "Weak Cash Flow"

    else:
        return "Balanced"

latest["pattern"] = latest.apply(classify, axis=1)

fig = px.treemap(
    latest,
    path=["pattern", "company_id"],
    values="operating_activity",
    color="operating_activity",
)

st.plotly_chart(
    fig,
    use_container_width=True
)

pattern = st.selectbox(
    "Select Pattern",
    sorted(latest["pattern"].unique())
)

filtered = latest[
    latest["pattern"] == pattern
]

st.subheader(f"{pattern} Companies")

st.dataframe(
    filtered[
        [
            "company_id",
            "operating_activity",
            "investing_activity",
            "financing_activity",
            "net_cash_flow",
        ]
    ],
    use_container_width=True,
)