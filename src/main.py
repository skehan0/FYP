from fastapi import FastAPI
from src.routes import stock_routes

app = FastAPI()

# Include stock-related routes
app.include_router(stock_routes.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Stock API"}



# from fastapi import FastAPI, HTTPException
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel, Field
# from datetime import datetime
# import yfinance as yf
#
# # FastAPI app setup
# app = FastAPI()
#
# # CORS Middleware (allow all origins for testing)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# # Models
# class StockRequest(BaseModel):
#     symbol: str
#     start_date: str
#     end_date: str
#
# class MultiStockRequest(BaseModel):
#     symbols: list[str]
#     start_date: str
#     end_date: str
#
# class StockResponse(BaseModel):
#     symbol: str
#     start_date: str
#     end_date: str
#     total_items: int
#     page: int
#     limit: int
#     data: list[dict] = Field(
#         ...,
#         example=[
#             {
#                 "date": "2017-01-01",
#                 "open": 26.81,
#                 "high": 26.93,
#                 "low": 26.57,
#                 "close": 26.89,
#                 "volume": 115127600,
#                 "dividends": 0,
#                 "splits": 0,
#             }
#         ],
#     )
#
# # Utility Functions
# def validate_stock_request(symbol: str, start_date: str, end_date: str):
#     try:
#         datetime.strptime(start_date, "%Y-%m-%d")
#         datetime.strptime(end_date, "%Y-%m-%d")
#     except ValueError:
#         raise HTTPException(status_code=400, detail="Dates must be in YYYY-MM-DD format.")
#     if not symbol.isalpha():
#         raise HTTPException(status_code=400, detail="Stock symbol must be alphabetic.")
#
# def fetch_stock_data(symbol: str, start_date: str, end_date: str, page: int = 1, limit: int = 50):
#     ticker = yf.Ticker(symbol)
#     data = ticker.history(start=start_date, end=end_date)
#     if data.empty:
#         raise HTTPException(status_code=404, detail="No stock data found for the given parameters.")
#
#     data.reset_index(inplace=True)
#     total_items = len(data)
#     start_index = (page - 1) * limit
#     end_index = start_index + limit
#
#     return {
#         "symbol": symbol.upper(),
#         "start_date": start_date,
#         "end_date": end_date,
#         "total_items": total_items,
#         "page": page,
#         "limit": limit,
#         "data": [
#             {
#                 "date": row["Date"].strftime("%Y-%m-%d"),
#                 "open": row["Open"],
#                 "high": row["High"],
#                 "low": row["Low"],
#                 "close": row["Close"],
#                 "volume": row["Volume"],
#                 "dividends": row["Dividends"],
#                 "splits": row["Stock Splits"],
#             }
#             for _, row in data.iloc[start_index:end_index].iterrows()
#         ],
#     }
#
# def fetch_stock_summary(symbol: str):
#     ticker = yf.Ticker(symbol)
#     info = ticker.info
#     if not info:
#         raise HTTPException(status_code=404, detail="No stock summary found for the given symbol.")
#     return info
#
# def fetch_stock_events(symbol: str):
#     ticker = yf.Ticker(symbol)
#     events = ticker.actions
#     if events.empty:
#         raise HTTPException(status_code=404, detail="No stock events found for the given symbol.")
#     return events.to_dict()
#
# # Routes
# @app.post("/stocks", response_model=StockResponse)
# async def get_stock_data(request: StockRequest, page: int = 1, limit: int = 5000):
#     try:
#         validate_stock_request(request.symbol, request.start_date, request.end_date)
#         stock_data = fetch_stock_data(request.symbol, request.start_date, request.end_date, page, limit)
#         return stock_data
#     except HTTPException as e:
#         return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
#
# @app.get("/stocks/{symbol}/summary")
# async def get_stock_summary(symbol: str):
#     try:
#         return fetch_stock_summary(symbol)
#     except HTTPException as e:
#         return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
#
# @app.get("/stocks/{symbol}/events")
# async def get_stock_events(symbol: str):
#     try:
#         return fetch_stock_events(symbol)
#     except HTTPException as e:
#         return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
#
# @app.post("/stocks/multiple")
# async def get_multiple_stocks(request: MultiStockRequest):
#     results = {}
#     for symbol in request.symbols:
#         try:
#             validate_stock_request(symbol, request.start_date, request.end_date)
#             results[symbol] = fetch_stock_data(symbol, request.start_date, request.end_date)
#         except HTTPException as e:
#             results[symbol] = {"error": e.detail}
#     return results