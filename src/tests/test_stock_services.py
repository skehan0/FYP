# import pytest
# import asyncio
# from unittest.mock import patch, AsyncMock
# from motor.motor_asyncio import AsyncIOMotorClient
# from src.alphaVantage.services.stock_services import fetch_stock_metadata, fetch_historical_data, fetch_news_headlines

# # Mock environment variables
# @pytest.fixture(autouse=True)
# def mock_env_vars(monkeypatch):
#     monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "test_api_key")
#     monkeypatch.setenv("MONGODB_URI", "mongodb://localhost:27017")
#     monkeypatch.setenv("MONGODB_DB_NAME", "test_db")

# # Mock MongoDB client
# @pytest.fixture
# def mock_db():
#     client = AsyncIOMotorClient("mongodb://localhost:27017")
#     db = client.test_db
#     yield db
#     client.drop_database("test_db")

# # Mock API response for stock metadata
# @pytest.fixture
# def mock_api_response_metadata():
#     return {
#         "Industry": "Technology",
#         "MarketCapitalization": "1000000000",
#         "DividendYield": "1.5",
#         "PERatio": "25.0",
#         "EPS": "5.0",
#         "Beta": "1.2",
#         "52WeekHigh": "150.0",
#         "52WeekLow": "100.0",
#         "50DayMovingAverage": "120.0",
#         "AnalystTargetPrice": "130.0",
#         "QuarterlyEarningsGrowthYOY": "10.0",
#         "Description": "Test company description"
#     }

# # Mock API response for historical data
# @pytest.fixture
# def mock_api_response_historical():
#     return {
#         "2022-01-01": {
#             "1. open": "100.0",
#             "2. high": "110.0",
#             "3. low": "90.0",
#             "4. close": "105.0",
#             "5. adjusted close": "105.0",
#             "6. volume": "1000000",
#             "7. dividend amount": "0.5"
#         }
#     }

# # Mock API response for news headlines
# @pytest.fixture
# def mock_api_response_news():
#     return {
#         "feed": [
#             {
#                 "title": "Test News Title",
#                 "summary": "Test News Summary",
#                 "time_published": "2022-01-01T00:00:00Z",
#                 "url": "http://example.com"
#             }
#         ]
#     }

# @pytest.mark.asyncio
# async def test_fetch_stock_metadata_stores_in_db(mock_db, mock_api_response_metadata):
#     ticker = "AAPL"

#     # Mock the make_request function
#     with patch("src.alphaVantage.services.stock_services.make_request", new_callable=AsyncMock) as mock_make_request:
#         mock_make_request.return_value = mock_api_response_metadata

#         # Call the function
#         metadata = await fetch_stock_metadata(ticker)

#         # Check if the data is stored in the database
#         stored_metadata = await mock_db.stock_metadata.find_one({"ticker": ticker})
#         assert stored_metadata is not None
#         assert stored_metadata["ticker"] == ticker
#         assert stored_metadata["industry"] == mock_api_response_metadata["Industry"]

# @pytest.mark.asyncio
# async def test_fetch_stock_metadata_retrieves_from_db(mock_db, mock_api_response_metadata):
#     ticker = "AAPL"

#     # Insert mock data into the database
#     await mock_db.stock_metadata.insert_one({
#         "ticker": ticker,
#         "industry": mock_api_response_metadata["Industry"],
#         "market_cap": mock_api_response_metadata["MarketCapitalization"],
#         "dividend_yield": mock_api_response_metadata["DividendYield"],
#         "pe_ratio": mock_api_response_metadata["PERatio"],
#         "eps": mock_api_response_metadata["EPS"],
#         "beta": mock_api_response_metadata["Beta"],
#         "52_week_high": mock_api_response_metadata["52WeekHigh"],
#         "52_week_low": mock_api_response_metadata["52WeekLow"],
#         "current_price": mock_api_response_metadata["50DayMovingAverage"],
#         "analyst_ratings": mock_api_response_metadata["AnalystTargetPrice"],
#         "price_targets": mock_api_response_metadata["AnalystTargetPrice"],
#         "events": mock_api_response_metadata["QuarterlyEarningsGrowthYOY"],
#         f"about_{ticker}": mock_api_response_metadata["Description"],
#     })

#     # Call the function
#     metadata = await fetch_stock_metadata(ticker)

#     # Check if the data is retrieved from the database
#     assert metadata is not None
#     assert metadata["ticker"] == ticker
#     assert metadata["industry"] == mock_api_response_metadata["Industry"]

# @pytest.mark.asyncio
# async def test_fetch_historical_data_stores_in_db(mock_db, mock_api_response_historical):
#     ticker = "AAPL"

#     # Mock the make_request function
#     with patch("src.alphaVantage.services.stock_services.TimeSeries.get_weekly_adjusted", new_callable=AsyncMock) as mock_get_weekly_adjusted:
#         mock_get_weekly_adjusted.return_value = (mock_api_response_historical, None)

#         # Call the function
#         historical_data = await fetch_historical_data(ticker)

#         # Check if the data is stored in the database
#         stored_historical_data = await mock_db.historical_data.find_one({"ticker": ticker})
#         assert stored_historical_data is not None
#         assert stored_historical_data["ticker"] == ticker
#         assert stored_historical_data["historical_data"][0]["date"] == "2022-01-01"

# @pytest.mark.asyncio
# async def test_fetch_historical_data_retrieves_from_db(mock_db, mock_api_response_historical):
#     ticker = "AAPL"

#     # Insert mock data into the database
#     await mock_db.historical_data.insert_one({
#         "ticker": ticker,
#         "historical_data": [
#             {
#                 "date": "2022-01-01",
#                 "open": "100.0",
#                 "high": "110.0",
#                 "low": "90.0",
#                 "close": "105.0",
#                 "adjusted_close": "105.0",
#                 "volume": "1000000",
#                 "dividend_amount": "0.5"
#             }
#         ]
#     })

#     # Call the function
#     historical_data = await fetch_historical_data(ticker)

#     # Check if the data is retrieved from the database
#     assert historical_data is not None
#     assert historical_data["ticker"] == ticker
#     assert historical_data["historical_data"][0]["date"] == "2022-01-01"

# @pytest.mark.asyncio
# async def test_fetch_news_headlines(mock_api_response_news):
#     ticker = "AAPL"

#     # Mock the make_request function
#     with patch("src.alphaVantage.services.stock_services.make_request", new_callable=AsyncMock) as mock_make_request:
#         mock_make_request.return_value = mock_api_response_news

#         # Call the function
#         news = await fetch_news_headlines(ticker)

#         # Check if the data is correct
#         assert news is not None
#         assert news["company"] == ticker
#         assert news["news"][0]["title"] == "Test News Title"