from fastapi import APIRouter, HTTPException
from src.yahooFinance.services.stock_services import (
    fetch_stock_metadata,
    fetch_historical_data,
    fetch_news_headlines,
)

router = APIRouter()

@router.get("/stocks/{ticker}")
async def get_stock_details(ticker: str):
    """
    Endpoint to retrieve stock details for a given ticker.
    """
    try:
        metadata = fetch_stock_metadata(ticker)
        historical_data = {
            "1d": fetch_historical_data(ticker, "1d"),
            "1w": fetch_historical_data(ticker, "7d"),
            "1m": fetch_historical_data(ticker, "1mo"),
            "1y": fetch_historical_data(ticker, "1y"),
            "5y": fetch_historical_data(ticker, "5y"),
        }
        news = fetch_news_headlines(ticker)

        return {
            "ticker": ticker.upper(),
            "metadata": metadata,
            "charts": historical_data,
            "news": news,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stock details: {str(e)}")