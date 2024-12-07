import yfinance as yf
import pandas as pd

# Function to fetch historical stock data for multiple tickers
def fetch_historical_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker')
    return data

# Function to fetch the Price-to-Earnings ratio for a given ticker
def fetch_pe_ratio(ticker):
    ticker_object = yf.Ticker(ticker)
    pe_ratio = ticker_object.info.get('forwardPE', 'N/A')  # Use .get to avoid key errors
    return pe_ratio

# Function to fetch the Dividend Rate for a given ticker
def fetch_dividend_rate(ticker):
    ticker_object = yf.Ticker(ticker)
    dividend_rate = ticker_object.info.get('dividendRate', 'N/A')
    return dividend_rate

# Function to fetch the Dividends for a given ticker
def fetch_dividends(ticker):
    ticker_object = yf.Ticker(ticker)
    dividends = ticker_object.dividends
    return dividends

# Function to fetch detailed info for multiple tickers and return it as a DataFrame
def fetch_ticker_info(tickers):
    tickers_data = {}  # Empty dictionary to store data

    for ticker in tickers:
        ticker_object = yf.Ticker(ticker)

        # Convert info() output from dictionary to DataFrame
        temp = pd.DataFrame.from_dict(ticker_object.info, orient="index").reset_index()
        temp.columns = ["Attribute", "Recent"]

        # Add (ticker, DataFrame) to main dictionary
        tickers_data[ticker] = temp

    # Combine data for all tickers into a single DataFrame
    combined_data = pd.concat(tickers_data, axis=0)
    combined_data = combined_data.reset_index(drop=True)
    return combined_data

# Example usage of the functions
if __name__ == "__main__":
    # Historical data for multiple tickers
    tickers = ["AMZN", "AAPL", "GOOG"]
    historical_data = fetch_historical_data(tickers, start_date="2017-01-01", end_date="2017-04-30")
    print("Historical Data for AMZN, AAPL, and GOOG:\n", historical_data)

    # Price-to-Earnings ratio for AAPL
    pe_ratio = fetch_pe_ratio("AAPL")
    print(f"\nPrice to Earnings Ratio for AAPL: {pe_ratio}")

    # Dividend Rate for AAPL
    dividend_rate = fetch_dividend_rate("AAPL")
    print(f"Dividend Rate for AAPL: {dividend_rate}")

    # Dividends for AAPL
    dividends = fetch_dividends("AAPL")
    print(f"Dividends for AAPL:\n{dividends}")

    # Fetch detailed info for multiple tickers
    tickers_list = ["AAPL", "GOOG", "AMZN", "BAC", "BA"]
    combined_data = fetch_ticker_info(tickers_list)
    print("\nCombined Data for all tickers:\n", combined_data)