"""
Routes for accessing vaccine market records.
"""

from fastapi import APIRouter, Query

from app.api.schemas.vaccine import VaccineListResponse
from app.models.vaccine import VaccineFilters
from app.services.vaccine_service import get_vaccine_records

router = APIRouter(prefix="/api/vaccines", tags=["Vaccines"])


@router.get("", response_model=VaccineListResponse)
def list_vaccines(
    region: str | None = Query(None, description="Filter by region."),
    brand: str | None = Query(None, description="Filter by vaccine brand."),
    year: int | None = Query(None, ge=1900, description="Filter by calendar year."),
    limit: int | None = Query(
        100, ge=1, le=500, description="Maximum number of records to return."
    ),
    offset: int = Query(0, ge=0, description="Number of records to skip."),
) -> VaccineListResponse:
    """Return filtered vaccine market records."""
    filters = VaccineFilters(region=region, brand=brand, year=year)
    records, total = get_vaccine_records(filters=filters, limit=limit, offset=offset)
    return VaccineListResponse(total=total, returned=len(records), data=records)


