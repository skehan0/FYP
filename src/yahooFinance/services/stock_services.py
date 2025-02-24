import yfinance as yf
from fastapi import HTTPException

def fetch_stock_metadata(ticker: str):
    """
    Fetches metadata for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        dict: A dictionary containing various metadata about the stock, including:
            - industry (str): The industry of the company.
            - market_cap (int): The market capitalization of the company.
            - dividend_yield (float): The dividend yield of the company.
            - pe_ratio (float): The price-to-earnings ratio of the company.
            - eps (float): The earnings per share of the company.
            - beta (float): The beta value of the company.
            - 52_week_high (float): The 52-week high price of the stock.
            - 52_week_low (float): The 52-week low price of the stock.
            - current_price (float): The current price of the stock.
            - analyst_ratings (float): The average analyst rating for the stock.

    Raises:
        HTTPException: If there is an error fetching the stock data.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "eps": info.get("trailingEps", "N/A"),
            "beta": info.get("beta", "N/A"),
            "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
            "current_price": info.get("currentPrice", "N/A"),
            "analyst_ratings": info.get("recommendationMean", "N/A"),
            "price_targets": info.get("targetMeanPrice", "N/A"),
            "events": info.get("earningsQuarterlyGrowth", "N/A"),
            f"about_{ticker}": info.get("longBusinessSummary", "N/A"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stock metadata: {str(e)}")

VALID_PERIODS = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']

def fetch_historical_data(ticker: str, period: str):
    """
    Fetch historical stock data for a given ticker and period.

    Args:
        ticker (str): The stock ticker symbol.
        period (str): The period for which to fetch historical data (e.g., '1d', '5d', '1mo', '1y').

    Returns:
        dict: A dictionary containing the columns and rows of the historical stock data.

    Raises:
        HTTPException: If the period is invalid or there is an error fetching the data.
    """
    if period not in VALID_PERIODS:
        raise HTTPException(status_code=400, detail=f"Period '{period}' is invalid, must be one of {VALID_PERIODS}")

    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        data.reset_index(inplace=True)
        columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
        rows = data[columns].to_dict(orient="records")
        return {
            "columns": columns,
            "rows": rows
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching historical data: {str(e)}")

# fetch the cleaned news information
def fetch_news_headlines(ticker: str, limit: int = 8):
    """
    Fetch the latest news headlines for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.
        limit (int): The maximum number of news headlines to fetch. Default is 8.

    Returns:
        list: A list of dictionaries containing news headlines and their details.
    """
    try:
        stock = yf.Ticker(ticker)
        news = stock.news
        ticker_title = stock.info.get("longName", ticker)
        cleaned_news = []
        for index, item in enumerate (news[:limit], start=1):
            content = item.get("content")
            if content is not None:
                title = content.get("title", "N/A")
                summary = content.get("summary", "N/A")
                pubDate = content.get("pubDate", "N/A")
                canonicalUrl = content.get("canonicalUrl", {}).get("url", "N/A")
                cleaned_news.append({
                    "article": index,
                    "title": title,
                    "summary": summary,
                    "pubDate": pubDate,
                    "url": canonicalUrl
                })
        return {
            "company": ticker_title,
            "news": cleaned_news
        }
    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Missing key in news data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news headlines: {str(e)}")
    
    
# def fetch_sma(ticker: str, period: str, window: int):
#     """
#     Fetch Simple Moving Average (SMA) for a given stock ticker and period.

#     Args:
#         ticker (str): The stock ticker symbol.
#         period (str): The period for which to fetch historical data (e.g., '1mo', '1y').
#         window (int): The window size for the SMA calculation.

#     Returns:
#         dict: A dictionary containing the dates and SMA values.

#     Raises:
#         HTTPException: If there is an error fetching the data.
#     """
#     try:
#         stock = yf.Ticker(ticker)
#         data = stock.history(period=period)
#         data['SMA'] = data['Close'].rolling(window=window).mean()
#         data.reset_index(inplace=True)
#         sma_data = data[['Date', 'SMA']].dropna().to_dict(orient='records')
#         return {
#             "ticker": ticker,
#             "period": period,
#             "window": window,
#             "sma": sma_data
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching SMA data: {str(e)}")

# def fetch_ema(ticker: str, period: str, window: int):
#     """
#     Fetch Exponential Moving Average (EMA) for a given stock ticker and period.

#     Args:
#         ticker (str): The stock ticker symbol.
#         period (str): The period for which to fetch historical data (e.g., '1mo', '1y').
#         window (int): The window size for the EMA calculation.

#     Returns:
#         dict: A dictionary containing the dates and EMA values.

#     Raises:
#         HTTPException: If there is an error fetching the data.
#     """
#     try:
#         stock = yf.Ticker(ticker)
#         data = stock.history(period=period)
#         data['EMA'] = data['Close'].ewm(span=window, adjust=False).mean()
#         data.reset_index(inplace=True)
#         ema_data = data[['Date', 'EMA']].dropna().to_dict(orient='records')
#         return {
#             "ticker": ticker,
#             "period": period,
#             "window": window,
#             "ema": ema_data
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching EMA data: {str(e)}")