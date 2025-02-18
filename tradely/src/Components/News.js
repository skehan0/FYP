import React from 'react';

function News({ data }) {
  if (!data) {
    return <div>No news available</div>;
  }

  return (
    <div>
      <h2>News</h2>
      <ul>
        {data.news.map((item, index) => (
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