# 📈 Nifty100 Financial Intelligence Platform

A comprehensive Financial Analytics Platform for Nifty100 companies built using Python, Streamlit, FastAPI, SQLite, and Plotly. The platform provides financial analysis, company insights, stock screening, peer comparison, valuation analytics, downloadable reports, and an interactive dashboard.

---

# Features

- 📊 Interactive Dashboard
- 🏢 Company Profile Analysis
- 🔍 Stock Screener
- 🤝 Peer Comparison
- 📈 Trend Analysis
- 🏭 Sector Analysis
- 💰 Capital Allocation Analysis
- 📑 Annual Reports
- 📊 Valuation Analytics
- ⚡ FastAPI REST API
- 📄 PDF Tearsheet Generation
- 📈 Financial KPI Analytics
- 🗄️ SQLite Database
- ✅ Automated Testing

---

# Tech Stack

- Python
- Streamlit
- FastAPI
- SQLite
- Pandas
- Plotly
- OpenPyXL
- ReportLab
- Pytest
- Ruff
- Black

---

# Project Structure

```text
nifty100-platform/
│
├── data/
├── docs/
├── output/
├── screenshots/
├── src/
│   ├── analytics/
│   ├── api/
│   ├── dashboard/
│   ├── etl/
│   ├── reports/
│   └── scripts/
├── tests/
├── README.md
└── requirements.txt
```

---

# Installation

```bash
git clone <repository-url>

cd nifty100-platform

pip install -r requirements.txt
```

---

# Run Dashboard

```bash
streamlit run src/dashboard/app.py
```

---

# Run API

```bash
uvicorn src.api.main:app --reload
```

---

# Run Tests

```bash
python -m pytest tests -q
```

Current Status

```
79 passed
```

---

# Code Quality

Format code

```bash
python -m black src tests
```

Lint code

```bash
python -m ruff check src tests
```

---

# Generated Outputs

- Valuation Summary
- Valuation Flags
- Performance Notes
- Company PDF Tearsheet
- Financial Reports

---

# Dashboard Modules

- Home Dashboard
- Company Profile
- Stock Screener
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Allocation
- Annual Reports
- Valuation Analytics

---

# Screenshots

## Dashboard

![Dashboard](screenshots/dashboard.png)

## Home

![Home](screenshots/home.png)

## Company Profile

![Company Profile](screenshots/company%20profile.png)

## Stock Screener

![Stock Screener](screenshots/stock%20scrreener.png)

## Peer Comparison

![Peer Comparison](screenshots/peer%20comparison.png)

## Trend Analysis

![Trend Analysis](screenshots/trend%20analysis.png)

## Sector Analysis

![Sector Analysis](screenshots/sector%20analysis.png)

## Capital Allocation

![Capital Allocation](screenshots/capital%20allocation%20map.png)

## Company Reports

![Company Reports](screenshots/company%20reports.png)

---

# Sprint Deliverables

- ✅ ETL Pipeline
- ✅ SQLite Database
- ✅ FastAPI Backend
- ✅ Streamlit Dashboard
- ✅ Financial KPI Analytics
- ✅ Stock Screener
- ✅ Peer Comparison
- ✅ PDF Tearsheet Generator
- ✅ Automated Tests (79 Passed)
- ✅ Performance Optimization
- ✅ Code Formatting & Linting

---

# Author

**Shashank Charpe**

MCA Graduate | Java Backend Developer | Python | Data Analytics