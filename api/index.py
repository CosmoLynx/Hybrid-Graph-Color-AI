"""
Vercel Serverless Function entry point.

Adds the backend directory to sys.path so that existing modules
(model.py, coloring.py, utils.py) are importable, then re-exports
the FastAPI app for Vercel's Python runtime.

A thin ASGI middleware strips the /api prefix so that FastAPI's
routes (/color-graph, /random-graph) match correctly.
"""

import sys
from pathlib import Path

# Ensure the backend package is on the import path
backend_dir = str(Path(__file__).resolve().parent.parent / "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from main import app as fastapi_app  # noqa: E402


class StripApiPrefix:
    """ASGI middleware that removes the /api prefix from the request path."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope.get("path", "")
            if path.startswith("/api"):
                scope = dict(scope)
                scope["path"] = path[4:] or "/"
        await self.app(scope, receive, send)


app = StripApiPrefix(fastapi_app)
