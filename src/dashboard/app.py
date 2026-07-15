import streamlit as st
import plotly.express as px
import importlib.util
from pathlib import Path


from utils.db import (
    get_companies,
    get_ratios,
    get_pl,
    get_bs,
    get_cf,
    get_dashboard_summary,
    get_sector_breakdown,
    get_top_companies

)
st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📈 Nifty 100 Financial Intelligence Platform")
companies = get_companies()

summary = get_dashboard_summary()

st.subheader("Dashboard Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Companies",
        summary["total_companies"]
    )

with col2:
    st.metric(
        "Average ROE",
        summary["avg_roe"]
    )

with col3:
    st.metric(
        "Average D/E",
        summary["median_de"]
    )

with col4:
    st.metric(
        "Debt Free Companies",
        summary["debt_free"]
    )

st.subheader("Sector Breakdown")

sector_df = get_sector_breakdown()

fig = px.pie(
    sector_df,
    names="broad_sector",
    values="company_count",
    hole=0.5,
    title="Companies by Sector"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Top 5 Companies by ROE")

top_companies = get_top_companies()

st.dataframe(
    top_companies,
    use_container_width=True
)

st.success(f"Total Companies: {len(companies)}")

st.dataframe(companies.head())


st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Home",
        "Company Profile",
        "Screener",
        "Peer Comparison",
        "Trend Analysis",
        "Sector Analysis",
        "Capital Allocation",
        "Annual Reports"
    ]
)

st.header(page)

PAGES = {
    "Home": "01_home.py",
    "Company Profile": "02_profile.py",
    "Screener": "03_screener.py",
    "Peer Comparison": "04_peers.py",
    "Trend Analysis": "05_trends.py",
    "Sector Analysis": "06_sectors.py",
    "Capital Allocation": "07_capital.py",
    "Annual Reports": "08_reports.py"
}

page_file = Path(__file__).parent / "pages" / PAGES[page]

spec = importlib.util.spec_from_file_location(
    page,
    page_file
)

module = importlib.util.module_from_spec(spec)

spec.loader.exec_module(module)