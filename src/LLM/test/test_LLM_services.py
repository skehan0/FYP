import asyncio
from src.alphaVantage.services.stock_services import fetch_all_stock_data
from src.LLM.LLM_service import perform_analysis, fetch_and_analyze_all_stock_data, send_prompt_to_llm, send_to_deepseek

async def test_fetch_all_stock_data():
    ticker = "AAPL"
    stock_data = await fetch_all_stock_data(ticker)
    print(stock_data)

asyncio.run(test_fetch_all_stock_data())

def test_perform_analysis():
    metadata = {
        "ticker": "AAPL",
        "industry": "ELECTRONIC COMPUTERS",
        "market_cap": "3278873821000",
        "dividend_yield": "0.0046",
        "pe_ratio": "34.59",
        "eps": "6.31",
        "beta": "1.178",
        "52_week_high": "259.81",
        "52_week_low": "163.31",
        "current_price": "231.92",
        "analyst_ratings": "252.59",
    }
    analysis = perform_analysis({"metadata": metadata})
    print(analysis)

def test_send_prompt_to_llm():
    prompt = """
    Analyze the following stock data:

    Metadata: {
        "ticker": "AAPL",
        "industry": "ELECTRONIC COMPUTERS",
        "market_cap": "3278873821000",
        "dividend_yield": "0.0046",
        "pe_ratio": "34.59",
        "eps": "6.31",
        "beta": "1.178",
        "52_week_high": "259.81",
        "52_week_low": "163.31",
        "current_price": "231.92",
        "analyst_ratings": "252.59"
    }
    """
    response = send_prompt_to_llm(prompt)
    print(response)

def test_send_to_deepseek():
    # Mock LLM response
    llm_response = """
    Okay, let's analyze the provided stock data for Apple (AAPL) based on the given metadata. Here's a breakdown of the key observations and potential interpretations:

    **Overall Impression:**
    Apple (AAPL) presents a mixed picture. It's a large, established company with a strong market capitalization, but the valuation metrics suggest it's currently trading at a premium.

    **Detailed Analysis:**
    * **Market Cap ($327.89 Billion):** This is a massive market capitalization, indicating Apple is one of the largest companies globally. It signifies significant market confidence and a substantial presence in the tech sector.
    * **Industry (ELECTRONIC COMPUTERS):** This confirms Apple's core business – designing, developing, and selling consumer electronics, computer software, and related services.
    * **Dividend Yield (0.0046 or 0.46%):** A dividend yield of 0.46% is quite low. Apple historically hasn't been a significant dividend payer, and this reflects that. Investors seeking income would likely find this unattractive.
    * **P/E Ratio (34.59):** This is a *high* P/E ratio. It means investors are paying a significant premium for each dollar of Apple's earnings. This could be due to high growth expectations, strong brand loyalty, or overall market sentiment. A high P/E ratio can also indicate overvaluation.
    * **Earnings Per Share (EPS) ($6.31):** $6.31 is a reasonable EPS figure, but it's important to consider it in conjunction with the P/E ratio.
    * **Beta (1.178):** A beta of 1.178 indicates that Apple's stock price is 17.8% more volatile than the overall market (as represented by the S&P 500). This suggests it's more sensitive to market fluctuations.
    * **52-Week High ($259.81) & 52-Week Low ($163.31):** The stock has traded significantly higher than its recent low, indicating strong upward momentum at some point. The current price ($231.92) is below the 52-week high, suggesting a potential pullback.
    * **Current Price ($231.92):** This price is below the 52-week high, which could be a buying opportunity for some investors.
    * **Analyst Ratings (252.59):** An analyst rating of 252.59 suggests that the majority of analysts covering Apple have a *buy* or *strongly buy* recommendation. This adds to the positive sentiment surrounding the stock.

    **Key Takeaways & Potential Considerations:**
    * **Valuation Concerns:** The high P/E ratio warrants caution. Investors should carefully assess whether Apple's growth prospects justify the premium being paid.
    * **Growth Potential:** Despite the high valuation, Apple continues to innovate and dominate key markets (smartphones, tablets, wearables, services). Future growth is a key factor driving the stock's price.
    * **Market Sentiment:** The strong analyst ratings suggest positive market sentiment, which could continue to support the stock price.
    * **Volatility:** The beta indicates that Apple's stock is more volatile than the market, so investors should be prepared for potential price swings.

    **Disclaimer:** *I am an AI Chatbot and cannot provide financial advice. This analysis is based solely on the provided data and should not be considered a recommendation to buy or sell Apple stock. Investors should conduct their own thorough research and consult with a qualified financial advisor before making any investment decisions.*
    """

    # Call the send_to_deepseek function
    try:
        deepseek_response = send_to_deepseek(llm_response, model="deepseek-r1:7b")
        print("DeepSeek Response:", deepseek_response)
    except Exception as e:
        print(f"Error in send_to_deepseek: {str(e)}")
        
async def test_fetch_and_analyze_all_stock_data():
    ticker = "AAPL"  # Example ticker symbol
    try:
        result = await fetch_and_analyze_all_stock_data(ticker)
        assert "symbol" in result, "Result should contain 'symbol'"
        assert "analysis" in result, "Result should contain 'analysis'"
        assert "llm_response" in result, "Result should contain 'llm_response'"
        assert "deepthinking_response" in result, "Result should contain 'deepthinking_response'"
        assert "stock_data" in result, "Result should contain 'stock_data'"
        print("Test passed. Result:", result)
    except Exception as e:
        print(f"Test failed with exception: {e}")

async def test_fetch_and_analyze():
    ticker = "AAPL"
    try:
        result = await fetch_and_analyze_all_stock_data(ticker)
        print("Debug: Function result:", result)
    except Exception as e:
        print(f"Debug: Exception occurred: {e}")

# Run the async function
if __name__ == "__main__":
    asyncio.run(test_fetch_and_analyze())


        