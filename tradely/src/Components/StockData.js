import React, { useEffect, useState } from 'react';
import Chart from './Chart';
import { fetchHistoricalData } from '../Services/api';

function StockData({ ticker }) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (ticker) {
      fetchHistoricalData(ticker)
        .then((data) => {
          const chartData = data.rows.map(row => ({
            time: row.Date,
            value: row.Close,
          }));
          setData(chartData);
        })
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
      <Chart data={data} />
    </div>
  );
}

export default StockData;