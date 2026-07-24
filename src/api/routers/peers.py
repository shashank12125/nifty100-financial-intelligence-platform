from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter(prefix="/peers", tags=["Peers"])


@router.get("/{company_id}")
def get_peers(company_id: str):
    conn = get_connection()

    cursor = conn.execute("""
        SELECT broad_sector
        FROM sectors
        WHERE company_id = ?
    """, (company_id,))

    sector = cursor.fetchone()

    if not sector:
        conn.close()
        return {"message": "Company not found"}

    cursor = conn.execute("""
        SELECT
            c.id,
            c.company_name
        FROM companies c
        JOIN sectors s
        ON c.id = s.company_id
        WHERE s.broad_sector = ?
        ORDER BY c.company_name
    """, (sector["broad_sector"],))

    peers = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return peers