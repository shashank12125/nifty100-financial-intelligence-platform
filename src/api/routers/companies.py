from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.get("/")
def get_companies():
    conn = get_connection()

    cursor = conn.execute("""
        SELECT
            id,
            company_name,
            website
        FROM companies
        ORDER BY company_name
    """)

    companies = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return companies