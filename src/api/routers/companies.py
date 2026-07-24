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
def company_profile(ticker:str):

    conn=get_connection()

    row=conn.execute("""

    SELECT
        c.*,
        s.*,
        fr.*
    FROM companies c
    LEFT JOIN sectors s
        ON c.id=s.company_id
    LEFT JOIN financial_ratios fr
        ON c.id=fr.company_id
    WHERE
        c.id=?
    AND
        fr.year=(SELECT MAX(year) FROM financial_ratios)

    """,(ticker,)).fetchone()

    conn.close()

    if row is None:
        raise HTTPException(status_code=404,detail="Company not found")

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