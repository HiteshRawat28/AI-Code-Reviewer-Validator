import React, { useState } from 'react';
import './CodeInputForm.css';

export default function CodeInputForm({ onSubmit, isLoading }) {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('Python');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!code.trim()) return;
    onSubmit(code, language);
  };

  return (
    <form className="code-form glass-panel" onSubmit={handleSubmit}>
      <div className="form-header">
        <h2>Submit Code for Review</h2>
        <select 
          value={language} 
          onChange={(e) => setLanguage(e.target.value)}
          className="language-select"
          disabled={isLoading}
        >
          <option value="Python">Python</option>
          <option value="JavaScript">JavaScript</option>
          <option value="TypeScript">TypeScript</option>
          <option value="Java">Java</option>
          <option value="C++">C++</option>
          <option value="Go">Go</option>
          <option value="Rust">Rust</option>
        </select>
      </div>
      
      <div className="textarea-wrapper">
        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Paste your code snippet here..."
          className="code-textarea"
          spellCheck="false"
          disabled={isLoading}
        />
      </div>

      <button 
        type="submit" 
        className="submit-btn"
        disabled={!code.trim() || isLoading}
      >
        {isLoading ? 'Analyzing...' : 'Analyze Code'}
      </button>
    </form>
  );
}
