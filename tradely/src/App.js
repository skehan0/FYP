import React, { useState, useEffect } from 'react';
import './Styles/App.css';
import Header from './Components/Header';
import StockData from './Components/StockData';
import Metadata from './Components/Metadata';
import News from './Components/News';
import LiveMarketData from './Components/LiveMarketPrices';
import Footer from './Components/Footer';
import { fetchStockMetadata, fetchHistoricalData, fetchNewsHeadlines, fetchLiveMarketPrices, fetchLiveNewsHeadlines, analyzeStock } from './Services/api';

function App() {
  const [ticker, setTicker] = useState('');
  const [range, setRange] = useState('1mo');
  const [metadata, setMetadata] = useState(null);
  const [historicalData, setHistoricalData] = useState(null);
  const [news, setNews] = useState(null);
  const [liveMarketData, setLiveMarketPrices] = useState(null);
  const [liveNews, setLiveNews] = useState(null);
  const [error, setError] = useState(null);
  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    const fetchLiveData = async () => {
      try {
        const marketData = await fetchLiveMarketPrices();
        console.log('Live Market Data:', marketData);
        setLiveMarketPrices(marketData);

        const newsData = await fetchLiveNewsHeadlines();
        console.log('Live News Data:', newsData);
        setLiveNews(newsData);
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
      // const metadata = await fetchStockMetadata(ticker);
      // console.log('Stock Metadata:', metadata);
      // setMetadata(metadata);

      // const historicalData = await fetchHistoricalData(ticker, range);
      // console.log('Historical Data:', historicalData);
      // setHistoricalData(historicalData);

      // const news = await fetchNewsHeadlines(ticker);
      // console.log('News Data:', news);
      // setNews(news);

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
          />
          <datalist id="tickers">
            <option value="AAPL">Apple</option>
            <option value="GOOGL">Alphabet</option>
            <option value="MSFT">Microsoft</option>
            <option value="AMZN">Amazon</option>
            <option value="TSLA">Tesla</option>
            {/* Add more options as needed */}
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
        {metadata && <Metadata data={metadata} />}
        {historicalData && <StockData data={historicalData} />}
        {news && <News data={news} />}
        {liveMarketData && <LiveMarketData data={liveMarketData} />}
        {liveNews && <News fetchNews={fetchLiveNewsHeadlines} />}
        {analysis && (
        <div className="analysis-section">
          <h3>Analysis</h3>
          <p>{analysis.analysis}</p>
        </div>
        )}
      </header>
      <section id="features" className="features-section">
        <h2>Features</h2>
        <ul>
          <li>Real-time stock market data</li>
          <li>Comprehensive stock analysis</li>
          <li>Latest financial news</li>
          <li>Historical stock data</li>
        </ul>
      </section>
      <section id="testimonials" className="testimonials-section">
        <h2>Testimonials</h2>
        <blockquote>
          <p>"Tradeskee has transformed the way I invest in the stock market. The insights are invaluable!"</p>
          <footer>- Jane Doe, Investor</footer>
        </blockquote>
        <blockquote>
          <p>"A must-have tool for anyone serious about stock trading."</p>
          <footer>- John Smith, Trader</footer>
        </blockquote>
      </section>
      <section id="cta" className="cta-section">
        <h2>Get Started Today</h2>
        <p>Sign up now and take your stock trading to the next level.</p>
        <button>Sign Up</button>
      </section>
      <section id="faq" className="faq-section">
        <h2>Frequently Asked Questions</h2>
        <div className="faq-item">
          <h3>What is Tradeskee?</h3>
          <p>Tradeskee is a platform that provides real-time stock market data, comprehensive analysis, and the latest financial news.</p>
        </div>
        <div className="faq-item">
          <h3>How do I get started?</h3>
          <p>Simply sign up for an account and start exploring the features of Tradeskee.</p>
        </div>
      </section>
      <section id="contact" className="contact-section">
        <h2>Contact Us</h2>
        <p>If you have any questions or need assistance, feel free to reach out to us at support@tradeskee.com.</p>
      </section>
      <Footer />
    </div>
  );
}

export default App;