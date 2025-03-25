import axios from 'axios';
const API_KEY = process.env.ALPHA_VANTAGE_API_KEY;

// Create an instance of axios with the base URL
const api = axios.create({
  baseURL: "http://localhost:8000"
});

// Export the Axios instance
export default api;

// Fetch and Analze Stock Data
export const analyzeStock = async (ticker) => {
  const response = await fetch(`http://localhost:8000/analyze_all?ticker=${ticker}`);
  const contentType = response.headers.get('content-type');

  if (!response.ok) {
    if (contentType && contentType.includes('application/json')) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to analyze stock');
    } else {
      const errorText = await response.text();
      throw new Error(errorText || 'Failed to analyze stock');
    }
  }

  if (contentType && contentType.includes('application/json')) {
    return await response.json();
  } else {
    throw new Error('Unexpected response format');
  }
};

// // Fetch historical stock data
// export const fetchHistoricalData = async (ticker, period = '1mo') => {
//   const response = await fetch(`http://localhost:8000/historical/${ticker}?period=${period}`);
//   if (!response.ok) {
//     throw new Error('Network response was not ok');
//   }
//   return response.json();
// };

// // Fetch stock metadata
// export const fetchStockMetadata = async (ticker) => {
//   const response = await fetch(`http://localhost:8000/metadata/${ticker}`);
//   if (!response.ok) {
//     throw new Error('Network response was not ok');
//   }
//   return response.json();
// };

// // Fetch news headlines
// export const fetchNewsHeadlines = async (ticker, limit = 8) => {
//   const response = await fetch(`http://localhost:8000/news/${ticker}?limit=${limit}`);
//   if (!response.ok) {
//     throw new Error('Network response was not ok');
//   }
//   return response.json();
// };


/* Live Market Functions for the Home Page */

export const fetchLiveMarketPrices = async () => {
  try {
    const response = await fetch(`http://localhost:8000/live-market-prices`);
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Live market prices not ok: ${errorText}`);
    }
    const data = await response.json();
    console.log('Live Market Data:', data);
    return data;
  } catch (error) {
    console.error('Error fetching live market prices:', error);
    throw error;
  }
};

// Fetch live news headlines (general)
export const fetchLiveNewsHeadlines = async (limit = 3) => {
  try {
    const response = await fetch(`https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey=${API_KEY}&limit=${limit}`);
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Live news not ok: ${errorText}`);
    }
    const data = await response.json();
    console.log('Live News Data:', data);
    return data.feed;
  } catch (error) {
    console.error('Error fetching live news headlines:', error);
    throw error;
  }
};
