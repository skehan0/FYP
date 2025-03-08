import axios from 'axios';
const API_KEY = process.env.REACT_APP_ALPHA_VANTAGE_API_KEY;

// Create an instance of axios with the base URL
const api = axios.create({
  baseURL: "http://localhost:8000"
});

// Export the Axios instance
export default api;

// Fetch historical stock data
export const fetchHistoricalData = async (ticker, period = '1mo') => {
  const response = await fetch(`http://localhost:8000/historical/${ticker}?period=${period}`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
};

// Fetch stock metadata
export const fetchStockMetadata = async (ticker) => {
  const response = await fetch(`http://localhost:8000/metadata/${ticker}`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
};

// Fetch news headlines
export const fetchNewsHeadlines = async (ticker, limit = 8) => {
  const response = await fetch(`http://localhost:8000/news/${ticker}?limit=${limit}`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
};

// Fetch live market data (general)
export const fetchLiveMarketData = async () => {
  const response = await fetch(`http://localhost:8000/market/live-market-data`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
};

// Fetch live news headlines (general)
export const fetchLiveNewsHeadlines = async (limit = 12) => {
  const response = await fetch(`https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey=${API_KEY}`);
  const data = await response.json();
  return data.feed;
};

