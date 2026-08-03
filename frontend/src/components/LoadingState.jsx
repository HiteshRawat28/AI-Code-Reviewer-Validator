import React from 'react';
import './LoadingState.css';

export default function LoadingState() {
  return (
    <div className="loading-container glass-panel">
      <div className="spinner"></div>
      <h3 className="glow-text">Analyzing your code...</h3>
      <p>Our AI is running a deep inspection for bugs, style issues, and security vulnerabilities.</p>
    </div>
  );
}
