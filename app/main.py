# module: app.main
// ... existing code ...
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import vaccines  # Import our new router

# Create the FastAPI application instance
app = FastAPI(
    title="Health Insight Dashboard API",
    description="An API for global COVID-19 vaccination data.",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routes from our vaccines module
app.include_router(vaccines.router)

# The data loading is now handled by the service, so no @app.on_event is needed here.

@app.get("/")
def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"status": "ok", "message": "Welcome to the new modular Health Insight Dashboard API!"}
// ... existing code ...