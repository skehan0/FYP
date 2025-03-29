import React, { useState, useEffect } from 'react';
import { saveAsTXT, saveAsCSV, saveAsPDF, saveAsJSON } from '../Utils/fileUtils';
import '../Styles/analysisSection.css';

const AnalysisSection = ({ analysis, isLoading, error, ticker }) => {
  const [visibleLines, setVisibleLines] = useState([]);

  useEffect(() => {
    if (analysis) {
      const lines = analysis.split('\n');
      setVisibleLines([]);
      const timeouts = [];

      lines.forEach((line, index) => {
        const timeout = setTimeout(() => {
          setVisibleLines((prev) => [...prev, line]);
        }, index * 600);
        timeouts.push(timeout);
      });

      return () => {
        timeouts.forEach((timeout) => clearTimeout(timeout));
      };
    }
  }, [analysis]);

  return (
    <div className="analysis-section">
      <h3>Stock Analysis</h3>
      {isLoading && <div className="loading"></div>}
      {error && <div className="error">Error: {error}</div>}
      <div className="analysis-output">
        {visibleLines.map((line, index) => (
          <p
            key={index}
            className={line.toLowerCase().includes('recommendation') ? 'highlight' : ''}
          >
            {line}
          </p>
        ))}
      </div>
      {analysis && (
        <div className="save-buttons">
          <button
            onClick={() => saveAsTXT(analysis, `${ticker || 'stock'}_analysis.txt`)}
            className="save-analysis-button"
          >
            Save as TXT
          </button>
          <button
            onClick={() => saveAsCSV(analysis, `${ticker || 'stock'}_analysis.csv`)}
            className="save-analysis-button"
          >
            Save as CSV
          </button>
          <button
            onClick={() => saveAsPDF(analysis, `${ticker || 'stock'}_analysis.pdf`)}
            className="save-analysis-button"
          >
            Save as PDF
          </button>
          <button
            onClick={() => saveAsJSON({ ticker, analysis }, `${ticker || 'stock'}_analysis.json`)}
            className="save-analysis-button"
          >
            Save as JSON
          </button>
        </div>
      )}
    </div>
  );
};

export default AnalysisSection;