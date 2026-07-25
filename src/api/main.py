from fastapi import FastAPI

from src.api.routers import (
    companies,
    health,
    market_cap,
    peers,
    portfolio,
    screener,
    sectors,
    valuation,
)

app = FastAPI(
    title="Nifty100 Financial Intelligence API",
    version="1.0.0"
)

app.include_router(health.router)
app.include_router(companies.router)
app.include_router(sectors.router)
app.include_router(screener.router)
app.include_router(peers.router)
app.include_router(portfolio.router)
app.include_router(valuation.router)
app.include_router(market_cap.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Nifty100 Financial Intelligence API"
    }