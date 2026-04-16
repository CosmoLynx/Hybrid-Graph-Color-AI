import { generatePalette } from './GraphVisualization';

export default function ResultsPanel({ data, viewMode, onViewChange }) {
  if (!data) return null;

  const colors = viewMode === 'before' ? data.colors_before : data.colors_after;
  const conflicts = viewMode === 'before' ? data.conflicts_before : data.conflicts_after;
  const numColors = viewMode === 'before' ? data.num_colors_before : data.num_colors_after;
  const isValid = viewMode === 'before' ? data.is_valid_before : data.is_valid_after;

  const maxColor = Math.max(...colors, 0);
  const palette = generatePalette(maxColor + 1);

  // Collect unique colors used
  const usedColors = [...new Set(colors)].sort((a, b) => a - b);

  return (
    <div className="glass-card fade-in">
      {/* View Toggle */}
      <div className="card-section">
        <h3 className="section-title">View Mode</h3>
        <div className="toggle-group">
          <button
            id="toggle-before"
            className={`toggle-btn ${viewMode === 'before' ? 'active' : ''}`}
            onClick={() => onViewChange('before')}
          >
            Before Correction
          </button>
          <button
            id="toggle-after"
            className={`toggle-btn ${viewMode === 'after' ? 'active' : ''}`}
            onClick={() => onViewChange('after')}
          >
            After Correction
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="card-section">
        <h3 className="section-title">Statistics</h3>
        <div className="stat-grid">
          <div className="stat-card">
            <div className="stat-value">{data.nodes}</div>
            <div className="stat-label">Nodes</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{data.edges.length}</div>
            <div className="stat-label">Edges</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{numColors}</div>
            <div className="stat-label">Colors Used</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{conflicts.length}</div>
            <div className="stat-label">Conflicts</div>
          </div>
        </div>
      </div>

      {/* Validity */}
      <div className="card-section">
        <h3 className="section-title">Validity</h3>
        {isValid ? (
          <span className="badge badge-success">✓ Valid Coloring</span>
        ) : (
          <span className="badge badge-error">✗ {conflicts.length} Conflict{conflicts.length !== 1 ? 's' : ''}</span>
        )}
      </div>

      {/* Comparison */}
      <div className="card-section">
        <h3 className="section-title">Before → After</h3>
        <div style={{ display: 'flex', gap: 'var(--space-md)', fontSize: '0.8125rem' }}>
          <div style={{ flex: 1 }}>
            <div style={{ color: 'var(--text-muted)', marginBottom: 4 }}>ML Prediction</div>
            <div style={{ color: data.is_valid_before ? 'var(--accent-emerald)' : 'var(--accent-rose)' }}>
              {data.num_colors_before} colors · {data.conflicts_before.length} conflicts
            </div>
          </div>
          <div style={{ color: 'var(--text-muted)', alignSelf: 'center', fontSize: '1.25rem' }}>→</div>
          <div style={{ flex: 1 }}>
            <div style={{ color: 'var(--text-muted)', marginBottom: 4 }}>Corrected</div>
            <div style={{ color: data.is_valid_after ? 'var(--accent-emerald)' : 'var(--accent-rose)' }}>
              {data.num_colors_after} colors · {data.conflicts_after.length} conflicts
            </div>
          </div>
        </div>
      </div>

      {/* Color Legend */}
      <div className="card-section">
        <h3 className="section-title">Color Legend</h3>
        <div className="color-legend">
          {usedColors.map((c) => (
            <div key={c} className="legend-item">
              <div className="legend-swatch" style={{ background: palette[c] }} />
              <span>Color {c}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
