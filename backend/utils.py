"""
Utility functions for graph construction, random generation, and layout computation.
"""

import random
from typing import Dict, List, Tuple

import networkx as nx
import numpy as np


def build_adjacency_matrix(num_nodes: int, edges: List[Tuple[int, int]]) -> np.ndarray:
    """Construct a symmetric adjacency matrix from an edge list."""
    adj = np.zeros((num_nodes, num_nodes), dtype=np.float32)
    for u, v in edges:
        adj[u][v] = 1.0
        adj[v][u] = 1.0
    return adj


def build_adjacency_list(num_nodes: int, edges: List[Tuple[int, int]]) -> Dict[int, List[int]]:
    """Construct an adjacency list dictionary from an edge list."""
    adj_list: Dict[int, List[int]] = {i: [] for i in range(num_nodes)}
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
    return adj_list


def generate_random_graph(num_nodes: int, edge_probability: float = 0.3) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Generate a random graph using the Erdős–Rényi model.

    Returns:
        Tuple of (num_nodes, edges) where edges is a list of (u, v) tuples.
    """
    edges: List[Tuple[int, int]] = []
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < edge_probability:
                edges.append((i, j))
    return num_nodes, edges


def compute_graph_layout(
    num_nodes: int, edges: List[Tuple[int, int]]
) -> Dict[int, Tuple[float, float]]:
    """
    Compute a spring layout for the graph using NetworkX.

    Returns:
        Dictionary mapping node_id → (x, y) coordinates normalised to [0, 1].
    """
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))
    G.add_edges_from(edges)

    # Use spring layout with a fixed seed for reproducibility within a single request
    pos = nx.spring_layout(G, seed=42, k=1.5 / max(1, num_nodes ** 0.5))

    # Normalise positions to [0.05, 0.95] range
    if num_nodes <= 1:
        return {0: (0.5, 0.5)} if num_nodes == 1 else {}

    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    range_x = max_x - min_x if max_x != min_x else 1.0
    range_y = max_y - min_y if max_y != min_y else 1.0

    normalised = {}
    for node, (x, y) in pos.items():
        nx_ = 0.05 + 0.9 * (x - min_x) / range_x
        ny_ = 0.05 + 0.9 * (y - min_y) / range_y
        normalised[node] = (round(nx_, 4), round(ny_, 4))

    return normalised
