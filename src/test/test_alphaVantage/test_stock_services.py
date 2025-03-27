import pytest
from httpx import AsyncClient
from src.main import app 

@pytest.mark.asyncio
async def test_get_stock_metadata():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/metadata/AAPL")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_historical_data():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/historical/AAPL")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_news_headlines():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/news/AAPL")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_income_statement():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/income/AAPL")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_balance_sheet():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/balance/AAPL")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_cash_flow():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/cashflow/AAPL")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_earnings():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/earnings/AAPL")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_SMA():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/SMA/AAPL")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_EMA():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/EMA/AAPL")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_check_db_status():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/status")
    assert response.status_code == 200

if __name__ == "__main__":
    pytest.main()