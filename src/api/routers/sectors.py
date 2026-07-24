from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter(prefix="/sectors", tags=["Sectors"])


@router.get("/")
def get_sectors():
    conn = get_connection()

    cursor = conn.execute("""
        SELECT
            company_id,
            broad_sector,
            sub_sector,
            market_cap_category,
            index_weight_pct
        FROM sectors
        ORDER BY broad_sector, company_id
    """)

    sectors = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return sectors