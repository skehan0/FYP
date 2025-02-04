from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.yahooFinance.routes import stock_routes

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",  # React development server
    # Add other origins if needed
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