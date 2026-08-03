import React from 'react';
import IssueCategoryCard from './IssueCategoryCard';
import './ReviewResults.css';

export default function ReviewResults({ data }) {
  if (!data) return null;

  return (
    <div className="review-results-container">
      <h2 className="results-title glow-text">Review Results</h2>
      
      <div className="results-grid">
        <IssueCategoryCard 
          title="Bugs" 
          issues={data.bugs} 
          colorTheme="bug" 
        />
        
        <IssueCategoryCard 
          title="Style Issues" 
          issues={data.style_issues} 
          colorTheme="style" 
        />
        
        <IssueCategoryCard 
          title="Security Vulnerabilities" 
          issues={data.security_issues} 
          colorTheme="security" 
        />
      </div>
    </div>
  );
}
