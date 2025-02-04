import React, { useEffect, useState } from 'react';
import { fetchStockMetadata } from '../Services/api';

function Metadata({ ticker }) {
  const [metadata, setMetadata] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (ticker) {
      fetchStockMetadata(ticker)
        .then((data) => setMetadata(data))
        .catch((error) => setError(error));
    }
  }, [ticker]);

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  if (!metadata) {
    return <div>No metadata available</div>;
  }

  return (
    <div>
      <h2>Metadata for {ticker}</h2>
      <pre>{JSON.stringify(metadata, null, 2)}</pre>
    </div>
  );
}

export default Metadata;