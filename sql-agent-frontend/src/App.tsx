import { useState } from 'react';
import type { AgentResponse } from './types/agent';
import { QueryInput } from './components/QueryInput';
import { AgentSteps } from './components/AgentSteps';
import { ResultTable } from './components/ResultTable';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface Result {
  question: string;
  response: AgentResponse;
}

export default function App() {
  const [results, setResults] = useState<Result[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleQuery(question: string) {
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`${API_URL}/api/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });
      const data: AgentResponse = await res.json();
      setResults(prev => [{ question, response: data }, ...(prev || [])]);
    } catch {
      setError('请求失败，请检查后端是否运行');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>SQL Writing Agent</h1>
        <p className="subtitle">用自然语言查询数据库</p>
      </header>

      <div className="main">
        <QueryInput onSubmit={handleQuery} loading={loading} />
        {loading && (
          <div className="loading">
            <span>Agent 正在分析...</span>
          </div>
        )}
        {error && <div className="error">{error}</div>}
        {results.map((r, i) => (
          <div key={i} className="result-block">
            <p className="question">{r.question}</p>
            <AgentSteps steps={r.response.steps} />
            <ResultTable steps={r.response.steps} />
            <div className="answer">
              <p className="answer-title">分析结论</p>
              <p>{r.response.answer}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}