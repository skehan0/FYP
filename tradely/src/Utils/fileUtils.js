import jsPDF from 'jspdf';

/**
 * Save content as a TXT file.
 * @param {string} content - The content to save.
 * @param {string} filename - The name of the file.
 */
export const saveAsTXT = (content, filename = 'file.txt') => {
  const blob = new Blob([content], { type: 'text/plain' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = filename;
  link.click();
};

/**
 * Save content as a CSV file.
 * @param {string} content - The content to save.
 * @param {string} filename - The name of the file.
 */
export const saveAsCSV = (content, filename = 'file.csv') => {
  const csvContent = `data:text/csv;charset=utf-8,${encodeURIComponent(content)}`;
  const link = document.createElement('a');
  link.href = csvContent;
  link.download = filename;
  link.click();
};

/**
 * Save content as a PDF file.
 * @param {string} content - The content to save.
 * @param {string} filename - The name of the file.
 */
export const saveAsPDF = (content, filename = 'file.pdf') => {
  const doc = new jsPDF();
  const lines = content.split('\n');
  lines.forEach((line, index) => {
    doc.text(line, 10, 10 + index * 10); // Add each line with spacing
  });
  doc.save(filename);
};

/**
 * Save content as a JSON file.
 * @param {Object} content - The content to save.
 * @param {string} filename - The name of the file.
 */
export const saveAsJSON = (content, filename = 'file.json') => {
  const jsonContent = JSON.stringify(content, null, 2); // Pretty-print JSON
  const blob = new Blob([jsonContent], { type: 'application/json' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = filename;
  link.click();
};