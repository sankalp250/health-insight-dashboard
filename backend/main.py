import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from app.services.data_service import (
    load_and_clean_data as service_load_and_clean_data,
    get_filtered_vaccine_data,
)

# Create the FastAPI application instance
app = FastAPI(
    title="Health Insight Dashboard API",
    description="An API for global COVID-19 vaccination data.",
    version="1.0.0",
)

# Configure CORS (Cross-Origin Resource Sharing)
# This allows our React frontend (on a different URL) to request data from this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, you should restrict this to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Loading and Cleaning ---
vaccine_df = None

@app.on_event("startup")
def load_and_clean_data():
    """
    This function runs when the API server starts.
    It loads the dataset and performs initial cleaning.
    """
    global vaccine_df
    try:
        # Warm the cache and store a copy for the root check
        df = service_load_and_clean_data()
        vaccine_df = df
        print("✅ Dataset loaded and cleaned successfully.")
    except Exception:
        print("❌ ERROR: Failed to load dataset via data service.")
        vaccine_df = pd.DataFrame()

# --- API Endpoints ---
@app.get("/")
def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"status": "ok", "message": "Welcome to the Health Insight Dashboard API"}

@app.get("/api/data-check")
def check_data_load():
    """Endpoint to verify that the dataset was loaded correctly."""
    df = service_load_and_clean_data()
    if df is not None and not df.empty:
        return {
            "status": "success",
            "rows_loaded": len(df),
            "columns": df.columns.tolist(),
            "data_head": df.head().to_dict(orient='records'),
        }
    return {"status": "error", "message": "Dataset could not be loaded."}