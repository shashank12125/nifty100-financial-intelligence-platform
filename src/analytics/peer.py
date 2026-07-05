import sqlite3
import pandas as pd

DB_PATH = "output/nifty100.db"

conn = sqlite3.connect(DB_PATH)

print("Connected to SQLite")

# ----------------------------
# Load Tables
# ----------------------------

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

peer_groups = pd.read_sql(
    "SELECT * FROM peer_groups",
    conn
)

print(f"Financial Ratios : {len(ratios)}")
print(f"Peer Group Rows  : {len(peer_groups)}")

# ----------------------------
# Merge
# ----------------------------

df = ratios.merge(
    peer_groups,
    on="company_id",
    how="left"
)

print(f"Merged Rows : {len(df)}")

# ----------------------------
# Metrics
# ----------------------------

metrics = [

    "return_on_equity_pct",

    "net_profit_margin_pct",

    "debt_to_equity",

    "asset_turnover"

]

records = []

# ----------------------------
# Percentile Ranking
# ----------------------------

for group in df["peer_group_name"].dropna().unique():

    peer_df = df[
        df["peer_group_name"] == group
    ].copy()

    for metric in metrics:

        peer_df["percentile_rank"] = (
            peer_df[metric]
            .rank(pct=True)
            * 100
        )

        for _, row in peer_df.iterrows():

            records.append({

                "company_id": row["company_id"],

                "peer_group_name": group,

                "metric": metric,

                "value": row[metric],

                "percentile_rank": round(
                    row["percentile_rank"],
                    2
                ),

                "year": row["year"]

            })

peer_percentiles = pd.DataFrame(records)

print()

print(peer_percentiles.head())

print()

print(
    f"Rows Generated : {len(peer_percentiles)}"
)

# ----------------------------
# SQLite
# ----------------------------

peer_percentiles.to_sql(

    "peer_percentiles",

    conn,

    if_exists="replace",

    index=False

)

print()

print("peer_percentiles table created.")

conn.close()