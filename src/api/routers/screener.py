from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter(prefix="/screener", tags=["Screener"])


@router.get("/")
def screener():
    conn = get_connection()

    query = """
    SELECT
        c.id,
        c.company_name,
        s.broad_sector,
        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.net_profit_margin_pct,
        fr.operating_profit_margin_pct
    FROM companies c
    LEFT JOIN sectors s
        ON c.id = s.company_id
    LEFT JOIN financial_ratios fr
        ON c.id = fr.company_id
    WHERE fr.year = (
        SELECT MAX(year)
        FROM financial_ratios
    )
    ORDER BY c.company_name;
    """

    cursor = conn.execute(query)

    data = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return data