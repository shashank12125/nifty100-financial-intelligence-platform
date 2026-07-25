import sqlite3

import pandas as pd

DB_PATH = "output/nifty100.db"

conn = sqlite3.connect(DB_PATH)

print("Connected")

peer = pd.read_sql(
    "SELECT * FROM peer_percentiles",
    conn
)

groups = sorted(
    peer["peer_group_name"].dropna().unique()
)

print(f"Peer Groups : {len(groups)}")

writer = pd.ExcelWriter(
    "output/peer_comparison.xlsx",
    engine="openpyxl"
)

for group in groups:

    df = peer[
        peer["peer_group_name"] == group
    ].copy()

    summary = pd.DataFrame({

        "company_id": ["Median"],

        "peer_group_name": [group],

        "metric": [""],

        "value": [
            df["value"].median()
        ],

        "percentile_rank": [
            df["percentile_rank"].median()
        ],

        "year": [""]

    })

    df = pd.concat(
        [df, summary],
        ignore_index=True
    )

    sheet = group[:31]

    df.to_excel(
        writer,
        sheet_name=sheet,
        index=False
    )

writer.close()

conn.close()

print()

print("peer_comparison.xlsx Generated")