from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn
from dotenv import load_dotenv
import os
from src.alphaVantage.routes import stock_routes
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from logging import info

load_dotenv()

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include stock-related routes
app.include_router(stock_routes.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Stock API"}

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)