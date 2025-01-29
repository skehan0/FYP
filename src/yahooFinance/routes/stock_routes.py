from fastapi import APIRouter, HTTPException, Query
from src.yahooFinance.services.stock_services import (
    fetch_stock_metadata,
    fetch_historical_data,
    fetch_news_headlines,
)

router = APIRouter()

@router.get("/metadata/{ticker}")
async def get_stock_metadata(ticker: str):
    return fetch_stock_metadata(ticker)

@router.get("/historical/{ticker}")
async def get_historical_data(ticker: str, period: str = "1mo"):
    return fetch_historical_data(ticker, period)

@router.get("/news/{ticker}")
async def get_news_headlines(ticker: str, limit: int = Query(8, description="Number of news items to return")):
    return fetch_news_headlines(ticker, limit)