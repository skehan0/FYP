import requests
from fastapi import HTTPException
from cachetools import TTLCache
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from alpha_vantage.timeseries import TimeSeries

# Load environment variables from .env file
load_dotenv()

# Load Alpha Vantage API key from environment variable
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
if not API_KEY:
    raise ValueError("Alpha Vantage API key is not set in environment variables.")

# Caches with a TTL of 1 hour and a max size of 100 items
metadata_cache = TTLCache(maxsize=100, ttl=3600)
historical_data_cache = TTLCache(maxsize=100, ttl=3600)
news_cache = TTLCache(maxsize=100, ttl=3600)

# Helper function for API requests
def make_request(url: str):
    """Handles API requests and rate limit errors."""
    response = requests.get(url)
    if response.status_code == 429:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from Alpha Vantage.")
    return response.json()

# Fetch stock metadata
def fetch_stock_metadata(ticker: str):
    if ticker in metadata_cache:
        return metadata_cache[ticker]

    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={API_KEY}"
    data = make_request(url)

    metadata = {
        "industry": data.get("Industry", "N/A"),
        "market_cap": data.get("MarketCapitalization", "N/A"),
        "dividend_yield": data.get("DividendYield", "N/A"),
        "pe_ratio": data.get("PERatio", "N/A"),
        "eps": data.get("EPS", "N/A"),
        "beta": data.get("Beta", "N/A"),
        "52_week_high": data.get("52WeekHigh", "N/A"),
        "52_week_low": data.get("52WeekLow", "N/A"),
        "current_price": data.get("50DayMovingAverage", "N/A"),  # Approximate as Alpha Vantage doesn't provide live prices
        "analyst_ratings": data.get("AnalystTargetPrice", "N/A"),
        "price_targets": data.get("AnalystTargetPrice", "N/A"),
        "events": data.get("QuarterlyEarningsGrowthYOY", "N/A"),
        f"about_{ticker}": data.get("Description", "N/A"),
    }

    metadata_cache[ticker] = metadata
    return metadata

def fetch_historical_data(ticker: str):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={ticker}&apikey={API_KEY}"
        
    ts = TimeSeries(key = API_KEY, output_format='json')
    data = ts.get_weekly_adjusted(ticker)
    
    return data

# Fetch news headlines
def fetch_news_headlines(ticker: str, limit: int = 8):
    cache_key = f"{ticker}_{limit}"
    if cache_key in news_cache:
        return news_cache[cache_key]

    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={API_KEY}"
    news_data = make_request(url).get("feed", [])

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