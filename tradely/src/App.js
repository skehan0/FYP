import React, { useState } from 'react';
import './Styles/App.css';
import StockData from './Components/StockData';
import Metadata from './Components/Metadata';
import News from './Components/News';
import { fetchStockMetadata, fetchHistoricalData, fetchNewsHeadlines } from './Services/api';

function App() {
  const [ticker, setTicker] = useState('');
  const [range, setRange] = useState('1mo');
  const [metadata, setMetadata] = useState(null);
  const [historicalData, setHistoricalData] = useState(null);
  const [news, setNews] = useState(null);
  const [error, setError] = useState(null);

  const handleInputChange = (event) => {
    setTicker(event.target.value);
  };

  const handleRangeChange = (event) => {
    setRange(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const metadata = await fetchStockMetadata(ticker);
      const historicalData = await fetchHistoricalData(ticker, range);
      const news = await fetchNewsHeadlines(ticker);
      setMetadata(metadata);
      setHistoricalData(historicalData);
      setNews(news);
      setError(null);
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Stock Data Visualizer</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={ticker}
            onChange={handleInputChange}
            placeholder="Enter stock ticker"
          />
          <input
            type="text"
            value={range}
            onChange={handleRangeChange}
            placeholder="Enter range (e.g., 1mo, 1y)"
          />
          <button type="submit">Fetch Data</button>
        </form>
        {error && <div>Error: {error}</div>}
        {metadata && <Metadata data={metadata} />}
        {historicalData && <StockData data={historicalData} />}
        {news && <News data={news} />}
      </header>
    </div>
  );
}

export default App;