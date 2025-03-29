import React, { useState, useEffect } from 'react';
import jsPDF from 'jspdf'; 
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

  // Save as TXT
  const saveAsTXT = () => {
    const blob = new Blob([analysis], { type: 'text/plain' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `${ticker || 'stock'}_analysis.txt`;
    link.click();
  };

  // Save as CSV
  const saveAsCSV = () => {
    const csvContent = `data:text/csv;charset=utf-8,${encodeURIComponent(analysis)}`;
    const link = document.createElement('a');
    link.href = csvContent;
    link.download = `${ticker || 'stock'}_analysis.csv`;
    link.click();
  };

  // Save as PDF
  const saveAsPDF = () => {
    const doc = new jsPDF();
    const lines = analysis.split('\n');
    lines.forEach((line, index) => {
      doc.text(line, 10, 10 + index * 10); // Add each line with spacing
    });
    doc.save(`${ticker || 'stock'}_analysis.pdf`);
  };

  // Save as JSON
  const saveAsJSON = () => {
    const jsonContent = JSON.stringify({ ticker, analysis });
    const blob = new Blob([jsonContent], { type: 'application/json' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `${ticker || 'stock'}_analysis.json`;
    link.click();
  };

  return (
    <div className="analysis-section">
      <h3>Stock Analysis</h3>
      {isLoading && <div className="loading">Processing... Please wait.</div>}
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
          <button onClick={saveAsTXT} className="save-analysis-button">Save as TXT</button>
          <button onClick={saveAsCSV} className="save-analysis-button">Save as CSV</button>
          <button onClick={saveAsPDF} className="save-analysis-button">Save as PDF</button>
          <button onClick={saveAsJSON} className="save-analysis-button">Save as JSON</button>
        </div>
      )}
    </div>
  );
};

export default AnalysisSection;