import React, { useState, useEffect } from 'react';
import '../Styles/news.css';

const News = ({ fetchNews }) => {
  const [data, setData] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const cachedNews = localStorage.getItem('newsData');
    const cachedTimestamp = localStorage.getItem('newsTimestamp');
    const now = new Date().getTime();

    // Check if cached data is available and not older than 1 hour
    if (cachedNews && cachedTimestamp && now - cachedTimestamp < 3600000) {
      setData(JSON.parse(cachedNews));
    } else {
      fetchNews().then((newsData) => {
        setData(newsData);
        localStorage.setItem('newsData', JSON.stringify(newsData));
        localStorage.setItem('newsTimestamp', now);
      });
    }
  }, [fetchNews]);

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
      <h2>Latest News</h2>
      <div className="news-container">
        <button className="arrow left" onClick={handlePrev}>&#9664;</button>
        {data.slice(currentIndex, currentIndex + 3).map((article, index) => (
          <div key={index} className="news-article">
            <h3>{article.title}</h3>
            {article.banner_image && <img src={article.banner_image} alt="Thumbnail" />}
            <p>{article.summary}</p>
            <a href={article.url} target="_blank" rel="noopener noreferrer">Read more</a>
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