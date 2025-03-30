from fastapi import HTTPException
from src.alphaVantage.services.stock_services import fetch_all_stock_data
from pymongo import MongoClient
from datetime import datetime
import requests
import json
import os
from dotenv import load_dotenv
import httpx
from motor.motor_asyncio import AsyncIOMotorClient
from src.utils.streaming_utils import process_streaming_response
from src.utils.validate_stock_data_utils import validate_stock_data

# Load environment variables from .env file
load_dotenv()

# Define USE_MOCK variable (set to True for testing or False for production)
USE_MOCK = os.getenv("USE_MOCK", "False").lower() == "true"


# MongoDB setup
client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
db = client.tradely

def perform_analysis(stock_data: dict) -> str:
    """
    Perform analysis on the stock data.
    """
    sections = [
        "Metadata", 
        # "Historical Data", "Income Statement", "Balance Sheet", "Cash Flow", "Earnings",
        # "SMA", "EMA",
        # "News"
    ]
    analysis = "if 'N/A' just say 'noooooo':\n\n"
    for section in sections:
        data = stock_data.get(section.lower().replace(" ", "_"), "No data available")
        analysis += f"{section}: {data}\n"
    analysis += "\nThis is a preliminary analysis. Please consult a financial advisor for investment decisions."
    return analysis

async def send_prompt_to_llm(prompt: str, model="gemma3:4b") -> str:
    """
    Send the formatted prompt to the LLM asynchronously and return the response.
    """
    url = os.getenv("LLM_API_URL", "http://localhost:11434/api/chat")
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=1000.0)

            if response.status_code == 200:
                llm_response = ""
                async for content in process_streaming_response(response):
                    print(content, end="", flush=True)  # Print each chunk as it arrives
                    llm_response += content
                    llm_response = 'I am testing'
                return llm_response
            else:
                raise RuntimeError(f"Error {response.status_code}: {response.text}")
    except httpx.RequestError as e:
        raise RuntimeError(f"HTTP request failed: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Failed to send prompt to LLM: {str(e)}")
    
async def send_to_deepseek(llm_response, model='deepseek-r1:7b'):
    """
    Send the LLM response to the DeepThinking model for final analysis.
    """
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": "I am testing, dont think, just provide a one line response"},
            {"role": "user", "content": llm_response}
        ]
    }

    print("Debug: Payload being sent to DeepThinking API:", payload)

    # Optionally include stock data in the prompt
    # if stock_data:
    #   payload["messages"].insert(0, {"role": "user", "content": f"Stock Data: {stock_data}"})
     
    try:
        async with httpx.AsyncClient() as client:
            # Stream the response
            async with client.stream("POST", url, json=payload, timeout=100.0) as response:
                if response.status_code == 200:
                    # Process the response using process_streaming_response
                    deepthinking_response = ""
                    async for content in process_streaming_response(response):
                        print(content, end="", flush=True)  # Print each chunk as it arrives
                        deepthinking_response += content
                    return deepthinking_response
                else:
                    print(f"Debug: DeepThinking API response status: {response.status_code}")
                    print(f"Debug: DeepThinking API response text: {response.text}")
                    raise RuntimeError(f"Error {response.status_code}: {response.text}")
    except httpx.RequestError as e:
        print(f"Debug: HTTP request error: {str(e)}")
        raise RuntimeError(f"Failed to send data to DeepThinking model: {str(e)}")
    except Exception as e:
        print(f"Debug: General exception: {str(e)}")
        raise RuntimeError(f"Failed to send data to DeepThinking model: {str(e)}")
    
def store_analysis(symbol, analysis):
    """
    Store the analysis in the database, avoiding duplicates.
    """
    db.analyses.update_one(
        {"symbol": symbol},
        {"$set": {
            "analysis": analysis,
            "timestamp": datetime.now()
        }},
        upsert=True
    )
    
async def fetch_and_analyze_all_stock_data(ticker: str):
    try:
        print("Debug: Using hardcoded responses for testing.")

        # Hardcoded stock data
        stock_data = {
            "metadata": {
                "ticker": ticker,
                "industry": "Technology",
                "market_cap": "2.5T",
                "dividend_yield": "0.5%",
                "pe_ratio": "30.5",
                "eps": "5.25",
                "beta": "1.2",
                "52_week_high": "200",
                "52_week_low": "100",
                "current_price": "150",
                "analyst_ratings": "Strong Buy",
                "price_targets": "180",
                "events": "Earnings report next week",
                "about_AAPL": "Apple Inc. is a technology company.",
                "last_updated": datetime.now(),
            }
        }
        print("Debug: Hardcoded stock data:", stock_data)

        # Hardcoded analysis
        analysis = ""
        print("Debug: Hardcoded analysis:", analysis)

        # Hardcoded LLM response
        llm_response = f"Hardcoded LLM response."
        print("Debug: Hardcoded LLM response:", llm_response)

        # Hardcoded DeepThinking response
        deepthinking_response = f"Hardcoded DeepThinking response for {ticker}: Apple is a strong buy due to its market dominance and consistent growth."
        print("Debug: Hardcoded DeepThinking response:", deepthinking_response)

        return {
            "symbol": ticker,
            "analysis": analysis,
            "llm_response": llm_response,
            "deepthinking_response": deepthinking_response,
            "stock_data": stock_data,
        }
    except Exception as e:
        print(f"Debug: Exception occurred: {e}")
        raise RuntimeError(f"Error in fetch_and_analyze_all_stock_data: {str(e)}")

