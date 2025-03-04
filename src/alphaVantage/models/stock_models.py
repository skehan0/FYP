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
    
# class IncomeStatement(BaseModel):
#     fiscal_date_ending: str
#     reported_currency: str
#     gross_profit: Optional[float]
#     total_revenue: Optional[float]
#     operating_income: Optional[float]
#     net_income: Optional[float]
#     research_and_development: Optional[float]
#     operating_expense: Optional[float]
#     current_assets: Optional[float]
#     total_assets: Optional[float]
#     total_liabilities: Optional[float]
#     shareholder_equity: Optional[float]
#     cash_and_cash_equivalents: Optional[float]
#     capital_expenditures: Optional[float] 