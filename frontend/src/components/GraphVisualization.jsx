import { useEffect, useRef } from 'react';
import * as d3 from 'd3';

// Generate visually distinct colors using golden-angle HSL spacing
function generatePalette(numColors) {
  const palette = [];
  const goldenAngle = 137.508;
  for (let i = 0; i < numColors; i++) {
    const hue = (i * goldenAngle) % 360;
    palette.push(`hsl(${hue}, 72%, 62%)`);
  }
  return palette;
}

export default function GraphVisualization({ data, viewMode }) {
  const svgRef = useRef(null);
  const containerRef = useRef(null);

  useEffect(() => {
    if (!data || !svgRef.current || !containerRef.current) return;

    const container = containerRef.current;
    const width = container.clientWidth;
    const height = container.clientHeight || width * 0.75;

    const svg = d3
      .select(svgRef.current)
      .attr('viewBox', `0 0 ${width} ${height}`)
      .attr('preserveAspectRatio', 'xMidYMid meet');

    // Clear previous content
    svg.selectAll('*').remove();

    // Determine which colors/conflicts to show
    const colors = viewMode === 'before' ? data.colors_before : data.colors_after;
    const conflicts =
      viewMode === 'before' ? data.conflicts_before : data.conflicts_after;

    const maxColor = Math.max(...colors, 0);
    const palette = generatePalette(maxColor + 1);

    // Build position map
    const posMap = {};
    data.positions.forEach((p) => {
      posMap[p.id] = { x: p.x * width, y: p.y * height };
    });

    // Build conflict set for quick lookup
    const conflictSet = new Set();
    conflicts.forEach((c) => {
      const key = `${Math.min(c.source, c.target)}-${Math.max(c.source, c.target)}`;
      conflictSet.add(key);
    });

    // Defs — glow filter
    const defs = svg.append('defs');
    const glowFilter = defs.append('filter').attr('id', 'node-glow');
    glowFilter
      .append('feGaussianBlur')
      .attr('stdDeviation', 4)
      .attr('result', 'blur');
    const feMerge = glowFilter.append('feMerge');
    feMerge.append('feMergeNode').attr('in', 'blur');
    feMerge.append('feMergeNode').attr('in', 'SourceGraphic');

    // Edges
    const edgeGroup = svg.append('g').attr('class', 'edges');
    data.edges.forEach((e) => {
      const pA = posMap[e.source];
      const pB = posMap[e.target];
      if (!pA || !pB) return;
      const key = `${Math.min(e.source, e.target)}-${Math.max(e.source, e.target)}`;
      const isConflict = conflictSet.has(key);

      edgeGroup
        .append('line')
        .attr('x1', pA.x)
        .attr('y1', pA.y)
        .attr('x2', pB.x)
        .attr('y2', pB.y)
        .attr('stroke', isConflict ? '#fb7185' : 'rgba(255,255,255,0.12)')
        .attr('stroke-width', isConflict ? 2.5 : 1.5)
        .attr('stroke-dasharray', isConflict ? '6 3' : 'none')
        .style('opacity', 0)
        .transition()
        .duration(500)
        .delay(100)
        .style('opacity', 1);
    });

    // Nodes
    const nodeGroup = svg.append('g').attr('class', 'nodes');
    const nodeRadius = Math.max(14, Math.min(28, 300 / data.nodes));

    data.positions.forEach((p, i) => {
      const cx = posMap[p.id].x;
      const cy = posMap[p.id].y;
      const color = palette[colors[p.id]] || '#888';

      // Glow circle
      nodeGroup
        .append('circle')
        .attr('cx', cx)
        .attr('cy', cy)
        .attr('r', nodeRadius + 6)
        .attr('fill', color)
        .attr('opacity', 0.15)
        .attr('filter', 'url(#node-glow)');

      // Main circle
      nodeGroup
        .append('circle')
        .attr('cx', cx)
        .attr('cy', cy)
        .attr('r', 0)
        .attr('fill', color)
        .attr('stroke', 'rgba(255,255,255,0.2)')
        .attr('stroke-width', 1.5)
        .style('cursor', 'pointer')
        .transition()
        .duration(500)
        .delay(i * 30)
        .attr('r', nodeRadius)
        .ease(d3.easeBounceOut);

      // Label
      nodeGroup
        .append('text')
        .attr('x', cx)
        .attr('y', cy)
        .attr('text-anchor', 'middle')
        .attr('dominant-baseline', 'central')
        .attr('fill', '#fff')
        .attr('font-size', Math.max(10, nodeRadius * 0.7))
        .attr('font-weight', 600)
        .attr('font-family', 'Inter, sans-serif')
        .attr('pointer-events', 'none')
        .style('opacity', 0)
        .text(p.id)
        .transition()
        .duration(400)
        .delay(i * 30 + 200)
        .style('opacity', 1);
    });
  }, [data, viewMode]);

  if (!data) {
    return (
      <div className="glass-card" style={{ flex: 1 }}>
        <div className="empty-state">
          <div className="empty-state-icon">🔗</div>
          <p>
            Input a graph and click <strong>Run Coloring</strong> to see the
            visualization.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="glass-card fade-in" style={{ flex: 1 }}>
      <div className="card-section" ref={containerRef}>
        <div className="graph-svg-container">
          <svg ref={svgRef} />
        </div>
      </div>
    </div>
  );
}

export { generatePalette };
