import sqlite3

import pandas as pd
import streamlit as st
from utils.db import DB_PATH

st.title("📑 Company Reports")
st.caption("Annual Reports of Nifty 100 Companies")
st.divider()

conn = sqlite3.connect(DB_PATH)

reports = pd.read_sql("""
SELECT
    company_id,
    year,
    annual_report
FROM documents
ORDER BY company_id, year DESC
""", conn)

conn.close()

companies = sorted(reports["company_id"].unique())

selected_company = st.selectbox(
    "Select Company",
    companies
)

company_reports = reports[
    reports["company_id"] == selected_company
]

st.subheader(f"{selected_company} Annual Reports")

for _, row in company_reports.iterrows():

    st.markdown(
        f"""
**{row['year']}**

📄 [Open Annual Report]({row['annual_report']})

---
"""
    )

st.dataframe(
    company_reports,
    use_container_width=True
)