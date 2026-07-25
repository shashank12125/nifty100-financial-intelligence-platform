import sqlite3
from pathlib import Path

import pandas as pd
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[2]

DB = ROOT / "output" / "nifty100.db"
OUTPUT = ROOT / "output"

REPORTS = ROOT / "reports"

TEARSHEETS = REPORTS / "tearsheets"

SECTOR_REPORTS = REPORTS / "sector"


styles = getSampleStyleSheet()

title_style = styles["Heading1"]
title_style.alignment = TA_CENTER

heading_style = styles["Heading2"]

normal = styles["BodyText"]

normal.wordWrap = "CJK"


# ---------------------------------------------------
# DATABASE
# ---------------------------------------------------

def get_connection():
    return sqlite3.connect(DB)


def query(sql, params=None):
    conn = get_connection()

    df = pd.read_sql_query(
        sql,
        conn,
        params=params
    )

    conn.close()

    return df


# ---------------------------------------------------
# COMPANY DATA
# ---------------------------------------------------

def load_company(company):

    company_info = query(
        """
        SELECT *
        FROM companies
        WHERE id=?
        """,
        (company,)
    )

    pnl = query(
        """
        SELECT *
        FROM profitandloss
        WHERE company_id=?
        ORDER BY year
        """,
        (company,)
    )

    balance = query(
        """
        SELECT *
        FROM balancesheet
        WHERE company_id=?
        ORDER BY year
        """,
        (company,)
    )

    cash = query(
        """
        SELECT *
        FROM cashflow
        WHERE company_id=?
        ORDER BY year
        """,
        (company,)
    )

    ratios = query(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        ORDER BY year
        """,
        (company,)
    )

    proscons = query(
        """
        SELECT *
        FROM prosandcons
        WHERE company_id=?
        """,
        (company,)
    )

    return (
        company_info,
        pnl,
        balance,
        cash,
        ratios,
        proscons,
    )


# ---------------------------------------------------
# KPI TILE
# ---------------------------------------------------

def kpi_tile(title, value):

    tbl = Table(
        [
            [
                Paragraph(
                    f"<b>{title}</b>",
                    normal,
                )
            ],
            [
                Paragraph(
                    str(value),
                    title_style,
                )
            ]
        ],
        colWidths=150,
    )

    tbl.setStyle(

        TableStyle(

            [

                ("GRID",(0,0),(-1,-1),0.5,colors.grey),

                ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0b3d91")),

                ("TEXTCOLOR",(0,0),(-1,0),colors.white),

                ("ALIGN",(0,0),(-1,-1),"CENTER"),

                ("BOTTOMPADDING",(0,0),(-1,-1),8),

            ]

        )

    )

    return tbl


# ---------------------------------------------------
# BAR CHART
# ---------------------------------------------------

def create_bar_chart(values, labels, title):

    drawing = Drawing(260,180)

    chart = VerticalBarChart()

    chart.x = 40
    chart.y = 30

    chart.width = 180
    chart.height = 110

    chart.data = [values]

    chart.categoryAxis.categoryNames = labels

    drawing.add(chart)

    return drawing


# ---------------------------------------------------
# LINE CHART
# ---------------------------------------------------

def create_line_chart(series1, series2, labels):

    drawing = Drawing(260,180)

    chart = HorizontalLineChart()

    chart.x = 40
    chart.y = 30

    chart.width = 180
    chart.height = 110

    chart.data = [
        series1,
        series2
    ]

    chart.categoryAxis.categoryNames = labels

    drawing.add(chart)

    return drawing


# ---------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------

def page_header(company_name, ticker):

    table = Table(

        [

            [

                Paragraph(

                    f"<font color='white'><b>{company_name:45}</b><br/>{ticker}</font>",

                    heading_style

                )

            ]

        ],

        colWidths=520

    )

    table.setStyle(

        TableStyle(

            [

                ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#082b6f")),

                ("BOTTOMPADDING",(0,0),(-1,-1),12),

                ("TOPPADDING",(0,0),(-1,-1),12),

                ("LEFTPADDING",(0,0),(-1,-1),10),

            ]

        )

    )

    return table

# ---------------------------------------------------
# PAGE 1
# ---------------------------------------------------

def build_page_one(story, company):

    info, pnl, balance, cash, ratios, proscons = load_company(company)

    if info.empty:
        return

    company_name = info.iloc[0]["company_name"]

    story.append(
        page_header(company_name, company)
    )

    story.append(Spacer(1, 12))

    latest_pnl = pnl.iloc[-1] if not pnl.empty else None
    latest_ratio = ratios.iloc[-1] if not ratios.empty else None

    # ---------------- KPIs ----------------

    kpis = [

        kpi_tile(
            "Revenue",
            round(latest_pnl["sales"], 2)
            if latest_pnl is not None else "-"
        ),

        kpi_tile(
            "Net Profit",
            round(latest_pnl["net_profit"], 2)
            if latest_pnl is not None else "-"
        ),

        kpi_tile(
            "ROE %",
            round(latest_ratio["return_on_equity_pct"], 2)
            if latest_ratio is not None else "-"
        ),

        kpi_tile(
            "Debt/Equity",
            round(latest_ratio["debt_to_equity"], 2)
            if latest_ratio is not None else "-"
        ),

        kpi_tile(
            "EPS",
            round(latest_ratio["earnings_per_share"], 2)
            if latest_ratio is not None else "-"
        ),

        kpi_tile(
            "FCF",
            round(latest_ratio["free_cash_flow_cr"], 2)
            if latest_ratio is not None else "-"
        ),

    ]

    kpi_table = Table(
        [
            kpis[:3],
            kpis[3:]
        ]
    )

    kpi_table.setStyle(

        TableStyle(

            [

                ("BOTTOMPADDING", (0,0), (-1,-1), 8),

                ("TOPPADDING", (0,0), (-1,-1), 8),

                ("ALIGN",(0,0),(-1,-1),"CENTER")

            ]

        )

    )

    story.append(kpi_table)

    story.append(Spacer(1,18))

    # ---------------- Revenue Chart ----------------

    revenue_chart = create_bar_chart(

        pnl["sales"].fillna(0).tolist(),

        pnl["year"].tolist(),

        "Revenue"

    )

    # ---------------- Net Profit ----------------

    profit_chart = create_bar_chart(

        pnl["net_profit"].fillna(0).tolist(),

        pnl["year"].tolist(),

        "Net Profit"

    )

    chart_table = Table(

        [

            [

                revenue_chart,

                profit_chart

            ]

        ]

    )

    story.append(chart_table)

    story.append(Spacer(1,18))

    # ---------------- ROE ROCE ----------------

    roe = ratios["return_on_equity_pct"].fillna(0).tolist()

    roce = []

    for _, row in pnl.iterrows():

        yr = row["year"]

        r = query(
            """
            SELECT roce_percentage
            FROM companies
            WHERE id=?
            """,
            (company,)
        )

        if r.empty:
            roce.append(0)
        else:
            roce.append(r.iloc[0]["roce_percentage"])

    line = create_line_chart(

        roe,

        roce,

        pnl["year"].tolist()

    )

    story.append(line)

    story.append(Spacer(1,20))

def build_tearsheet(company):

    story = []

    pdf_path = str(OUTPUT / f"{company}.pdf")

    pdf = SimpleDocTemplate(
        pdf_path,
        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20
    )

    pdf = SimpleDocTemplate(
        str(TEARSHEETS / f"{company}_tearsheet.pdf"),
        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20
    )

    build_page_one(

        story,

        company

    )

    build_page_two(

        story,

        company

    )

    pdf.build(story)

    print(company, "Done")

# ---------------------------------------------------
# PAGE 2
# ---------------------------------------------------

def build_page_two(story, company):

    info, pnl, balance, cash, ratios, proscons = load_company(company)

    story.append(PageBreak())

    story.append(
        Paragraph("<b>Financial Intelligence</b>", heading_style)
    )

    story.append(Spacer(1, 12))

    # -------------------------------------------------
    # Balance Sheet Composition
    # -------------------------------------------------

    latest = balance.tail(8)

    labels = latest["year"].tolist()

    equity = latest["equity_capital"].fillna(0).tolist()

    debt = latest["borrowings"].fillna(0).tolist()

    liabilities = latest["other_liabilities"].fillna(0).tolist()

    drawing = Drawing(520,220)

    chart = VerticalBarChart()

    chart.x = 50
    chart.y = 35

    chart.width = 380
    chart.height = 140

    chart.data = [

        equity,

        debt,

        liabilities

    ]

    chart.categoryAxis.categoryNames = labels

    drawing.add(chart)

    story.append(
        Paragraph("<b>Balance Sheet Composition</b>", normal)
    )

    story.append(drawing)

    story.append(Spacer(1,15))

    # -------------------------------------------------
    # Cash Flow
    # -------------------------------------------------

    latest_cash = cash.iloc[-1]

    cf_labels = [

        "CFO",

        "CFI",

        "CFF",

        "Net"

    ]

    cf_values = [

        latest_cash["operating_activity"],

        latest_cash["investing_activity"],

        latest_cash["financing_activity"],

        latest_cash["net_cash_flow"]

    ]

    cash_chart = create_bar_chart(

        cf_values,

        cf_labels,

        "Cash Flow"

    )

    story.append(

        Paragraph(

            "<b>Latest Cash Flow</b>",

            normal

        )

    )

    story.append(cash_chart)

    story.append(Spacer(1,18))

    # -------------------------------------------------
    # Pros & Cons
    # -------------------------------------------------

    pros = ""

    cons = ""

    if not proscons.empty:

        pros = str(proscons.iloc[0]["pros"])

        cons = str(proscons.iloc[0]["cons"])

    table = Table(

        [

            [

                Paragraph(

                    "<font color='green'><b>Pros</b></font>",

                    normal

                ),

                Paragraph(

                    "<font color='red'><b>Cons</b></font>",

                    normal

                )

            ],

            [

                Paragraph(
                    pros.replace("\n", "<br/>"),
                    normal
                ),

                Paragraph(
                    cons.replace("\n", "<br/>"),
                    normal
                )

            ]

        ],

        colWidths=[255,255]

    )

    table.setStyle(

        TableStyle(

            [

                ("GRID",(0,0),(-1,-1),0.5,colors.grey),

                ("VALIGN",(0,0),(-1,-1),"TOP"),

                ("WORDWRAP",(0,0),(-1,-1),True),

                ("BOTTOMPADDING",(0,0),(-1,-1),8),

            ]

        )

    )

    story.append(table)

    story.append(Spacer(1,15))

    # -------------------------------------------------
    # Capital Allocation Badge
    # -------------------------------------------------

    try:

        allocation = pd.read_csv(

            OUTPUT / "capital_allocation.csv"

        )

        latest = allocation[

            allocation["company_id"] == company

        ].iloc[-1]

        badge = latest["pattern_label"]

    except Exception:

        badge = "Not Available"

    badge_tbl = Table(

        [

            [

                Paragraph(

                    f"<b>Capital Allocation:</b> {badge}",

                    normal

                )

            ]

        ],

        colWidths=520

    )

    badge_tbl.setStyle(

        TableStyle(

            [

                ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#E8F5E9")),

                ("GRID",(0,0),(-1,-1),0.5,colors.green),

                ("ALIGN",(0,0),(-1,-1),"CENTER"),

                ("BOTTOMPADDING",(0,0),(-1,-1),10)

            ]

        )

    )

    story.append(badge_tbl)

    # ---------------------------------------------------
    # BATCH GENERATION
    # ---------------------------------------------------

companies = query("""
SELECT id
FROM companies
ORDER BY id
""")

def batch_generate():

    companies = query("""
    SELECT id
    FROM companies
    ORDER BY id
    """)

    success = 0
    failed = []

    for _, row in companies.iterrows():

        company = row["id"]

        try:

            print(f"Generating {company}...")

            build_tearsheet(company)

            success += 1

        except Exception as e:

            failed.append(
                {
                    "company": company,
                    "error": str(e)
                }
            )

            print(f"{company} Failed -> {e}")

    print("=" * 60)
    print("Batch Generation Completed")
    print("=" * 60)
    print("Success :", success)
    print("Failed :", len(failed))

    if failed:
        print("\nErrors:")
        for f in failed:
            print(f)

        pd.DataFrame(failed).to_csv(
            OUTPUT / "skipped_tearsheets.csv",
            index=False
        )

        print("\nSkipped tickers saved to output/skipped_tearsheets.csv")

if __name__ == "__main__":
    batch_generate()