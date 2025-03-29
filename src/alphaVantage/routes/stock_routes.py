from fastapi import APIRouter, HTTPException, Query
from src.alphaVantage.services.stock_services import (
    fetch_stock_metadata,
    fetch_historical_data,
    fetch_news_headlines,
    fetch_income_statement,
    fetch_balance_sheet,
    fetch_cash_flow,
    fetch_earnings,
    fetch_SMA,
    fetch_EMA,
    fetch_live_market_prices,
    fetch_all_stock_data,
    fetch_top_gainers_losers
)
from src.LLM.LLM_service import fetch_and_analyze_all_stock_data
from src.mongoDB.database import database 

router = APIRouter()

# Main Endpoint
@router.get("/analyze_all")
async def analyze_all_stock_data(ticker: str = Query(..., description="Stock ticker to analyze")):
    """
    Endpoint to fetch all stock data, analyze it, and send it to the LLM.
    """
    try:
        # Call the service function to fetch, analyze, and send data to the LLM
        result = await fetch_and_analyze_all_stock_data(ticker)

        # Return the result
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metadata/{ticker}")
async def get_stock_metadata(ticker: str):
    return await fetch_stock_metadata(ticker)

@router.get("/historical/{ticker}")
async def get_historical_data(ticker: str):
    return await fetch_historical_data(ticker)

@router.get("/news/{ticker}")
async def get_news_headlines(ticker: str, limit: int = Query(8, description="Number of news items to return")):
    return await fetch_news_headlines(ticker, limit)

@router.get("/income/{ticker}")
async def get_income_statement(ticker: str, limit: int = Query(5, description="Number of years and quarters to return")):
    return await fetch_income_statement(ticker, limit)

@router.get("/balance/{ticker}")
async def get_balance_sheet(ticker: str,  limit: int = Query(5, description="Number of years and quarters to return")):
    return await fetch_balance_sheet(ticker)

@router.get("/cashflow/{ticker}")
async def get_cash_flow(ticker: str, limit: int = Query(5, description="Number of years and quarters to return")):
    return await fetch_cash_flow(ticker)

@router.get("/earnings/{ticker}")
async def get_earnings(ticker: str, limit: int = Query(5, description="Number of years and quarters to return")):
    return await fetch_earnings(ticker)

@router.get("/live-market-prices")
async def get_live_market_prices():
    try:
        data = await fetch_live_market_prices()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sma/{ticker}")
async def get_SMA(ticker: str):
    return await fetch_SMA(ticker)

@router.get("/ema/{ticker}")
async def get_EMA(ticker: str):
    return await fetch_EMA(ticker)

@router.get("/all-stock-data/{ticker}")
async def get_all_stock_data(ticker: str):
    return await fetch_all_stock_data(ticker)

@router.get("/top-gainers-losers")
async def get_top_gainers_losers(limit: int = Query(5, description="Number of gainers and losers to return")):
    return await fetch_top_gainers_losers(limit)

@router.get("/status")
async def check_db_status():
    try:
        db = await database.get_db()
        collections = await db.list_collection_names()
        return {"status": "Connected successfully!", "collections": collections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")