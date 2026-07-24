from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter(prefix="/valuation", tags=["Valuation"])


@router.get("/{company_id}")
def valuation(company_id: str):
    conn = get_connection()

    cursor = conn.execute("""
        SELECT *
        FROM analysis
        WHERE company_id = ?
    """, (company_id,))

    data = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return data