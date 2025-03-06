import requests
from fastapi import HTTPException
from cachetools import TTLCache
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from alpha_vantage.timeseries import TimeSeries
from src.alphaVantage.models.stock_models import StockMetadata, StockHistoricalData
from src.mongoDB.database import database
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import logging

# Load environment variables from .env file
load_dotenv()

# Load Alpha Vantage API key from environment variable
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
if not API_KEY:
    raise ValueError("Alpha Vantage API key is not set in environment variables.")

# MongoDB setup
client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
db = client.tradely  # Use the 'tradely' database

# Caches with a TTL of 1 hour and a max size of 100 items
metadata_cache = TTLCache(maxsize=100, ttl=3600)
historical_data_cache = TTLCache(maxsize=100, ttl=3600)
news_cache = TTLCache(maxsize=100, ttl=3600)
income_statement_cache = TTLCache(maxsize=100, ttl=3600)
balance_sheet_cache = TTLCache(maxsize=100, ttl=3600)
cash_flow_cache = TTLCache(maxsize=100, ttl=3600)
earnings_cache = TTLCache(maxsize=100, ttl=3600)
sma_cache = TTLCache(maxsize=100, ttl=3600)
ema_cache = TTLCache(maxsize=100, ttl=3600)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Helper function for API requests with retries
async def make_request(url: str, retries: int = 3, backoff_factor: float = 0.5):
    """Handles API requests and rate limit errors with retries."""
    for attempt in range(retries):
        response = requests.get(url)
        if response.status_code == 429:
            if attempt < retries - 1:
                await asyncio.sleep(backoff_factor * (2 ** attempt))
                continue
            raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from Alpha Vantage.")
        return response.json()
    raise HTTPException(status_code=500, detail="Failed to fetch data after multiple attempts.")

async def fetch_stock_metadata(ticker: str):
    if ticker in metadata_cache:
        return metadata_cache[ticker]
    
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={API_KEY}"
    data = await make_request(url)

    metadata = {
        "ticker": ticker,
        "industry": data.get("Industry", "N/A"),
        "market_cap": data.get("MarketCapitalization", "N/A"),
        "dividend_yield": data.get("DividendYield", "N/A"),
        "pe_ratio": data.get("PERatio", "N/A"),
        "eps": data.get("EPS", "N/A"),
        "beta": data.get("Beta", "N/A"),
        "52_week_high": data.get("52WeekHigh", "N/A"),
        "52_week_low": data.get("52WeekLow", "N/A"),
        "current_price": data.get("50DayMovingAverage", "N/A"),
        "analyst_ratings": data.get("AnalystTargetPrice", "N/A"),
        "price_targets": data.get("AnalystTargetPrice", "N/A"),
        "events": data.get("QuarterlyEarningsGrowthYOY", "N/A"),
        f"about_{ticker}": data.get("Description", "N/A"),
        "last_updated": datetime.utcnow()
    }

    # Store in MongoDB (overwrite existing data)
    await db.stock_metadata.update_one(
        {"ticker": ticker},
        {"$set": metadata},
        upsert=True
    )
    logger.info(f"Stored metadata for {ticker} in database")

    # Update cache
    metadata_cache[ticker] = metadata

    return metadata

async def fetch_historical_data(ticker: str):
    """Fetch weekly historical stock data."""
    if ticker in historical_data_cache:
        return historical_data_cache[ticker]

    # Check if historical data is already stored in the database
    existing_data = await db.historical_data.find_one({"ticker": ticker})
    if existing_data:
        existing_data["_id"] = str(existing_data["_id"])
        return existing_data

    try:
        ts = TimeSeries(key=os.getenv("ALPHA_VANTAGE_API_KEY"), output_format='json')
        data, _ = ts.get_weekly_adjusted(ticker)

        # Extract relevant details (adjust as needed)
        cleaned_data = [
            {
                "date": date,
                "open": values["1. open"],
                "high": values["2. high"],
                "low": values["3. low"],
                "close": values["4. close"],
                "adjusted_close": values["5. adjusted close"],
                "volume": values["6. volume"],
                "dividend_amount": values["7. dividend amount"]
            }
            for date, values in data.items()
        ]

        historical_data = {
            "ticker": ticker,
            "historical_data": cleaned_data,
            "last_updated": datetime.utcnow()
        }

        # Store in MongoDB
        await db.historical_data.update_one(
            {"ticker": ticker},
            {"$set": historical_data},
            upsert=True
        )
        logger.info(f"Stored historical data for {ticker} in database")

        # Update cache
        historical_data_cache[ticker] = historical_data

        return historical_data

    except Exception as e:
        logger.error(f"Failed to fetch historical data for {ticker}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch historical data: {str(e)}")

# Fetch news headlines
async def fetch_news_headlines(ticker: str, limit: int = 8):
    cache_key = f"{ticker}_{limit}"
    if cache_key in news_cache:
        return news_cache[cache_key]

    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={API_KEY}"
    news_data = await make_request(url).get("feed", [])

    cleaned_news = [
        {
            "article": index + 1,
            "title": item.get("title", "N/A"),
            "summary": item.get("summary", "N/A"),
            "pubDate": item.get("time_published", "N/A"),
            "url": item.get("url", "N/A")
        }
        for index, item in enumerate(news_data[:limit])
    ]

    result = {"company": ticker, "news": cleaned_news}
    news_cache[cache_key] = result
    return result

