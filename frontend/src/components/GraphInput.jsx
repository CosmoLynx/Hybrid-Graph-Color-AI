import { useState } from 'react';

const SAMPLE_EDGES = `0 1
0 2
1 2
1 3
2 3
3 4
4 5
5 6
6 3`;

export default function GraphInput({ onColorGraph, onRandomGraph, loading }) {
  const [numNodes, setNumNodes] = useState(7);
  const [edgeText, setEdgeText] = useState(SAMPLE_EDGES);
  const [error, setError] = useState('');

  const parseEdges = (text) => {
    const edges = [];
    const lines = text.trim().split('\n');
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed) continue;
      const parts = trimmed.split(/[\s,]+/);
      if (parts.length < 2) {
        throw new Error(`Invalid edge format: "${trimmed}". Expected "source target".`);
      }
      const source = parseInt(parts[0], 10);
      const target = parseInt(parts[1], 10);
      if (isNaN(source) || isNaN(target)) {
        throw new Error(`Non-numeric node in edge: "${trimmed}".`);
      }
      edges.push({ source, target });
    }
    return edges;
  };

  const handleSubmit = () => {
    setError('');
    try {
      const edges = parseEdges(edgeText);
      // Validate node references
      for (const e of edges) {
        if (e.source < 0 || e.source >= numNodes || e.target < 0 || e.target >= numNodes) {
          throw new Error(
            `Edge (${e.source}, ${e.target}) references node outside range [0, ${numNodes - 1}].`
          );
        }
      }
      onColorGraph({ nodes: numNodes, edges });
    } catch (err) {
      setError(err.message);
    }
  };

  const handleRandom = () => {
    setError('');
    onRandomGraph(numNodes);
  };

  return (
    <div className="glass-card fade-in">
      <div className="card-section">
        <h3 className="section-title">Graph Input</h3>

        <div className="form-group" style={{ marginBottom: 'var(--space-md)' }}>
          <label className="form-label" htmlFor="num-nodes">
            Number of Nodes
          </label>
          <input
            id="num-nodes"
            type="number"
            className="form-input"
            min={1}
            max={50}
            value={numNodes}
            onChange={(e) => setNumNodes(Math.max(1, Math.min(50, parseInt(e.target.value) || 1)))}
          />
        </div>

        <div className="form-group" style={{ marginBottom: 'var(--space-md)' }}>
          <label className="form-label" htmlFor="edge-list">
            Edge List <span style={{ fontWeight: 400, textTransform: 'none', letterSpacing: 0 }}>
              (one per line: source target)
            </span>
          </label>
          <textarea
            id="edge-list"
            className="form-textarea"
            rows={8}
            placeholder="0 1&#10;0 2&#10;1 3"
            value={edgeText}
            onChange={(e) => setEdgeText(e.target.value)}
          />
        </div>

        {error && <div className="error-message">{error}</div>}
      </div>

      <div className="card-section" style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)' }}>
        <button
          id="run-coloring-btn"
          className="btn btn-primary btn-full"
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? (
            <>
              <span className="spinner" /> Running…
            </>
          ) : (
            <>🎨 Run Coloring</>
          )}
        </button>

        <button
          id="random-graph-btn"
          className="btn btn-secondary btn-full"
          onClick={handleRandom}
          disabled={loading}
        >
          🎲 Random Graph
        </button>
      </div>
    </div>
  );
}
