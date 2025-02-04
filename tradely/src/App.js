import React, { useState } from 'react';
import './Styles/App.css';
import StockData from './Components/StockData';
import Metadata from './Components/Metadata';
import News from './Components/News';

function App() {
  const [ticker, setTicker] = useState('');

  const handleInputChange = (event) => {
    setTicker(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // You can add logic to fetch stock data here if needed
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
          <button type="submit">Fetch Data</button>
        </form>
        <StockData ticker={ticker} />
        <Metadata ticker={ticker} />
        <News ticker={ticker} />
      </header>
    </div>
  );
}

export default App;