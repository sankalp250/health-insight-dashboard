# module: app.routes.vaccines
// ... existing code ...
from fastapi import APIRouter, Query
from typing import Optional
from app.services import data_service

# An APIRouter helps organize endpoints into groups
router = APIRouter()

@router.get("/api/vaccines")
async def get_vaccines_data(
    country: Optional[str] = Query(None, description="Filter by country name"),
    vaccine: Optional[str] = Query(None, description="Filter by vaccine brand name"),
    year: Optional[int] = Query(None, description="Filter by year"),
):
    """
    This endpoint returns vaccine data.
    It supports filtering by country, vaccine brand, and year.
    """
    return data_service.get_filtered_vaccine_data(country, vaccine, year)

@router.get("/api/filters")
async def get_filter_options():
    """
    This endpoint returns unique values for creating filter dropdowns on the frontend.
    """
    df = data_service.load_and_clean_data()
    if df is None or df.empty:
        return {"countries": [], "vaccines": [], "years": []}

    countries = sorted(df["country"].unique().tolist())
    # Explode to get a unique list of all vaccines across all entries
    all_vaccines = sorted(df.explode("vaccine_brand")["vaccine_brand"].unique().tolist())
    years = sorted(df["year"].unique().tolist())

    return {
        "countries": countries,
        "vaccines": all_vaccines,
        "years": years,
    }
// ... existing code ...