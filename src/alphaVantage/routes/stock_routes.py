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
)
from src.mongoDB.database import database 

router = APIRouter()

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

@router.get("/sma/{ticker}")
async def get_SMA(ticker: str):
    return await fetch_SMA(ticker)

@router.get("/ema/{ticker}")
async def get_SMA(ticker: str):
    return await fetch_SMA(ticker)

@router.get("/status")
async def check_db_status():
    try:
        db = await database.get_db()
        collections = await db.list_collection_names()
        return {"status": "Connected successfully!", "collections": collections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")