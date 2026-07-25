import sqlite3
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / "output" / "nifty100.db"
OUT = ROOT / "reports" / "sector"
OUT.mkdir(parents=True, exist_ok=True)

styles = getSampleStyleSheet()

conn = sqlite3.connect(DB)

sectors = pd.read_sql("""
SELECT DISTINCT broad_sector
FROM sectors
ORDER BY broad_sector
""", conn)

for sector in sectors["broad_sector"]:

    df = pd.read_sql("""

    SELECT

    s.company_id,
    c.company_name,

    r.return_on_equity_pct,
    r.net_profit_margin_pct,
    r.operating_profit_margin_pct,
    r.debt_to_equity,
    r.interest_coverage,
    r.asset_turnover,
    r.free_cash_flow_cr,
    r.composite_quality_score

    FROM sectors s

    JOIN companies c
      ON s.company_id=c.id

    LEFT JOIN financial_ratios r
      ON s.company_id=r.company_id

    WHERE s.broad_sector=?

    """, conn, params=(sector,))

    if df.empty:
        continue

    latest = (
        df.sort_values("company_id")
          .groupby("company_id")
          .tail(1)
    )

    pdf = SimpleDocTemplate(
        str(OUT / f"{sector}_report.pdf")
    )

    story=[]

    story.append(
        Paragraph(
            f"<b>{sector} Sector Report</b>",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1,12))

    story.append(
        Paragraph("<b>Median KPIs</b>",styles["Heading2"])
    )

    metrics=[
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",
        "free_cash_flow_cr",
        "composite_quality_score"
    ]

    med=[]

    for m in metrics:
        med.append([m, round(latest[m].median(),2)])

    t=Table(med)

    t.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),0.5,colors.grey),
        ("BACKGROUND",(0,0),(-1,-1),colors.beige)
    ]))

    story.append(t)

    story.append(Spacer(1,20))

    story.append(
        Paragraph("<b>Companies</b>",styles["Heading2"])
    )

    rows=[[
        "Company",
        "ROE",
        "NPM",
        "OPM",
        "D/E",
        "IC",
        "AT",
        "FCF",
        "Score"
    ]]

    for _,r in latest.iterrows():

        rows.append([

            r["company_name"],

            r["return_on_equity_pct"],
            r["net_profit_margin_pct"],
            r["operating_profit_margin_pct"],
            r["debt_to_equity"],
            r["interest_coverage"],
            r["asset_turnover"],
            r["free_cash_flow_cr"],
            r["composite_quality_score"]

        ])

    tbl=Table(rows)

    tbl.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),0.5,colors.grey),
        ("BACKGROUND",(0,0),(-1,0),colors.lightgrey),
        ("FONTSIZE",(0,0),(-1,-1),8),
        ("BOTTOMPADDING",(0,0),(-1,-1),5)
    ]))

    story.append(tbl)

    pdf.build(story)

    print(sector,"Done")

conn.close()

print("All sector reports generated.")