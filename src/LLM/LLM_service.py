from src.alphaVantage.services.stock_services import fetch_all_stock_data, fetch_income_statement
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
    analysis = f"""
    Analyze the following stock data:

    Metadata: {stock_data}
    
    This is a preliminary analysis. Please consult a financial advisor for investment decisions.
    """
    
    # Limit data
    """
    Historical Data: {stock_data['historical_data'] or 'No historical data available'}
    Income Statement: {stock_data['income_statement'] or 'No income statement data available'}
    Balance Sheet: {stock_data['balance_sheet'] or 'No balance sheet data available'}
    News: {stock_data['news'] or 'No news data available'}
    Cash Flow: {stock_data['cash_flow'] or 'No cash flow data available'}
    Earnings: {stock_data['earnings'] or 'No earnings data available'}
    SMA: {stock_data['sma'] or 'No SMA data available'}
    EMA: {stock_data['ema'] or 'No EMA data available'}
    """
    return analysis

def send_prompt_to_llm(prompt, model="gemma3:4b"):
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
    
def send_to_deepseek(llm_response, model='deepseek-r1:7b'):
    """
    Send the LLM response to the DeepThinking model for final analysis.
    """
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": "As a financial advicer with years of experience with stock markets, please perform a deeper analysis based on the following response, keep it short and to the point:"},
            {"role": "user", "content": llm_response}]
    }
    
    # Optionally include stock data in the prompt
    # if stock_data:
    #     payload["messages"].insert(0, {"role": "user", "content": f"Stock Data: {stock_data}"})
    
    try:
        response = requests.post(url, json=payload, stream=True)
        
        if response.status_code == 200:
            deepthinking_response = ""
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        json_data = json.loads(line)
                        if "message" in json_data and "content" in json_data["message"]:
                            deepthinking_response += json_data["message"]["content"]
                    except json.JSONDecodeError:
                        raise ValueError(f"Failed to parse line: {line}")
            return deepthinking_response
        else:
            raise RuntimeError(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        raise RuntimeError(f"Failed to send data to DeepThinking model: {str(e)}")                   

def store_analysis(symbol, analysis):
    """
    Store the analysis in the database.
    """
    db.analyses.insert_one({
        "symbol": symbol,
        "analysis": analysis,
        "timestamp": datetime.now()
    })


async def fetch_and_analyze_all_stock_data(ticker: str):
    try:
        stock_data = await fetch_all_stock_data(ticker)
        print("Debug: Fetched stock data:", stock_data)

        if not stock_data:
            raise ValueError(f"Stock data is empty or None for ticker: {ticker}")

        if "metadata" not in stock_data:
            raise KeyError(f"'metadata' key missing in stock data: {stock_data}")

        metadata = stock_data["metadata"]
        print("Debug: Metadata:", metadata)

        analysis = perform_analysis(metadata)
        print("Debug: Analysis result:", analysis)

        prompt = f"""
        Analyze the following stock data:

        Metadata: {metadata}
        """
        print("Debug: Prompt for LLM:", prompt)

        llm_response = send_prompt_to_llm(prompt)
        print("Debug: LLM response:", llm_response)

        deepthinking_response = send_to_deepseek(llm_response)
        print("Debug: DeepThinking response:", deepthinking_response)

        return {
            "symbol": ticker,
            "analysis": analysis,
            "llm_response": llm_response,
            "deepthinking_response": deepthinking_response,
            "stock_data": stock_data
        }
    except Exception as e:
        print(f"Debug: Exception occurred: {e}")
        raise RuntimeError(f"Error in fetch_and_analyze_all_stock_data: {str(e)}")