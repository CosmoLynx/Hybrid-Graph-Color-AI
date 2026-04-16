"""
FastAPI application — entry point for the Hybrid Graph Coloring API.

Endpoints:
    POST /color-graph  — accept a graph, run ML prediction + correction
    POST /random-graph — generate a random graph for quick testing
"""

from typing import List, Tuple

import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from coloring import correct_coloring, find_conflicts, validate_coloring
from model import predict_colors
from utils import build_adjacency_matrix, compute_graph_layout, generate_random_graph

# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------

class Edge(BaseModel):
    source: int
    target: int


class GraphRequest(BaseModel):
    nodes: int = Field(..., ge=1, le=50, description="Number of nodes (1–50)")
    edges: List[Edge] = Field(default_factory=list)


class RandomGraphRequest(BaseModel):
    nodes: int = Field(default=10, ge=1, le=50)
    edge_probability: float = Field(default=0.3, ge=0.0, le=1.0)


class NodePosition(BaseModel):
    id: int
    x: float
    y: float


class ColoringResponse(BaseModel):
    nodes: int
    edges: List[Edge]
    positions: List[NodePosition]
    colors_before: List[int]
    colors_after: List[int]
    conflicts_before: List[Edge]
    conflicts_after: List[Edge]
    num_colors_before: int
    num_colors_after: int
    is_valid_before: bool
    is_valid_after: bool


class RandomGraphResponse(BaseModel):
    nodes: int
    edges: List[Edge]


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Hybrid Graph Coloring AI",
    description="ML-predicted + deterministically-corrected graph coloring",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.post("/color-graph", response_model=ColoringResponse)
async def color_graph(request: GraphRequest):
    """Run the hybrid graph coloring pipeline."""
    num = request.nodes
    edge_tuples: List[Tuple[int, int]] = []

    for e in request.edges:
        if e.source < 0 or e.source >= num or e.target < 0 or e.target >= num:
            raise HTTPException(
                status_code=422,
                detail=f"Edge ({e.source}, {e.target}) references node outside range [0, {num - 1}]",
            )
        if e.source == e.target:
            continue  # skip self-loops
        edge_tuples.append((e.source, e.target))

    # Build adjacency matrix
    adj = build_adjacency_matrix(num, edge_tuples)

    # Step 1 — ML prediction
    max_colors = min(num, 6)
    predicted = predict_colors(adj, num, max_colors)

    # Step 2 — Deterministic correction
    corrected = correct_coloring(adj, predicted)

    # Compute conflicts for both stages
    conflicts_before = find_conflicts(adj, predicted)
    conflicts_after = find_conflicts(adj, corrected)

    # Layout
    positions = compute_graph_layout(num, edge_tuples)

    return ColoringResponse(
        nodes=num,
        edges=[Edge(source=u, target=v) for u, v in edge_tuples],
        positions=[
            NodePosition(id=node, x=pos[0], y=pos[1])
            for node, pos in positions.items()
        ],
        colors_before=predicted.tolist(),
        colors_after=corrected.tolist(),
        conflicts_before=[Edge(source=u, target=v) for u, v in conflicts_before],
        conflicts_after=[Edge(source=u, target=v) for u, v in conflicts_after],
        num_colors_before=int(len(set(predicted.tolist()))),
        num_colors_after=int(len(set(corrected.tolist()))),
        is_valid_before=validate_coloring(adj, predicted),
        is_valid_after=validate_coloring(adj, corrected),
    )


@app.post("/random-graph", response_model=RandomGraphResponse)
async def random_graph(request: RandomGraphRequest):
    """Generate a random Erdős–Rényi graph."""
    num, edges = generate_random_graph(request.nodes, request.edge_probability)
    return RandomGraphResponse(
        nodes=num,
        edges=[Edge(source=u, target=v) for u, v in edges],
    )
