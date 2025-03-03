from pydantic import BaseModel
from typing import List, Dict, Optional

class StockMetadata(BaseModel):
    name: str
    sector: str
    industry: str
    market_cap: int
    dividend_yield: Optional[float]
    pe_ratio: Optional[float]
    eps: Optional[float]
    beta: Optional[float]
    current_price: float
    analyst_ratings: float
    price_targets: float
    events: str
    about_ticker: str

class StockHistoricalData(BaseModel):
    Date: str
    Open: float
    High: float
    Low: float
    Close: float
    Volume: int
    
class NewsHeadline(BaseModel):
    number: int
    title: str
    summary: str
    pubDate: str
    conicalURL: str


# class StockResponse(BaseModel):
#     ticker: str
#     metadata: StockMetadata
#     news: List[NewsHeadline]
    
# class TrendingNews(BaseModel):
#     news: List[NewsHeadline]
    