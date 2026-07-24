from fastapi import APIRouter, HTTPException
from statistics import median
from src.api.database import get_connection

router = APIRouter(prefix="/api/v1/sectors", tags=["Sectors"])


@router.get("")
def get_sectors():

    conn = get_connection()

    sectors = conn.execute("""
        SELECT DISTINCT broad_sector
        FROM sectors
        ORDER BY broad_sector
    """).fetchall()

    result = []

    for s in sectors:

        sector = s["broad_sector"]

        rows = conn.execute("""
            SELECT
                fr.return_on_equity_pct,
                fr.debt_to_equity
            FROM financial_ratios fr
            JOIN sectors sec
                ON fr.company_id = sec.company_id
            WHERE sec.broad_sector = ?
            AND fr.year = (
                SELECT MAX(year)
                FROM financial_ratios
            )
        """, (sector,)).fetchall()

        roe = [r["return_on_equity_pct"] for r in rows if r["return_on_equity_pct"] is not None]
        de = [r["debt_to_equity"] for r in rows if r["debt_to_equity"] is not None]

        count = conn.execute("""
            SELECT COUNT(*)
            FROM sectors
            WHERE broad_sector = ?
        """, (sector,)).fetchone()[0]

        result.append({
            "sector": sector,
            "company_count": count,
            "median_roe": round(median(roe), 2) if roe else None,
            "median_de": round(median(de), 2) if de else None,
            "median_pe": None
        })

    conn.close()

    return result

@router.get("/{sector}/companies")
def sector_companies(sector: str):

    conn = get_connection()

    exists = conn.execute("""
        SELECT 1
        FROM sectors
        WHERE LOWER(broad_sector)=LOWER(?)
        LIMIT 1
    """,(sector,)).fetchone()

    if not exists:
        conn.close()
        raise HTTPException(status_code=404,detail="Sector not found")

    rows = conn.execute("""
        SELECT

            c.id,
            c.company_name,

            fr.return_on_equity_pct,
            fr.debt_to_equity,
            fr.free_cash_flow_cr,
            fr.net_profit_margin_pct,
            fr.operating_profit_margin_pct

        FROM companies c

        JOIN sectors s
            ON c.id=s.company_id

        LEFT JOIN financial_ratios fr
            ON c.id=fr.company_id

        WHERE
            LOWER(s.broad_sector)=LOWER(?)
            AND fr.year=(
                SELECT MAX(year)
                FROM financial_ratios
            )

        ORDER BY c.company_name

    """,(sector,)).fetchall()

    conn.close()

    return [dict(r) for r in rows]