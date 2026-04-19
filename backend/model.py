"""
Lightweight NumPy neural network for initial graph color prediction.

The model takes a flattened adjacency matrix as input and outputs a predicted
color class for each node. Since the model uses random initialisation (no
pre-training), predictions are essentially learned heuristics — the
deterministic correction step in coloring.py guarantees validity.

Note: This is a pure-NumPy reimplementation of the original PyTorch model,
enabling deployment on platforms with strict package-size limits (e.g. Vercel).
"""

import numpy as np


class LinearLayer:
    """A single fully-connected (dense) layer with Xavier-uniform init."""

    def __init__(self, in_features: int, out_features: int, rng: np.random.Generator):
        limit = np.sqrt(6.0 / (in_features + out_features))
        self.weight = rng.uniform(-limit, limit, (out_features, in_features)).astype(np.float32)
        self.bias = np.zeros(out_features, dtype=np.float32)

    def __call__(self, x: np.ndarray) -> np.ndarray:
        return x @ self.weight.T + self.bias


def relu(x: np.ndarray) -> np.ndarray:
    """Element-wise ReLU activation."""
    return np.maximum(0, x)


class GraphColoringModel:
    """
    Feedforward neural network for graph coloring prediction (NumPy).

    Architecture:
        Input (n²) → Linear → ReLU
                    → Linear → ReLU
                    → Linear → ReLU
                    → Output (n × max_colors)
    """

    def __init__(self, num_nodes: int, max_colors: int = 6, seed: int = 42):
        self.num_nodes = num_nodes
        self.max_colors = max_colors

        rng = np.random.default_rng(seed)

        input_size = num_nodes * num_nodes
        hidden_size = min(256, max(64, num_nodes * 8))
        output_size = num_nodes * max_colors

        self.layers = [
            LinearLayer(input_size, hidden_size, rng),
            LinearLayer(hidden_size, hidden_size, rng),
            LinearLayer(hidden_size, hidden_size // 2, rng),
            LinearLayer(hidden_size // 2, output_size, rng),
        ]

    def __call__(self, x: np.ndarray) -> np.ndarray:
        """
        Forward pass.

        Args:
            x: Flattened adjacency matrix of shape (n²,).

        Returns:
            Array of shape (n, max_colors) with raw logits.
        """
        out = x
        for layer in self.layers[:-1]:
            out = relu(layer(out))
        # Last layer — no activation (raw logits)
        out = self.layers[-1](out)
        return out.reshape(self.num_nodes, self.max_colors)


def predict_colors(adj_matrix: np.ndarray, num_nodes: int, max_colors: int = 6) -> np.ndarray:
    """
    Run the neural network to predict initial color assignments.

    Args:
        adj_matrix: (n, n) numpy adjacency matrix.
        num_nodes: Number of nodes in the graph.
        max_colors: Maximum number of color classes.

    Returns:
        1-D numpy array of predicted color indices for each node.
    """
    model = GraphColoringModel(num_nodes, max_colors)

    # Flatten the adjacency matrix
    flat = adj_matrix.flatten().astype(np.float32)

    logits = model(flat)  # (n, max_colors)
    predictions = np.argmax(logits, axis=1)  # (n,)

    return predictions
