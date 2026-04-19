"""
Vercel Serverless Function entry point.

Adds the backend directory to sys.path so that existing modules
(model.py, coloring.py, utils.py) are importable, then re-exports
the FastAPI app for Vercel's Python runtime.
"""

import sys
from pathlib import Path

# Ensure the backend package is on the import path
backend_dir = str(Path(__file__).resolve().parent.parent / "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Re-export — Vercel auto-detects the `app` ASGI object
from main import app  # noqa: E402, F401
