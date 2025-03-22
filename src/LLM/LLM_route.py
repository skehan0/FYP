from fastapi import APIRouter, HTTPException, Query
from src.LLM.LLM_service import fetch_and_analyze_all_stock_data

router = APIRouter()

@router.get("/analyze_all")
async def analyze_all_stock_data(ticker: str = Query(..., description="Stock ticker to analyze")):
    """
    Endpoint to fetch all stock data, analyze it, and send it to the LLM.
    """
    try:
        # Call the service function to fetch, analyze, and send data to the LLM
        result = await fetch_and_analyze_all_stock_data(ticker)

        # Return the result
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))