import plotly.graph_objects as go
import streamlit as st
from utils.db import (
    get_benchmark_company,
    get_company_metrics,
    get_peer_groups,
    get_peers,
)

st.title("🤝 Peer Comparison")

peer_groups = get_peer_groups()

selected_group = st.selectbox(
    "Select Peer Group",
    peer_groups["peer_group_name"]
)

peer_df = get_peers(selected_group)

company = st.selectbox(
    "Select Company",
    peer_df["company_id"]
)

st.subheader(f"{selected_group}")

display_df = peer_df[
    [
        "company_id",
        "is_benchmark"
    ]
].copy()

display_df["Selected"] = display_df["company_id"].apply(
    lambda x: "✅" if x == company else ""
)

display_df["Benchmark"] = display_df["is_benchmark"].map(
    {
        1: "⭐ Benchmark",
        0: ""
    }
)

display_df = display_df[
    [
        "company_id",
        "Selected",
        "Benchmark"
    ]
]

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)
benchmark_df = get_benchmark_company(selected_group)

benchmark_company = benchmark_df.iloc[0]["company_id"]

selected_metrics = get_company_metrics(company)
benchmark_metrics = get_company_metrics(benchmark_company)

if selected_metrics.empty or benchmark_metrics.empty:
    st.warning("Metrics not available.")
    st.stop()

# st.subheader("Selected Company Metrics")
#
# st.dataframe(selected_metrics)
#
# st.subheader("Benchmark Metrics")
#
# st.dataframe(benchmark_metrics)

    # a finl code

st.markdown(
    f"### {company} vs ⭐ {benchmark_company}"
)

st.info(
    "The benchmark company is the industry leader for the selected peer group."
)

st.subheader("📊 Radar Comparison")

categories = [
    "ROE",
    "Debt/Equity",
    "Interest Coverage",
    "Net Profit Margin",
    "Operating Margin",
    "Asset Turnover",
]

selected_values = [
    float(selected_metrics.iloc[0]["return_on_equity_pct"]),
    float(selected_metrics.iloc[0]["debt_to_equity"]),
    float(selected_metrics.iloc[0]["interest_coverage"]),
    float(selected_metrics.iloc[0]["net_profit_margin_pct"]),
    float(selected_metrics.iloc[0]["operating_profit_margin_pct"]),
    float(selected_metrics.iloc[0]["asset_turnover"]),
]

benchmark_values = [
    float(benchmark_metrics.iloc[0]["return_on_equity_pct"]),
    float(benchmark_metrics.iloc[0]["debt_to_equity"]),
    float(benchmark_metrics.iloc[0]["interest_coverage"]),
    float(benchmark_metrics.iloc[0]["net_profit_margin_pct"]),
    float(benchmark_metrics.iloc[0]["operating_profit_margin_pct"]),
    float(benchmark_metrics.iloc[0]["asset_turnover"]),
]

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=selected_values,
        theta=categories,
        fill="toself",
        name=company,
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=benchmark_values,
        theta=categories,
        fill="toself",
        name=benchmark_company,
    )
)

fig.update_layout(
    title=f"{company} vs {benchmark_company}",
    polar=dict(
        radialaxis=dict(visible=True)
    ),
    showlegend=True,
    height=600,
)


st.plotly_chart(
    fig,
    use_container_width=True
)

