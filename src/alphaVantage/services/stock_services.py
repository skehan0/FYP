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

# Helper function for API requests
async def make_request(url: str):
    """Handles API requests and rate limit errors."""
    response = requests.get(url)
    if response.status_code == 429:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from Alpha Vantage.")
    return response.json()

async def fetch_stock_metadata(ticker: str):
    if ticker in metadata_cache:
        return metadata_cache[ticker]
    
    # Check if metadata is already stored in the database
    existing_metadata = await db.stock_metadata.find_one({"ticker": ticker})
    if existing_metadata:
        existing_metadata["_id"] = str(existing_metadata["_id"])
        return existing_metadata

    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={API_KEY}"
    data = await make_request(url)

    metadata = {
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
    }

    # Store in MongoDB
    result = await db.stock_metadata.insert_one(metadata)
    metadata["_id"] = str(result.inserted_id)

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
            "historical_data": cleaned_data
        }

        # Store in MongoDB
        result = await db.historical_data.insert_one(historical_data)
        historical_data["_id"] = str(result.inserted_id)

        # Update cache
        historical_data_cache[ticker] = historical_data

        return historical_data

    except Exception as e:
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