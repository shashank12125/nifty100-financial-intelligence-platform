import sqlite3
from pathlib import Path

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

ROOT = Path(__file__).resolve().parents[2]

DB = ROOT / "output" / "nifty100.db"

REPORTS = ROOT / "reports"
PORTFOLIO = REPORTS / "portfolio"

PORTFOLIO.mkdir(parents=True, exist_ok=True)


def get_connection():
    return sqlite3.connect(DB)


def query(sql, params=None):
    conn = get_connection()
    df = pd.read_sql(sql, conn, params=params)
    conn.close()
    return df

def load_companies():
    sql = """
    SELECT
        c.id,
        c.company_name,
        s.broad_sector
    FROM companies c
    LEFT JOIN sectors s
        ON c.id = s.company_id
    ORDER BY c.id
    """
    return query(sql)

def load_ratios(company_id):
    sql = """
    SELECT *
    FROM financial_ratios
    WHERE company_id = ?
    ORDER BY year DESC
    LIMIT 2
    """
    return query(sql, [company_id])

def trend_arrow(current, previous):

    if pd.isna(current) or pd.isna(previous):
        return "-"

    if previous == 0:
        return "→"

    change = ((current - previous) / abs(previous)) * 100

    if change > 2:
        return "↑"

    elif change < -2:
        return "↓"

    else:
        return "→"

def build_portfolio():

    companies = load_companies()

    styles = getSampleStyleSheet()

    title = styles["Heading1"]
    title.alignment = TA_CENTER

    normal = styles["BodyText"]

    pdf = SimpleDocTemplate(
        str(PORTFOLIO / "portfolio_summary.pdf")
    )

    story = []

    for _, row in companies.iterrows():

        ratios = load_ratios(row["id"])

        if ratios.empty:
            continue

        latest = ratios.iloc[0]

        previous = ratios.iloc[1] if len(ratios) > 1 else latest

        story.append(
            Paragraph(row["company_name"], title)
        )

        story.append(
            Paragraph(f"<b>Ticker:</b> {row['id']}", normal)
        )

        story.append(
            Paragraph(f"<b>Sector:</b> {row['broad_sector']}", normal)
        )

        story.append(Spacer(1, 0.25 * inch))

        data = [
            ["KPI", "Value", "Trend"],
            [
                "Revenue CAGR",
                latest["revenue_cagr_5yr"],
                trend_arrow(
                    latest["revenue_cagr_5yr"],
                    previous["revenue_cagr_5yr"],
                ),
            ],
            [
                "PAT CAGR",
                latest["pat_cagr_5yr"],
                trend_arrow(
                    latest["pat_cagr_5yr"],
                    previous["pat_cagr_5yr"],
                ),
            ],
            [
                "ROE",
                latest["return_on_equity_pct"],
                trend_arrow(
                    latest["return_on_equity_pct"],
                    previous["return_on_equity_pct"],
                ),
            ],
            [
                "Net Margin",
                latest["net_profit_margin_pct"],
                trend_arrow(
                    latest["net_profit_margin_pct"],
                    previous["net_profit_margin_pct"],
                ),
            ],
            [
                "Debt/Equity",
                latest["debt_to_equity"],
                trend_arrow(
                    latest["debt_to_equity"],
                    previous["debt_to_equity"],
                ),
            ],
            [
                "EPS",
                latest["earnings_per_share"],
                trend_arrow(
                    latest["earnings_per_share"],
                    previous["earnings_per_share"],
                ),
            ],
        ]

        table = Table(data)

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ]
            )
        )

        story.append(table)
        story.append(PageBreak())

    pdf.build(story)

    print("Portfolio Summary Generated")

if __name__ == "__main__":
    build_portfolio()