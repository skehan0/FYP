import React from 'react';
import './Styles/analysisResults.css';

const AnalysisResults = ({ analysis }) => {
    return (
      <div className="analysis-results">
        <h3>Analysis Results</h3>
        <div className="analysis-content">
          {Object.entries(analysis).map(([key, value]) => (
            <div key={key} className="analysis-item">
              <strong>{key}:</strong> {typeof value === 'object' ? JSON.stringify(value, null, 2) : value}
            </div>
          ))}
        </div>
      </div>
    );
  };