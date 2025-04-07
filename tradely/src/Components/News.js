import React, { useState, useEffect } from 'react';
import '../Styles/news.css';

const News = ({ fetchNews, isLiveNews = false }) => {
  const [data, setData] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const cachedNews = localStorage.getItem(isLiveNews ? 'liveNewsData' : 'newsData');
    const cachedTimestamp = localStorage.getItem(isLiveNews ? 'liveNewsTimestamp' : 'newsTimestamp');
    const now = new Date().getTime();

    // Check if cached data is available and not older than 1 hour
    if (cachedNews && cachedTimestamp && now - cachedTimestamp < 3600000) {
      setData(JSON.parse(cachedNews));
      setIsLoading(false);
    } else {
      fetchNews()
        .then((newsData) => {
          if (newsData && newsData.length > 0) {
            setData(newsData);
            localStorage.setItem(isLiveNews ? 'liveNewsData' : 'newsData', JSON.stringify(newsData));
            localStorage.setItem(isLiveNews ? 'liveNewsTimestamp' : 'newsTimestamp', now);
          } else {
            setError('No news available at the moment.');
          }
        })
        .catch(() => {
          setError('Failed to fetch news. Please try again later.');
        })
        .finally(() => {
          setIsLoading(false);
        });
    }
  }, [fetchNews, isLiveNews]);

  const handlePrev = () => {
    setCurrentIndex((prevIndex) => {
      const newIndex = prevIndex - 3;
      return newIndex < 0 ? Math.max(0, data.length - (data.length % 3 || 3)) : newIndex;
    });
  };

  const handleNext = () => {
    setCurrentIndex((prevIndex) => {
      const newIndex = prevIndex + 3;
      return newIndex >= data.length ? 0 : newIndex;
    });
  };

  const renderDots = () => {
    const dots = [];
    for (let i = 0; i < Math.ceil(data.length / 3); i++) {
      dots.push(
        <span
          key={i}
          className={`dot ${currentIndex / 3 === i ? 'active' : ''}`}
          onClick={() => setCurrentIndex(i * 3)}
        ></span>
      );
    }
    return dots;
  };

  return (
    <div className="news">
      <h2>{isLiveNews ? 'Live News' : 'Latest News'}</h2>
      {isLoading ? (
        <div className="loading-message">Loading news...</div>
      ) : error ? (
        <div className="error-message">{error}</div>
      ) : data.length === 0 ? (
        <div className="no-news-message">No news available at the moment.</div>
      ) : (
        <>
          <div className="news-container">
            <button className="arrow left" onClick={handlePrev}>&#9664;</button>
            {data.slice(currentIndex, currentIndex + 3).map((article, index) => (
              <div key={index} className="news-article">
                {article.banner_image && <img src={article.banner_image} alt="Thumbnail" />}
                <div className="news-content">
                  <h3>{article.title}</h3>
                  <p className="summary">{article.summary}</p>
                  <a href={article.url} target="_blank" rel="noopener noreferrer">Read more</a>
                </div>
              </div>
            ))}

            {data.length < 3 && data.map((article, index) => (
              <div key={index} className="news-article">
                {article.banner_image && <img src={article.banner_image} alt="Thumbnail" />}
                <div className="news-content">
                  <h3>{article.title}</h3>
                  <p className="summary">{article.summary}</p>
                  <a href={article.url} target="_blank" rel="noopener noreferrer">Read more</a>
                </div>
              </div>
            ))}
            <button className="arrow right" onClick={handleNext}>&#9654;</button>
          </div>
          <div className="dots-container">{renderDots()}</div>
        </>
      )}
    </div>
  );
};

export default News;