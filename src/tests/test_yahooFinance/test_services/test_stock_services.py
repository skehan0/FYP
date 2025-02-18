from src.yahooFinance.services.stock_services import (
    fetch_stock_metadata,
    fetch_historical_data,
    fetch_news_headlines,
)

def test_fetch_stock_metadata():
    """
    Test fetching stock metadata.
    """
    result = fetch_stock_metadata("AAPL")  # Replace "AAPL" with any valid ticker
    assert "name" in result
    assert "sector" in result
    assert "current_price" in result

def test_fetch_historical_data():
    """
    Test fetching historical stock data.
    """
    result = fetch_historical_data("AAPL", "1mo")
    assert isinstance(result, list)
    assert len(result) > 0
    assert "Date" in result[0]
    assert "Open" in result[0]

def test_fetch_news_headlines():
    """
    Test fetching stock-related news headlines.
    """
    result = fetch_news_headlines("AAPL")
    assert isinstance(result, list)
    assert len(result) > 0
    assert "headline" in result[0]
    assert "url" in result[0]