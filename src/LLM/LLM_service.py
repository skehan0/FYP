from src.alphaVantage.services.stock_services import fetch_all_stock_data
from pymongo import MongoClient
from datetime import datetime
import requests
import json

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client.stock_analysis

def perform_analysis(stock_data):
    """
    Perform analysis on the stock data.
    """
    prompt = f"""
    Analyze the following stock data:

    Metadata: {stock_data['metadata']}
    Historical Data: {stock_data['historical_data'] or 'No historical data available'}
    News: {stock_data['news'] or 'No news data available'}
    Income Statement: {stock_data['income_statement'] or 'No income statement data available'}
    Balance Sheet: {stock_data['balance_sheet'] or 'No balance sheet data available'}
    Cash Flow: {stock_data['cash_flow'] or 'No cash flow data available'}
    Earnings: {stock_data['earnings'] or 'No earnings data available'}
    SMA: {stock_data['sma'] or 'No SMA data available'}
    EMA: {stock_data['ema'] or 'No EMA data available'}

    This is a preliminary analysis. Please consult a financial advisor for investment decisions.
    """
    return analysis

def send_prompt_to_llm(prompt, model="mistral"):
    """
    Send the formatted prompt to the LLM and return the response.
    """
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, json=payload, stream=True)

        if response.status_code == 200:
            llm_response = ""
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        json_data = json.loads(line)
                        if "message" in json_data and "content" in json_data["message"]:
                            llm_response += json_data["message"]["content"]
                    except json.JSONDecodeError:
                        raise ValueError(f"Failed to parse line: {line}")
            return llm_response
        else:
            raise RuntimeError(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        raise RuntimeError(f"Failed to send prompt to LLM: {str(e)}")

async def fetch_and_analyze_all_stock_data(ticker: str):
    """
    Fetch all stock data, analyze it, and send it to the LLM.
    """
    try:
        stock_data = await fetch_all_stock_data(ticker)

        if not stock_data or "metadata" not in stock_data:
            raise ValueError(f"Failed to fetch stock data for ticker: {ticker}")

        analysis = perform_analysis(stock_data["metadata"])

        prompt = f"""
        Analyze the following stock data for {ticker}:

        Metadata: {stock_data['metadata']}
        Historical Data: {stock_data['historical_data']}
        News: {stock_data['news']}
        Income Statement: {stock_data['income_statement']}
        Balance Sheet: {stock_data['balance_sheet']}
        Cash Flow: {stock_data['cash_flow']}
        Earnings: {stock_data['earnings']}
        SMA: {stock_data['sma']}
        EMA: {stock_data['ema']}
        """

        llm_response = send_prompt_to_llm(prompt)

        return {
            "symbol": ticker,
            "analysis": analysis,
            "llm_response": llm_response,
            "stock_data": stock_data
        }
    except Exception as e:
        raise RuntimeError(f"Error in fetch_and_analyze_all_stock_data: {str(e)}")

def store_analysis(symbol, analysis):
    """
    Store the analysis in the database.
    """
    db.analyses.insert_one({
        "symbol": symbol,
        "analysis": analysis,
        "timestamp": datetime.now()
    })