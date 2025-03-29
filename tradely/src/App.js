import React, { useState, useEffect } from 'react';
import './Styles/App.css';
import './Styles/topGainersLosers.css'; 
import Header from './Components/Header';
import News from './Components/News';
import LiveMarketData from './Components/LiveMarketPrices';
import Footer from './Components/footer';
import TopGainersLosers from './Components/TopGainersLosers'; // Import the new component
import { fetchLiveMarketPrices, fetchLiveNewsHeadlines, analyzeStock } from './Services/api';

function App() {
  const [ticker, setTicker] = useState('');
  const [range, setRange] = useState('1mo');
  const [liveMarketData, setLiveMarketPrices] = useState(null);
  const [liveNews, setLiveNews] = useState(null);
  const [error, setError] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [gainersLosers, setGainersLosers] = useState({ gainers: [], losers: [] }); // State for top gainers and losers

  useEffect(() => {
    const fetchLiveData = async () => {
      try {
        const marketData = await fetchLiveMarketPrices();
        console.log('Live Market Data:', marketData);
        setLiveMarketPrices(marketData);

        const newsData = await fetchLiveNewsHeadlines();
        console.log('Live News Data:', newsData);
        setLiveNews(newsData);

        // Fetch top gainers and losers
        const response = await fetch('http://localhost:8000/top-gainers-losers?limit=5');
        const data = await response.json();
        console.log('Top Gainers and Losers:', data);
        setGainersLosers(data);
      } catch (error) {
        console.error('Error fetching live data:', error);
        setError(error.message);
      }
    };

    fetchLiveData();
  }, []);

  const handleInputChange = (event) => {
    setTicker(event.target.value);
  };

  const handleRangeChange = (event) => {
    setRange(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const analysisResult = await analyzeStock(ticker);
      console.log('Analysis Result:', analysisResult);
      setAnalysis(analysisResult);

      setError(null);
    } catch (error) {
      console.error('Error fetching data:', error);
      setError(error.message);
    }
  };

  return (
    <div className="App">
      <Header />
      <header className="App-header">
        <div className="hero-section">
          <h2>Welcome to Tradeskee</h2>
          <p>Your go-to platform for stock market analysis and insights.</p>
        </div>
        <form onSubmit={handleSubmit}>
          <input
            list="tickers"
            value={ticker}
            onChange={handleInputChange}
            placeholder="Enter stock ticker"
            className='stock-input'
          />
          <datalist id="tickers">
            <option value="AAPL">Apple</option>
            <option value="GOOGL">Alphabet</option>
            <option value="MSFT">Microsoft</option>
            <option value="AMZN">Amazon</option>
            <option value="TSLA">Tesla</option>
          </datalist>
          <select value={range} onChange={handleRangeChange}>
            <option value="1d">1 Day</option>
            <option value="5d">5 Days</option>
            <option value="1mo">1 Month</option>
            <option value="3mo">3 Months</option>
            <option value="6mo">6 Months</option>
            <option value="1y">1 Year</option>
            <option value="2y">2 Years</option>
            <option value="5y">5 Years</option>
            <option value="10y">10 Years</option>
            <option value="ytd">Year to Date</option>
            <option value="max">Max</option>
          </select>
          <button type="submit">Analyze Stock</button>
        </form>
        {error && <div>Error: {error}</div>}
        {analysis && (
          <div className="analysis-section">
            <h3>Analysis</h3>
            <pre>{JSON.stringify(analysis, null, 2)}</pre>
          </div>
        )}
        {liveMarketData && <LiveMarketData data={liveMarketData} />}
        <TopGainersLosers gainers={gainersLosers.gainers} losers={gainersLosers.losers} />
        {liveNews && <News fetchNews={fetchLiveNewsHeadlines} />}
      </header>
      <Footer />
    </div>
  );
}

export default App;