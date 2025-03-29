import React, { useState } from 'react';
import '../Styles/questionSection.css';

const QuestionSection = ({ analysis }) => {
  const [userQuestion, setUserQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleQuestionSubmit = async () => {
    if (!userQuestion.trim()) return;

    try {
      setAnswer(''); // Clear previous answer
      setIsLoading(true); // Show loading state

      const response = await fetch('http://localhost:8000/ask-question', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: userQuestion,
          context: analysis, // Optional: Provide stock analysis as context
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch answer');
      }

      const data = await response.json();
      setAnswer(data.answer || 'No answer received.');
    } catch (err) {
      console.error('Error answering question:', err);
    setAnswer('Please provide a valid question or analyze a stock first.');
    } finally {
      setIsLoading(false); // Hide loading state
    }
  };

return (
    <div className="question-section">
        <h3>Ask a Question About the Stock Analysis</h3>
        <input
            type="text"
            value={userQuestion}
            onChange={(e) => setUserQuestion(e.target.value)}
            placeholder="Type your question here"
            className="question-input"
        />
        <button onClick={handleQuestionSubmit} className="question-button" disabled={isLoading}>
            {isLoading ? 'Loading...' : 'Submit'}
        </button>
        {answer && <div className="answer">{answer}</div>}
    </div>
);
};

export default QuestionSection;