import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DB_PATH = "output/nifty100.db"

OUTPUT_DIR = Path("reports/radar_charts")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql("""
SELECT
company_id,
year,
return_on_equity_pct,
net_profit_margin_pct,
debt_to_equity,
asset_turnover,
composite_quality_score
FROM financial_ratios
""", conn)

conn.close()

metrics = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "asset_turnover",
    "composite_quality_score"
]

latest = (
    df.sort_values("year")
      .groupby("company_id")
      .tail(1)
)

print(f"Charts to Generate: {len(latest)}")

for _, row in latest.iterrows():

    values = []

    for metric in metrics:

        value = row[metric]

        if pd.isna(value):
            value = 0

        values.append(value)

    values.append(values[0])

    angles = np.linspace(
        0,
        2*np.pi,
        len(metrics),
        endpoint=False
    ).tolist()

    angles.append(angles[0])

    plt.figure(figsize=(6,6))

    ax = plt.subplot(111, polar=True)

    ax.plot(
        angles,
        values,
        linewidth=2
    )

    ax.fill(
        angles,
        values,
        alpha=0.25
    )

    ax.set_xticks(angles[:-1])

    ax.set_xticklabels([
        "ROE",
        "NPM",
        "D/E",
        "AT",
        "Score"
    ])

    plt.title(row["company_id"])

    plt.savefig(
        OUTPUT_DIR /
        f"{row['company_id']}_radar.png",
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()

print("\nRadar Charts Generated Successfully.")