"""
FastAPI application entrypoint for the Health Insight Dashboard backend.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import ai, summary, vaccines
from app.core.config import get_settings


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version=settings.app_version)

    # Enable CORS for local development and future frontends.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(vaccines.router)
    app.include_router(summary.router)
    app.include_router(ai.router)

    @app.get("/", tags=["Root"])
    def root() -> dict[str, str]:
        """Root endpoint."""
        return {
            "message": "Health Insight Dashboard API",
            "version": settings.app_version,
            "docs": "/docs",
            "health": "/healthz",
        }

    @app.get("/healthz", tags=["Health"])
    def health_check() -> dict[str, str]:
        """Simple health check endpoint."""
        return {"status": "ok"}

    return app


app = create_app()


