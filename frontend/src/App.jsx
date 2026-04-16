import { useState } from 'react';
import GraphInput from './components/GraphInput';
import GraphVisualization from './components/GraphVisualization';
import ResultsPanel from './components/ResultsPanel';

const API_BASE = 'http://localhost:8000';

export default function App() {
  const [data, setData] = useState(null);
  const [viewMode, setViewMode] = useState('after');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleColorGraph = async (graphInput) => {
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`${API_BASE}/color-graph`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(graphInput),
      });
      if (!res.ok) {
        const detail = await res.json().catch(() => ({}));
        throw new Error(detail.detail || `Server error ${res.status}`);
      }
      const result = await res.json();
      setData(result);
      setViewMode('after');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleRandomGraph = async (numNodes) => {
    setLoading(true);
    setError('');
    try {
      // Step 1: generate random graph
      const res1 = await fetch(`${API_BASE}/random-graph`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nodes: numNodes, edge_probability: 0.35 }),
      });
      if (!res1.ok) throw new Error('Failed to generate random graph');
      const randomGraph = await res1.json();

      // Step 2: color it
      const res2 = await fetch(`${API_BASE}/color-graph`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(randomGraph),
      });
      if (!res2.ok) throw new Error('Failed to color the graph');
      const result = await res2.json();
      setData(result);
      setViewMode('after');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header glass-card">
        <div>
          <h1>Hybrid Graph Coloring AI</h1>
          <p className="subtitle">
            ML-predicted initial coloring → deterministic correction → valid graph coloring
          </p>
        </div>
        {data && (
          <div style={{ display: 'flex', gap: 'var(--space-sm)' }}>
            <span className="badge badge-success">
              ✓ {data.num_colors_after} colors
            </span>
            <span className={`badge ${data.is_valid_after ? 'badge-success' : 'badge-error'}`}>
              {data.is_valid_after ? '✓ Valid' : '✗ Invalid'}
            </span>
          </div>
        )}
      </header>

      {/* Sidebar */}
      <aside className="sidebar">
        <GraphInput
          onColorGraph={handleColorGraph}
          onRandomGraph={handleRandomGraph}
          loading={loading}
        />
        <ResultsPanel
          data={data}
          viewMode={viewMode}
          onViewChange={setViewMode}
        />
      </aside>

      {/* Main */}
      <main className="main-content">
        {error && (
          <div className="error-message fade-in">
            ⚠️ {error}
          </div>
        )}
        <GraphVisualization data={data} viewMode={viewMode} />
      </main>
    </div>
  );
}
