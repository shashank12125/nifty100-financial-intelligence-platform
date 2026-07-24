from fastapi import FastAPI
from src.api.routers import (
    health,
    companies,
    sectors,
    screener,
    peers,
    portfolio,
    valuation
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


@app.get("/")
def root():
    return {
        "message": "Welcome to Nifty100 Financial Intelligence API"
    }