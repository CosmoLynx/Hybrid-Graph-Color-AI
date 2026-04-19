# Hybrid Graph Coloring AI

A full-stack web application demonstrating a **hybrid approach to graph coloring**:

1. 🧠 A lightweight **PyTorch neural network** predicts initial node colors
2. ⚙️ A **deterministic correction algorithm** fixes any invalid colorings
3. 🎨 The result is **visualized interactively** with D3.js

---

## Architecture

```
React Frontend  ──POST /color-graph──▶  FastAPI Backend
                                          │
                                          ├── model.py (PyTorch NN)
                                          │     predicted colors ↓
                                          ├── coloring.py (Correction)
                                          │     valid colors ↓
                                          └── JSON response ──▶  D3.js Visualization
```

---

## Quick Start

### Prerequisites

- **Python 3.9+** with `pip`
- **Node.js 18+** with `npm`

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`.

---

## API Endpoints

| Method | Endpoint        | Description                              |
|--------|-----------------|------------------------------------------|
| POST   | `/color-graph`  | Accept a graph, run ML + correction      |
| POST   | `/random-graph` | Generate a random Erdős–Rényi graph      |

### Example Request

```json
{
  "nodes": 5,
  "edges": [
    {"source": 0, "target": 1},
    {"source": 1, "target": 2},
    {"source": 2, "target": 3},
    {"source": 3, "target": 4},
    {"source": 4, "target": 0}
  ]
}
```

---

## Tech Stack

| Layer    | Technology                    |
|----------|-------------------------------|
| Backend  | FastAPI, PyTorch, NumPy, NetworkX |
| Frontend | React 18, Vite, D3.js         |
| Styling  | Vanilla CSS (glassmorphism dark theme) |

---

## Project Structure

```
Hybrid-Graph-Color-AI/
├── backend/
│   ├── main.py            # FastAPI entry point
│   ├── model.py           # PyTorch neural network
│   ├── coloring.py        # Correction algorithm
│   ├── utils.py           # Graph utilities
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── index.css
│   │   └── components/
│   │       ├── GraphInput.jsx
│   │       ├── GraphVisualization.jsx
│   │       └── ResultsPanel.jsx
│   ├── index.html
│   └── package.json
└── README.md
```
