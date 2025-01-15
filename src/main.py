from fastapi import FastAPI
from src.yahooFinance.routes import stock_routes

app = FastAPI()

# Include stock-related routes
app.include_router(stock_routes.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Stock API"}