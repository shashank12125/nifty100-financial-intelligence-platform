import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "output/nifty100.db"
SCHEMA_PATH = "db/schema.sql"

Path("output").mkdir(exist_ok=True)

# Fresh database
conn = sqlite3.connect(DB_PATH)
print("Connected to SQLite")

# Create schema
with open(SCHEMA_PATH, "r") as f:
    conn.executescript(f.read())

conn.execute("PRAGMA foreign_keys = OFF")

print("Schema loaded")

audit_log = []

def load_table(file_path, table_name, columns=None, header=1):
    df = pd.read_excel(file_path, header=header)

    if columns:
        df = df[columns]

    df.columns = [
        str(col).strip().lower()
        for col in df.columns
    ]

    df.to_sql(
        table_name,
        conn,
        if_exists="append",
        index=False
    )

    print(f"{table_name}: {len(df)} rows loaded")

    audit_log.append({
        "table_name": table_name,
        "rows_loaded": len(df)
    })

# Companies
load_table(
    "data/raw/companies.xlsx",
    "companies",
    columns=[
        "id",
        "company_name",
        "website",
        "face_value",
        "book_value",
        "roce_percentage",
        "roe_percentage"
    ]
)

# Core files
load_table(
    "data/raw/profitandloss.xlsx",
    "profitandloss"
)

load_table(
    "data/raw/balancesheet.xlsx",
    "balancesheet"
)

load_table(
    "data/raw/cashflow.xlsx",
    "cashflow"
)

load_table(
    "data/raw/analysis.xlsx",
    "analysis"
)

load_table(
    "data/raw/documents.xlsx",
    "documents"
)

load_table(
    "data/raw/prosandcons.xlsx",
    "prosandcons"
)

# Supporting files
load_table(
    "data/supporting/sectors.xlsx",
    "sectors",
    header=0
)

load_table(
    "data/supporting/stock_prices.xlsx",
    "stock_prices",
    header=0
)

load_table(
    "data/supporting/financial_ratios.xlsx",
    "financial_ratios",
    header=0
)

load_table(
    "data/supporting/peer_groups.xlsx",
    "peer_groups",
    header=0
)

# Audit CSV
audit_df = pd.DataFrame(audit_log)
audit_df.to_csv(
    "output/load_audit.csv",
    index=False
)

print("\nLoad Audit")
print(audit_df)

conn.close()
print("\nDatabase load complete.")