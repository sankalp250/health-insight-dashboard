import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI app
app = FastAPI(
    title="Health Insight Dashboard API",
    description="API for vaccine market analytics.",
    version="1.0.0"
)

# Add CORS middleware to allow cross-origin requests from our frontend
# This is essential for the React app to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, we allow all. For production, lock this down.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Loading ---
# We load the data here once when the application starts.
# The @app.on_event("startup") decorator would be a more advanced way,
# but for simplicity, we'll load it directly into a global DataFrame.
try:
    vaccine_df = pd.read_csv("data/pharma_sales_data.csv")
    print("✅ Dataset loaded successfully!")
except FileNotFoundError:
    print("❌ Error: 'data/pharma_sales_data.csv' not found.")
    print("Please make sure the dataset is in the 'backend/data/' directory.")
    vaccine_df = pd.DataFrame() # Create an empty DataFrame if file not found


# --- API Endpoints ---
@app.get("/")
def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "Welcome to the Health Insight Dashboard API"}

@app.get("/api/data-check")
def check_data():
    """An endpoint to check if the data was loaded correctly."""
    if not vaccine_df.empty:
        return {
            "status": "success",
            "rows_loaded": len(vaccine_df),
            "columns": vaccine_df.columns.tolist()
        }
    return {"status": "error", "message": "Dataset could not be loaded."}