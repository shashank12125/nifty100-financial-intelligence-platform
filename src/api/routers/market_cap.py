from fastapi import APIRouter, HTTPException

from src.api.database import get_connection

router = APIRouter(prefix="/api/v1/market-cap", tags=["Market Cap"])


def market_cap_history(ticker: str):

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            substr(date,1,4) as year,
            adjusted_close
        FROM stock_prices
        WHERE company_id=?
        AND substr(date,1,4) BETWEEN '2019' AND '2024'
        ORDER BY year
    """,(ticker,)).fetchall()

    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="Company not found")

    return [
        {
            "year": r["year"],
            "pe": None,
            "pb": None,
            "ev_ebitda": None,
            "dividend_yield": None,
            "price": r["adjusted_close"]
        }
        for r in rows
    ]
