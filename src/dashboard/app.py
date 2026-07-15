import streamlit as st
from utils.db import (
    get_companies,
    get_ratios,
    get_pl,
    get_bs,
    get_cf
)
from utils.db import get_companies, get_ratios


st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📈 Nifty 100 Financial Intelligence Platform")
companies = get_companies()

ratios = get_ratios("TCS")
pl = get_pl("TCS")
bs = get_bs("TCS")
cf = get_cf("TCS")

st.write(f"P&L Rows: {len(pl)}")
st.write(f"Balance Sheet Rows: {len(bs)}")
st.write(f"Cash Flow Rows: {len(cf)}")

st.subheader("TCS Financial Ratios")

st.write(f"Rows Found: {len(ratios)}")

st.dataframe(ratios.head())

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

st.info(f"{page} page is under development.")