"""
FastAPI application entrypoint for the Health Insight Dashboard backend.

This module follows the Application Factory pattern, allowing for better
testability and configuration management. The app is created through the
create_app() function which sets up middleware, routes, and configuration.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import ai, summary, vaccines
from app.core.config import get_settings


def create_app() -> FastAPI:
    """
    Application Factory Pattern: Creates and configures the FastAPI application.
    
    This pattern allows for:
    - Better testability (can create multiple app instances)
    - Cleaner configuration management
    - Easier dependency injection
    
    Returns:
        Configured FastAPI application instance
    """
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version=settings.app_version)

    # CORS Configuration: Enable cross-origin requests for frontend integration
    # In production, replace ["*"] with specific frontend domain(s) for security
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: Restrict to specific domains in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Route Registration: Modular routing keeps code organized and maintainable
    # Each router handles a specific domain (vaccines, summary, AI)
    app.include_router(vaccines.router)  # Core data endpoints
    app.include_router(summary.router)    # KPI aggregation endpoints
    app.include_router(ai.router)        # AI-powered endpoints

    @app.get("/", tags=["Root"])
    def root() -> dict[str, str]:
        """
        Root endpoint providing API metadata.
        
        Returns basic information about the API including version and
        links to documentation. Useful for API discovery and health monitoring.
        """
        return {
            "message": "Health Insight Dashboard API",
            "version": settings.app_version,
            "docs": "/docs",      # Swagger UI documentation
            "health": "/healthz",  # Health check endpoint
        }

    @app.get("/healthz", tags=["Health"])
    def health_check() -> dict[str, str]:
        """
        Health check endpoint for monitoring and load balancers.
        
        Kubernetes/Docker convention: /healthz endpoint used by orchestration
        tools to verify service availability. Returns 200 OK if service is running.
        """
        return {"status": "ok"}

    return app


app = create_app()


