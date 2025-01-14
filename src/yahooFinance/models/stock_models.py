from pydantic import BaseModel
from typing import List, Dict

class StockMetadata(BaseModel):
    name: str
    sector: str
    industry: str
    market_cap: int
    dividend_yield: float
    pe_ratio: float
    beta: float
    current_price: float

class StockHistoricalData(BaseModel):
    Date: str
    Open: float
    High: float
    Low: float
    Close: float
    Volume: int

class StockResponse(BaseModel):
    ticker: str
    metadata: StockMetadata
    charts: Dict[str, List[StockHistoricalData]]
    news: List[Dict[str, str]]