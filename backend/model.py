"""
Lightweight PyTorch neural network for initial graph color prediction.

The model takes a flattened adjacency matrix as input and outputs a predicted
color class for each node. Since the model uses random initialisation (no
pre-training), predictions are essentially learned heuristics — the
deterministic correction step in coloring.py guarantees validity.
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class GraphColoringModel(nn.Module):
    """
    Feedforward neural network for graph coloring prediction.

    Architecture:
        Input (n²) → Linear → ReLU → Dropout
                    → Linear → ReLU → Dropout
                    → Linear → ReLU → Dropout
                    → Output (n × max_colors)
    """

    def __init__(self, num_nodes: int, max_colors: int = 6):
        super().__init__()
        input_size = num_nodes * num_nodes
        hidden_size = min(256, max(64, num_nodes * 8))
        output_size = num_nodes * max_colors

        self.num_nodes = num_nodes
        self.max_colors = max_colors

        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_size // 2, output_size),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass.

        Args:
            x: Flattened adjacency matrix of shape (batch, n²).

        Returns:
            Tensor of shape (batch, n, max_colors) with raw logits.
        """
        out = self.network(x)
        return out.view(-1, self.num_nodes, self.max_colors)


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
    model.eval()

    # Flatten the adjacency matrix and add batch dimension
    flat = adj_matrix.flatten().astype(np.float32)
    x = torch.tensor(flat).unsqueeze(0)

    with torch.no_grad():
        logits = model(x)  # (1, n, max_colors)
        predictions = torch.argmax(logits, dim=2).squeeze(0)  # (n,)

    return predictions.numpy()
