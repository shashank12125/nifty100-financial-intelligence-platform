from fastapi import APIRouter, HTTPException
from src.api.database import get_connection

router = APIRouter(prefix="/api/v1/peers", tags=["Peers"])


@router.get("/{group_name}")
def peer_group(group_name: str):

    conn = get_connection()

    exists = conn.execute("""
        SELECT 1
        FROM peer_groups
        WHERE LOWER(peer_group_name)=LOWER(?)
        LIMIT 1
    """,(group_name,)).fetchone()

    if not exists:
        conn.close()
        raise HTTPException(status_code=404, detail="Peer group not found")

    rows = conn.execute("""
        SELECT

            c.id,
            c.company_name,

            pg.is_benchmark,

            fr.return_on_equity_pct,
            fr.debt_to_equity,
            fr.net_profit_margin_pct,
            fr.operating_profit_margin_pct,
            fr.free_cash_flow_cr

        FROM peer_groups pg

        JOIN companies c
            ON pg.company_id=c.id

        LEFT JOIN financial_ratios fr
            ON c.id = fr.company_id
            AND CAST(SUBSTR(fr.year,5) AS INTEGER) = (
                SELECT MAX(CAST(SUBSTR(f2.year,5) AS INTEGER))
                FROM financial_ratios f2
                WHERE f2.company_id = c.id
            )

        WHERE
            LOWER(pg.peer_group_name)=LOWER(?)
          

        ORDER BY
            pg.is_benchmark DESC,
            c.company_name

    """,(group_name,)).fetchall()

    conn.close()

    return [dict(r) for r in rows]