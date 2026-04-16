"""
Deterministic graph coloring correction algorithm.

Takes an initial (possibly invalid) coloring and iteratively fixes conflicts
until a valid coloring is achieved. Also provides utilities for validation
and conflict detection.
"""

from typing import Dict, List, Tuple

import numpy as np

from utils import build_adjacency_list


def find_conflicts(adj_matrix: np.ndarray, colors: np.ndarray) -> List[Tuple[int, int]]:
    """
    Find all edges where both endpoints share the same color.

    Args:
        adj_matrix: (n, n) adjacency matrix.
        colors: 1-D array of color assignments.

    Returns:
        List of (u, v) tuples representing conflicting edges (u < v).
    """
    n = len(colors)
    conflicts: List[Tuple[int, int]] = []
    for i in range(n):
        for j in range(i + 1, n):
            if adj_matrix[i][j] == 1 and colors[i] == colors[j]:
                conflicts.append((i, j))
    return conflicts


def validate_coloring(adj_matrix: np.ndarray, colors: np.ndarray) -> bool:
    """Check if the coloring is valid (no adjacent nodes share a color)."""
    return len(find_conflicts(adj_matrix, colors)) == 0


def correct_coloring(
    adj_matrix: np.ndarray,
    colors: np.ndarray,
    max_iterations: int = 100,
) -> np.ndarray:
    """
    Iteratively correct an invalid graph coloring.

    Algorithm:
        For every edge (u, v) where color[u] == color[v]:
            - Compute the set of colors used by neighbours of u
            - If there is an available color, assign the smallest one to u
            - Otherwise, assign a new color (max_current + 1)
        Repeat until no conflicts remain (guaranteed to terminate because
        we always have the option to introduce a new color).

    Args:
        adj_matrix: (n, n) adjacency matrix.
        colors: 1-D array of initial color assignments (modified in place).
        max_iterations: Safety limit to prevent infinite loops.

    Returns:
        Corrected 1-D color array.
    """
    colors = colors.copy()
    n = len(colors)
    adj_list = build_adjacency_list(n, [])

    # Build adjacency list from the matrix directly
    for i in range(n):
        for j in range(i + 1, n):
            if adj_matrix[i][j] == 1:
                adj_list[i].append(j)
                adj_list[j].append(i)

    for _ in range(max_iterations):
        conflicts = find_conflicts(adj_matrix, colors)
        if not conflicts:
            break

        for u, v in conflicts:
            # Fix node u: find colours used by its neighbours
            neighbour_colors = {colors[nb] for nb in adj_list[u]}
            # Find the smallest available color
            color = 0
            while color in neighbour_colors:
                color += 1
            colors[u] = color

    return colors
