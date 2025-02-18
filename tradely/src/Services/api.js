import axios from 'axios';

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