import yfinance as yf
from fastapi import HTTPException

def fetch_stock_metadata(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "name": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "beta": info.get("beta", "N/A"),
            "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
            "current_price": info.get("currentPrice", "N/A"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stock metadata: {str(e)}")

def fetch_historical_data(ticker: str, period: str):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        data.reset_index(inplace=True)
        return data[["Date", "Open", "High", "Low", "Close", "Volume"]].to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching historical data: {str(e)}")

def fetch_news_headlines(ticker: str):
    # Mocked news. Replace this with actual API logic or scraping.
    news = [
        {"headline": f"{ticker} hits a new high!", "url": "https://example.com/news1"},
        {"headline": f"Analyst upgrade on {ticker}", "url": "https://example.com/news2"},
    ]
    return news