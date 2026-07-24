from fastapi import APIRouter, HTTPException
from typing import Optional
from src.api.database import get_connection

router = APIRouter(prefix="/api/v1/screener", tags=["Screener"])


@router.get("")
def screener(
    min_roe: Optional[float] = None,
    max_de: Optional[float] = None,
    min_fcf: Optional[float] = None,
    sector: Optional[str] = None,
    min_rev_cagr_5yr: Optional[float] = None,
    min_pat_cagr_5yr: Optional[float] = None,
    max_pe: Optional[float] = None
):

    if min_roe is not None and min_roe < 0:
        raise HTTPException(status_code=400, detail="Invalid min_roe")

    if max_de is not None and max_de < 0:
        raise HTTPException(status_code=400, detail="Invalid max_de")

    conn = get_connection()

    query = """
    SELECT
        c.id,
        c.company_name,
        s.broad_sector,

        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.free_cash_flow_cr,

        a.compounded_sales_growth,
        a.compounded_profit_growth

    FROM companies c

    LEFT JOIN sectors s
        ON c.id=s.company_id

    LEFT JOIN financial_ratios fr
        ON c.id=fr.company_id

    LEFT JOIN analysis a
        ON c.id=a.company_id

    WHERE
        fr.year=(SELECT MAX(year) FROM financial_ratios)
    """

    params=[]

    if min_roe is not None:
        query+=" AND fr.return_on_equity_pct>=?"
        params.append(min_roe)

    if max_de is not None:
        query+=" AND fr.debt_to_equity<=?"
        params.append(max_de)

    if min_fcf is not None:
        query+=" AND fr.free_cash_flow_cr>=?"
        params.append(min_fcf)

    if sector:
        query+=" AND LOWER(s.broad_sector)=LOWER(?)"
        params.append(sector)

    if min_rev_cagr_5yr is not None:
        query+=" AND a.compounded_sales_growth>=?"
        params.append(min_rev_cagr_5yr)

    if min_pat_cagr_5yr is not None:
        query+=" AND a.compounded_profit_growth>=?"
        params.append(min_pat_cagr_5yr)

    query += """
    ORDER BY
        fr.return_on_equity_pct DESC
    """

    rows = conn.execute(query, params).fetchall()

    conn.close()

    return [dict(r) for r in rows]