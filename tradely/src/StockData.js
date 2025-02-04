import React, { useEffect, useState } from 'react';

function StockData({ ticker }) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (ticker) {
      fetch(`http://localhost:8000/api/stock/${ticker}`)
        .then((response) => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then((data) => setData(data))
        .catch((error) => setError(error));
    }
  }, [ticker]);

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  if (!data) {
    return <div>No data available</div>;
  }

  return (
    <div>
      <h2>Stock Data for {ticker}</h2>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}

export default StockData;