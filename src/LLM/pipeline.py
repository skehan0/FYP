import json
import requests
from pymongo import MongoClient
from datetime import datetime
from src.alphaVantage.services.stock_services import fetch_live_market_data

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client.stock_analysis

# Function to perform analysis
def perform_analysis(stock_data):
    analysis = f"""
    Here's my analysis:

    1. Market Cap: A market cap of ${stock_data['market_cap']} indicates that the company is large and well-established in its industry. The size of the company can provide stability and reduce risk compared to smaller companies.

    2. Dividend Yield: A dividend yield of {stock_data['dividend_yield']}% suggests that there may not be significant income generation from this stock, but it's important to note that Apple has been reinvesting most of its profits to drive growth and innovation in their product lineup.

    3. P/E Ratio: A P/E ratio of {stock_data['pe_ratio']} indicates that the market is pricing the company at a premium compared to other companies in the industry. This could suggest potential for future growth, as investors are willing to pay a higher price now due to optimism about Apple's prospects. However, it's essential to consider this risk when making investment decisions.

    4. EPS: A strong Earnings Per Share (EPS) of {stock_data['eps']} indicates the company is earning substantial profits per share of stock outstanding. This can be a positive sign for long-term investors.

    5. Beta: A beta of {stock_data['beta']} suggests that Apple's stock price is more volatile than the overall market, which means it tends to experience greater price movements in response to market movements. However, this volatility may also offer opportunities for capital gains if you can successfully time your investments or ride out periods of market downturn.

    6. 52 Week High and Low: The range between the 52-week high ({stock_data['52_week_high']}) and low ({stock_data['52_week_low']}) indicates a significant swing in price, which can create opportunities for long-term investors to buy at lower prices during market downturns.

    7. Analyst Ratings and Price Targets: With an average analyst rating of {stock_data['analyst_ratings']} and a price target of {stock_data['price_targets']}, analysts generally view Apple as a strong buy with expectations for future growth. However, it's essential to remember that analyst ratings are not always accurate and should be used as part of your overall analysis.

    8. Events: The absence of notable events suggests that there may not be any immediate catalysts driving the stock price. This could mean a more stable investment environment but also less potential for rapid price movements.

    In conclusion, Apple Inc. (AAPL) appears to have strong fundamentals and growth prospects, making it a suitable candidate for long-term investment. However, investors should be aware of the higher volatility associated with this stock and consider diversifying their portfolio to mitigate risk. As always, it's essential to conduct thorough research and consult with a financial advisor before making any investment decisions.
    """
    return analysis

# Function to store analysis in database
def store_analysis(symbol, analysis):
    db.analyses.insert_one({
        "symbol": symbol,
        "analysis": analysis,
        "timestamp": datetime.now()
    })

# Function to send analysis to AI
def send_analysis_to_ai(analysis):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "deepseek-r1:7b",  # Replace with the model name you're using
        "messages": [{"role": "user", "content": analysis}]
    }
    response = requests.post(url, json=payload, stream=True)
    if response.status_code == 200:
        print("Streaming response from DeepSeek:")
        for line in response.iter_lines(decode_unicode=True):
            if line:  # Ignore empty lines
                try:
                    json_data = json.loads(line)
                    if "message" in json_data and "content" in json_data["message"]:
                        print(json_data["message"]["content"], end="")
                except json.JSONDecodeError:
                    print(f"\nFailed to parse line: {line}")
        print()  # Ensure the final output ends with a newline
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

# Main pipeline function
def main():
    symbol = "AAPL"  # Replace with the desired stock symbol
    stock_data = fetch_live_market_data()
    if symbol in stock_data:
        specific_stock_data = stock_data[symbol]
        specific_stock_data['symbol'] = symbol
        analysis = perform_analysis(specific_stock_data)
        store_analysis(symbol, analysis)
        send_analysis_to_ai(analysis)
    else:
        print(f"Error: No data found for symbol {symbol}")

if __name__ == "__main__":
    main()