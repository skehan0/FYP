import React from 'react';

function Metadata({ data }) {
  if (!data) {
    return <div>No metadata available</div>;
  }

  return (
    <div>
      <h2>Metadata</h2>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}

export default Metadata;