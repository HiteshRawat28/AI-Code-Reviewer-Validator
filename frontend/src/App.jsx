import React, { useState } from 'react';
import CodeInputForm from './components/CodeInputForm';
import LoadingState from './components/LoadingState';
import ReviewResults from './components/ReviewResults';
import { submitReview } from './api/reviewApi';
import './App.css';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [reviewResult, setReviewResult] = useState(null);

  const handleReviewSubmit = async (code, language) => {
    setIsLoading(true);
    setError(null);
    setReviewResult(null);

    try {
      const data = await submitReview(code, language);
      setReviewResult(data);
    } catch (err) {
      setError(err.message || "An unexpected error occurred while reviewing your code.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1 className="glow-text">AI Code Reviewer</h1>
        <p>Get instant, structured feedback on bugs, style violations, and security vulnerabilities.</p>
      </header>

      <main className="content-wrapper">
        <CodeInputForm onSubmit={handleReviewSubmit} isLoading={isLoading} />
        
        {error && (
          <div className="error-banner">
            ⚠️ {error}
          </div>
        )}

        {isLoading && <LoadingState />}

        {reviewResult && !isLoading && (
          <ReviewResults data={reviewResult} />
        )}
      </main>
    </div>
  );
}

export default App;
