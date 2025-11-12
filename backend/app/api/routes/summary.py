"""
Routes providing KPI summary data.
"""

from fastapi import APIRouter, Query

from app.api.schemas.vaccine import SummaryResponse, VaccineQueryParams
from app.models.vaccine import VaccineFilters
from app.services.vaccine_service import compute_summary

router = APIRouter(prefix="/api/summary", tags=["Summary"])


@router.get("", response_model=SummaryResponse)
def get_summary(
    region: str | None = Query(None, description="Filter KPIs by region."),
    brand: str | None = Query(None, description="Filter KPIs by vaccine brand."),
    year: int | None = Query(None, ge=1900, description="Filter KPIs by calendar year."),
) -> SummaryResponse:
    """Return KPI summary metrics for the selected filters."""
    filters = VaccineFilters(region=region, brand=brand, year=year)
    kpis = compute_summary(filters)
    applied = VaccineQueryParams(region=region, brand=brand, year=year)
    return SummaryResponse(kpis=kpis, filters_applied=applied)


