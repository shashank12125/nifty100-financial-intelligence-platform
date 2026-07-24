from fastapi import APIRouter, HTTPException
from typing import Optional
from src.api.database import get_connection

router = APIRouter(prefix="/api/v1/companies", tags=["Companies"])

@router.get("")
def get_companies(
        sector: Optional[str] = None,
        market_cap_category: Optional[str] = None,
        search: Optional[str] = None
):

    conn = get_connection()

    query = """
    SELECT
        c.id,
        c.company_name,
        s.broad_sector,
        s.sub_sector,
        c.roe_percentage,
        c.roce_percentage,
        s.market_cap_category
    FROM companies c
    LEFT JOIN sectors s
    ON c.id=s.company_id
    WHERE 1=1
    """

    params=[]

    if sector:
        query+=" AND s.broad_sector=?"
        params.append(sector)

    if market_cap_category:
        query+=" AND s.market_cap_category=?"
        params.append(market_cap_category)

    if search:
        query+=" AND (c.company_name LIKE ? OR c.id LIKE ?)"
        params.extend([f"%{search}%",f"%{search}%"])

    query+=" ORDER BY c.company_name"

    rows=conn.execute(query,params).fetchall()

    conn.close()

    return [dict(r) for r in rows]


@router.get("/{ticker}")
def company_profile(ticker: str):

    conn = get_connection()

    row = conn.execute("""

    SELECT
        c.*,
        s.*,
        fr.*

    FROM companies c

    LEFT JOIN sectors s
        ON c.id = s.company_id

    LEFT JOIN financial_ratios fr
        ON c.id = fr.company_id
        AND CAST(SUBSTR(fr.year,5) AS INTEGER) = (
            SELECT MAX(CAST(SUBSTR(f2.year,5) AS INTEGER))
            FROM financial_ratios f2
            WHERE f2.company_id = c.id
        )

    WHERE
        c.id = ?

    """, (ticker,)).fetchone()

    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return dict(row)

@router.get("/{ticker}/pl")
def profit_loss(
        ticker:str,
        from_year:Optional[str]=None,
        to_year:Optional[str]=None
):

    conn=get_connection()

    query="SELECT * FROM profitandloss WHERE company_id=?"

    params=[ticker]

    if from_year:
        query+=" AND year>=?"
        params.append(from_year)

    if to_year:
        query+=" AND year<=?"
        params.append(to_year)

    query+=" ORDER BY year"

    rows=conn.execute(query,params).fetchall()

    conn.close()

    return [dict(r) for r in rows]


@router.get("/{ticker}/bs")
def balance_sheet(
        ticker:str,
        from_year:Optional[str]=None,
        to_year:Optional[str]=None
):

    conn=get_connection()

    query="SELECT * FROM balancesheet WHERE company_id=?"

    params=[ticker]

    if from_year:
        query+=" AND year>=?"
        params.append(from_year)

    if to_year:
        query+=" AND year<=?"
        params.append(to_year)

    query+=" ORDER BY year"

    rows=conn.execute(query,params).fetchall()

    conn.close()

    return [dict(r) for r in rows]


@router.get("/{ticker}/cashflow")
def cashflow(
        ticker:str,
        from_year:Optional[str]=None,
        to_year:Optional[str]=None
):

    conn=get_connection()

    query="SELECT * FROM cashflow WHERE company_id=?"

    params=[ticker]

    if from_year:
        query+=" AND year>=?"
        params.append(from_year)

    if to_year:
        query+=" AND year<=?"
        params.append(to_year)

    query+=" ORDER BY year"

    rows=conn.execute(query,params).fetchall()

    conn.close()

    return [dict(r) for r in rows]

@router.get("/{ticker}/ratios")
def ratios(
        ticker:str,
        year:Optional[str]=None
):

    conn=get_connection()

    query="SELECT * FROM financial_ratios WHERE company_id=?"

    params=[ticker]

    if year:
        query+=" AND year=?"
        params.append(year)

    query+=" ORDER BY year"

    rows=conn.execute(query,params).fetchall()

    conn.close()

    return [dict(r) for r in rows]

from fastapi.responses import FileResponse
from fastapi import HTTPException
import os

@router.get("/{ticker}/tearsheet")
def get_tearsheet(ticker: str):

    path = f"reports/tearsheets/{ticker}_tearsheet.pdf"

    if not os.path.exists(path):
        raise HTTPException(
            status_code=404,
            detail="Tearsheet not found"
        )

    return FileResponse(
        path=path,
        media_type="application/pdf",
        filename=f"{ticker}_tearsheet.pdf"
    )

@router.get("/{ticker}/peers/compare")
def compare_with_peers(ticker: str):

    conn = get_connection()

    # Company ka peer group
    peer = conn.execute("""
        SELECT peer_group_name
        FROM peer_groups
        WHERE company_id = ?
    """, (ticker,)).fetchone()

    if not peer:
        conn.close()
        raise HTTPException(status_code=404, detail="Peer group not found")

    group = peer["peer_group_name"]

    # Company metrics (latest year)
    company = conn.execute("""
        SELECT
            return_on_equity_pct,
            debt_to_equity,
            net_profit_margin_pct,
            operating_profit_margin_pct,
            free_cash_flow_cr
        FROM financial_ratios
        WHERE company_id = ?
        ORDER BY CAST(SUBSTR(year,5) AS INTEGER) DESC
        LIMIT 1
    """, (ticker,)).fetchone()

    # Peer average
    peer_avg = conn.execute("""
        SELECT
            AVG(fr.return_on_equity_pct) AS roe,
            AVG(fr.debt_to_equity) AS de,
            AVG(fr.net_profit_margin_pct) AS npm,
            AVG(fr.operating_profit_margin_pct) AS opm,
            AVG(fr.free_cash_flow_cr) AS fcf
        FROM financial_ratios fr
        JOIN peer_groups pg
            ON fr.company_id = pg.company_id
        WHERE LOWER(pg.peer_group_name)=LOWER(?)
        AND CAST(SUBSTR(fr.year,5) AS INTEGER)=(
            SELECT MAX(CAST(SUBSTR(f2.year,5) AS INTEGER))
            FROM financial_ratios f2
            WHERE f2.company_id=fr.company_id
        )
    """, (group,)).fetchone()

    # Benchmark company
    benchmark = conn.execute("""
        SELECT
            c.id,
            c.company_name
        FROM peer_groups pg
        JOIN companies c
            ON pg.company_id=c.id
        WHERE LOWER(pg.peer_group_name)=LOWER(?)
        AND pg.is_benchmark=1
    """, (group,)).fetchone()

    conn.close()

    return {
        "company": dict(company) if company else {},
        "peer_average": dict(peer_avg) if peer_avg else {},
        "benchmark": dict(benchmark) if benchmark else {}
    }



@router.get("/{ticker}/documents")
def company_documents(ticker: str):

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            year,
            annual_report
        FROM documents
        WHERE company_id=?
        ORDER BY year DESC
    """,(ticker,)).fetchall()

    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="Documents not found")

    return [
        {
            "year": r["year"],
            "annual_report": r["annual_report"],
            "is_url_valid": (
                r["annual_report"].startswith("http")
                if r["annual_report"] else False
            )
        }
        for r in rows
        ]