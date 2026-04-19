# Hybrid Graph Coloring AI

A full-stack web application demonstrating a **hybrid approach to graph coloring**:

1. 🧠 A lightweight **neural network** predicts initial node colors
2. ⚙️ A **deterministic correction algorithm** fixes any invalid colorings
3. 🎨 The result is **visualized interactively** with D3.js

### 🌐 [Live Demo → hybrid-graph-color-ai.vercel.app](https://hybrid-graph-color-ai.vercel.app/)

---

## Architecture

```
React Frontend  ──POST /api/color-graph──▶  Serverless Function (FastAPI)
                                               │
                                               ├── model.py (NumPy NN)
                                               │     predicted colors ↓
                                               ├── coloring.py (Correction)
                                               │     valid colors ↓
                                               └── JSON response ──▶  D3.js Visualization
```

---

## Quick Start (Local Development)

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

## Deployment (Vercel)

This project is configured for **one-click Vercel deployment**:

- The **React frontend** is built with Vite and served as static files
- The **FastAPI backend** runs as a Python serverless function via `api/index.py`
- API routes are proxied through Vercel rewrites (`/api/*` → serverless function)

To deploy your own instance:

1. Fork/clone this repo
2. Import the repo on [vercel.com](https://vercel.com)
3. Deploy — `vercel.json` handles all configuration automatically

> **Note:** The neural network uses a pure NumPy implementation (no PyTorch) to fit
> within Vercel's 250MB serverless function size limit. A PyTorch version is available
> on the [`pytorch-version`](../../tree/pytorch-version) branch for local development.

---

## API Endpoints

| Method | Endpoint        | Description                              |
|--------|-----------------|------------------------------------------|
| POST   | `/color-graph`  | Accept a graph, run NN + correction      |
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

| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | FastAPI, NumPy, NetworkX          |
| Frontend   | React 18, Vite, D3.js            |
| Styling    | Vanilla CSS (glassmorphism dark theme) |
| Deployment | Vercel (static + serverless)      |

---

## Project Structure

```
Hybrid-Graph-Color-AI/
├── api/
│   └── index.py             # Vercel serverless entry point
├── backend/
│   ├── main.py               # FastAPI application
│   ├── model.py              # NumPy neural network
│   ├── coloring.py           # Correction algorithm
│   ├── utils.py              # Graph utilities
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
├── vercel.json               # Vercel deployment config
├── requirements.txt          # Python deps (Vercel runtime)
└── README.md
```

---

## License

MIT
