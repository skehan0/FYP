from alpaca.trading.client import TradingClient
from dotenv import load_dotenv
import os
from alpaca.data import StockHistoryDataClient, StockTradesRequest
from datetime import datetime

# Load environment variables
load_dotenv()

# Fetch API keys from environment variables
api_key = os.getenv('APCA_API_KEY_ID')
secret_key = os.getenv('APCA_API_SECRET_KEY')

# Check if the environment variables are loaded properly
if not api_key or not secret_key:
    raise ValueError("API Key or Secret Key not found in environment variables")

# Initialize the StockHistoryDataClient with the API key and secret key
data_client = StockHistoryDataClient(api_key, secret_key)

# Define the request parameters for stock trades
request_params = StockTradesRequest(
    symbol_or_symbols='AAPL',
    start=datetime(2024, 10, 27, 14, 30),
    end=datetime(2024, 10, 27, 14, 45)
)

# Fetch trades using the data client
trades = data_client.get_trades(request_params)

# Print the retrieved trades
print(trades)
