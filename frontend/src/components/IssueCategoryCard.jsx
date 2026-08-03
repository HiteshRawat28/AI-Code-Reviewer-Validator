import React from 'react';
import './IssueCategoryCard.css';

export default function IssueCategoryCard({ title, issues, colorTheme }) {
  const hasIssues = issues && issues.length > 0;

  return (
    <div className={`category-card glass-panel theme-${colorTheme}`}>
      <div className="category-header">
        <h3>{title}</h3>
        <span className="issue-count">{issues ? issues.length : 0} found</span>
      </div>

      {!hasIssues ? (
        <div className="empty-state">
          <span>✅ All clean! No {title.toLowerCase()} detected.</span>
        </div>
      ) : (
        <div className="issues-list">
          {issues.map((issue, index) => (
            <div key={index} className="issue-item">
              <div className="issue-meta">
                <span className={`severity-badge severity-${issue.severity.toLowerCase()}`}>
                  {issue.severity.toUpperCase()}
                </span>
                {issue.line_number && (
                  <span className="line-number">Line: {issue.line_number}</span>
                )}
              </div>
              <p className="issue-desc">{issue.description}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