# Fetch Income Statement
async def fetch_income_statement(ticker: str, limit: int = 5):
    cache_key = f"{ticker}_{limit}"
    if cache_key in income_statement_cache:
        return income_statement_cache[cache_key]
    
    # Check if income statement is already stored in the database
    existing_income_statement = await db.income_statement.find_one({"ticker": ticker})
    if existing_income_statement:
        existing_income_statement["_id"] = str(existing_income_statement["_id"])
        return existing_income_statement
    
    url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={API_KEY}"
    data = await make_request(url)

    # Process the data to limit the number of statements
    limited_data = {
        "ticker": ticker,
        "annual_reports": data.get("annualReports", [])[:limit],
        # "quarterly_reports": data.get("quarterlyReports", [])[:limit]
    }

    # Store in MongoDB
    await db.income_statement.update_one(
        {"ticker": ticker},
        {"$set": limited_data},
        upsert=True
    )
    logger.info(f"Stored income statement for {ticker} in database")

    # Cache the result
    income_statement_cache[cache_key] = limited_data

    return limited_data

# Fetch Balance Sheet
async def fetch_balance_sheet(ticker: str, limit: int = 5):
    cache_key = f"{ticker}_{limit}"
    if cache_key in balance_sheet_cache:
        return balance_sheet_cache[cache_key]
    
    # Check if balance sheet is already stored in the database
    existing_balance_sheet = await db.balance_sheet.find_one({"ticker": ticker})
    if existing_balance_sheet:
        existing_balance_sheet["_id"] = str(existing_balance_sheet["_id"])
        return existing_balance_sheet
    
    url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey={API_KEY}"
    data = await make_request(url)

    # Process the data to limit the number of balance sheets
    limited_data = {
        "ticker": ticker,
        "annual_reports": data.get("annualReports", [])[:limit],
        # "quarterly_reports": data.get("quarterlyReports", [])[:limit]
    }

    # Store in MongoDB
    await db.balance_sheet.update_one(
        {"ticker": ticker},
        {"$set": limited_data},
        upsert=True
    )
    logger.info(f"Stored balance sheet for {ticker} in database")

    # Cache the result
    balance_sheet_cache[cache_key] = limited_data

    return limited_data

# Fetch Cash Flow
async def fetch_cash_flow(ticker: str, limit: int = 5):
    cache_key = f"{ticker}_{limit}"
    if cache_key in cash_flow_cache:
        return cash_flow_cache[cache_key]
    
    url = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker}&apikey={API_KEY}"
    data = await make_request(url)
    
    # Check if cash flow is already stored in the database
    existing_cash_flow = await db.cash_flow.find_one({"ticker": ticker})
    if existing_cash_flow:
        existing_cash_flow["_id"] = str(existing_cash_flow["_id"])
        return existing_cash_flow
    
    # Process the data to limit the number of cash flows
    limited_data = {
        "ticker": ticker,
        "annual_reports": data.get("annualReports", [])[:limit],
        # "quarterly_reports": data.get("quarterlyReports", [])[:limit]
    }

    # Store in MongoDB
    await db.cash_flow.update_one(
        {"ticker": ticker},
        {"$set": limited_data},
        upsert=True
    )
    logger.info(f"Stored cash flow for {ticker} in database")

    # Cache the result
    cash_flow_cache[cache_key] = limited_data

    return limited_data

# Fetch Earnings
async def fetch_earnings(ticker: str, limit: int = 5):
    cache_key = f"{ticker}_{limit}"
    if cache_key in earnings_cache:
        return earnings_cache[cache_key]
    
    # Check if earnings are already stored in the database
    existing_earnings = await db.earnings.find_one({"ticker": ticker})
    if existing_earnings:
        existing_earnings["_id"] = str(existing_earnings["_id"])
        return existing_earnings
    
    url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={API_KEY}"
    data = await make_request(url)
    
    # Process the data to limit the number of earnings
    limited_data = {
        "ticker": ticker,
        "annual_reports": data.get("annualReports", [])[:limit],
        # "quarterly_reports": data.get("quarterlyReports", [])[:limit]
    }
    
    # Store in MongoDB
    await db.earnings.update_one(
        {"ticker": ticker},
        {"$set": limited_data},
        upsert=True
    )
    logger.info(f"Stored earnings for {ticker} in database")

    # Cache the result
    earnings_cache[cache_key] = limited_data

    return limited_data

# Fetch SMA
async def fetch_SMA(ticker: str, interval: str = "weekly", time_period: int = 60, series_type: str = "close", limit: int = 12):
    cache_key = f"{ticker}_{limit}"
    if cache_key in sma_cache:
        return sma_cache[cache_key]
    
    url = f"https://www.alphavantage.co/query?function=SMA&symbol={ticker}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={API_KEY}"
    data = await make_request(url)
    sma_data = data.get("Technical Analysis: SMA", {})
    
    # Limit the data to the last 'limit' entries
    limited_sma_data = dict(list(sma_data.items())[:limit])
    
    # Cache the result
    sma_cache[cache_key] = limited_sma_data

    return limited_sma_data

# Fetch EMA
async def fetch_EMA(ticker: str, interval: str = "weekly", time_period: int = 60, series_type: str = "close", limit: int = 12):
    cache_key = f"{ticker}_{limit}"
    if cache_key in ema_cache:
        return ema_cache[cache_key]
    
    url = f"https://www.alphavantage.co/query?function=EMA&symbol={ticker}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={API_KEY}"
    data = await make_request(url)
    ema_data = data.get("Technical Analysis: EMA", {})
    
    # Limit the data to the last 'limit' entries
    limited_ema_data = dict(list(ema_data.items())[:limit])
    
    # Cache the result
    ema_cache[cache_key] = limited_ema_data

    return limited_ema_data