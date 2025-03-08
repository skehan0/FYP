import React from 'react';

const LiveMarketPrices = ({ data }) => {
  return (
    <div className="live-market-prices">
      <h2>Live Market Data</h2>
      <ul>
        {Object.keys(data).map((symbol) => {
          const latestData = data[symbol];
          return (
            <li key={symbol}>
              <h3>{symbol}</h3>
              <div>
                <p><strong>Current Price:</strong> {latestData.close}</p>
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default LiveMarketPrices;