async def process_question_with_llm(question: str, context: str = None) -> str:
    try:
        print(f"Debug: Received question: {question}")
        print(f"Debug: Received context: {context}")

        # Construct the prompt
        prompt = f"""
        You are a stock market assistant. Answer the following question concisely:

        Question: {question}
        """
        if context:
            prompt += f"\nContext: {context}\n"

        print(f"Debug: Constructed prompt: {prompt}")

        # Send the prompt to the LLM
        llm_response = await send_prompt_to_llm(prompt)
        
        print(f"Debug: LLM response: {llm_response}")
        return llm_response
    except Exception as e:
        print(f"Error in process_question_with_llm: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

# async def fetch_and_analyze_all_stock_data(ticker: str):
#     try:
#         if USE_MOCK:
#             print("Debug: Using mocked responses for testing.")

#             # Mocked stock data
#             stock_data = {
#                 "metadata": {
#                     "ticker": ticker,
#                     "industry": "Technology",
#                     "market_cap": "2.5T",
#                     "dividend_yield": "0.5%",
#                     "pe_ratio": "30.5",
#                     "eps": "5.25",
#                     "beta": "1.2",
#                     "52_week_high": "200",
#                     "52_week_low": "100",
#                     "current_price": "150",
#                     "analyst_ratings": "Strong Buy",
#                     "price_targets": "180",
#                     "events": "Earnings report next week",
#                     "about_AAPL": "Apple Inc. is a technology company.",
#                     "last_updated": datetime.now(),
#                 }
#             }
#             print("Debug: Mocked stock data:", stock_data)

#             # Mocked analysis
#             analysis = "Analyze the following stock data:\n\nMetadata: Mocked metadata for testing.\n\nThis is a preliminary analysis. Please consult a financial advisor for investment decisions."
#             print("Debug: Mocked analysis:", analysis)

#             # Mocked LLM response
#             llm_response = f"Mock LLM response for {ticker}: Apple is a leader in the technology sector with strong fundamentals."
#             print("Debug: Mocked LLM response:", llm_response)

#             # Mocked DeepThinking response
#             deepthinking_response = f"Mock DeepThinking response for {ticker}: Apple is a strong buy due to its market dominance and consistent growth."
#             print("Debug: Mocked DeepThinking response:", deepthinking_response)

#             return {
#                 "symbol": ticker,
#                 "analysis": analysis,
#                 "llm_response": llm_response,
#                 "deepthinking_response": deepthinking_response,
#                 "stock_data": stock_data,
#             }

#         # Real implementation
#         stock_data = validate_stock_data(await fetch_all_stock_data(ticker))
#         print("Debug: Fetched stock data:", stock_data)

#         if not stock_data or "metadata" not in stock_data:
#             print("Debug: No stock data available, using default prompt.")
#             prompt = "I'm testing the system, just say hi!"
#         else:
#             metadata = stock_data["metadata"]
#             print("Debug: Metadata:", metadata)

#             analysis = perform_analysis(metadata)
#             print("Debug: Analysis result:", analysis)

#             prompt = f"""
#             Analyze the following stock data:

#             Metadata: {metadata}
#             """
#             print("Debug: Prompt for LLM:", prompt)

#         llm_response = await send_prompt_to_llm(prompt)
#         print("Debug: LLM response:", llm_response)

#         deepthinking_response = await send_to_deepseek(llm_response)
#         print("Debug: DeepThinking response:", deepthinking_response)

#         return {
#             "symbol": ticker,
#             "analysis": analysis if 'analysis' in locals() else "No analysis performed",
#             "llm_response": llm_response,
#             "deepthinking_response": deepthinking_response,
#             "stock_data": stock_data if stock_data else "No stock data available"
#         }
#     except Exception as e:
#         print(f"Debug: Exception occurred: {e}")
#         raise RuntimeError(f"Error in fetch_and_analyze_all_stock_data: {str(e)}")