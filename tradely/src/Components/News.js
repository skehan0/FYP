import React, { useEffect, useState } from 'react';
import { fetchNewsHeadlines } from '../Services/api';

function News({ ticker }) {
  const [news, setNews] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (ticker) {
      fetchNewsHeadlines(ticker)
        .then((data) => setNews(data))
        .catch((error) => setError(error));
    }
  }, [ticker]);

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  if (!news) {
    return <div>No news available</div>;
  }

  return (
    <div>
      <h2>News for {ticker}</h2>
      <ul>
        {news.news.map((item, index) => (
          <li key={index}>
            <a href={item.url} target="_blank" rel="noopener noreferrer">
              {item.title}
            </a>
            <p>{item.summary}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default News;