import React, { useState, useEffect } from 'react';
import '../Styles/news.css';

const News = ({ fetchNews, isLiveNews = false }) => {
  const [data, setData] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const cachedNews = localStorage.getItem(isLiveNews ? 'liveNewsData' : 'newsData');
    const cachedTimestamp = localStorage.getItem(isLiveNews ? 'liveNewsTimestamp' : 'newsTimestamp');
    const now = new Date().getTime();

    // Check if cached data is available and not older than 1 hour
    if (cachedNews && cachedTimestamp && now - cachedTimestamp < 3600000) {
      setData(JSON.parse(cachedNews));
    } else {
      fetchNews().then((newsData) => {
        setData(newsData);
        localStorage.setItem(isLiveNews ? 'liveNewsData' : 'newsData', JSON.stringify(newsData));
        localStorage.setItem(isLiveNews ? 'liveNewsTimestamp' : 'newsTimestamp', now);
      });
    }
  }, [fetchNews, isLiveNews]);

  const handlePrev = () => {
    setCurrentIndex((prevIndex) => (prevIndex === 0 ? data.length - 3 : prevIndex - 3));
  };

  const handleNext = () => {
    setCurrentIndex((prevIndex) => (prevIndex === data.length - 3 ? 0 : prevIndex + 3));
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
        <button className="arrow right" onClick={handleNext}>&#9654;</button>
      </div>
      <div className="dots-container">
        {renderDots()}
      </div>
    </div>
  );
};

export default News;