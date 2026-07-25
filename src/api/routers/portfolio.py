from fastapi import APIRouter

from src.api.database import get_connection

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


@router.get("/stats")
def portfolio_stats():
    conn = get_connection()

    cursor = conn.execute("""
        SELECT *
        FROM portfolio_stats
    """)

    data = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return data