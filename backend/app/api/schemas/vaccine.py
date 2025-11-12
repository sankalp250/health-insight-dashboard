"""
API response schemas for vaccine data endpoints.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.vaccine import VaccineRecord


class VaccineQueryParams(BaseModel):
    """Query parameters accepted by the `/api/vaccines` endpoint."""

    region: Optional[str] = Field(None, description="Filter results by region.")
    brand: Optional[str] = Field(None, description="Filter results by brand.")
    year: Optional[int] = Field(None, description="Filter results by year.")
    limit: Optional[int] = Field(
        None, ge=1, le=500, description="Maximum number of records to return."
    )
    offset: Optional[int] = Field(
        0, ge=0, description="Number of records to skip before returning results."
    )


class VaccineListResponse(BaseModel):
    """Structured response for paginated vaccine data."""

    total: int = Field(..., ge=0, description="Total number of records matching filters.")
    returned: int = Field(
        ..., ge=0, description="Number of records returned in this response."
    )
    data: List[VaccineRecord] = Field(..., description="List of vaccine records.")


class SummaryKPI(BaseModel):
    """Represents a single KPI metric."""

    label: str = Field(..., description="Human-readable KPI label.")
    value: float = Field(..., description="Numeric KPI value.")
    unit: str | None = Field(None, description="Optional unit associated with the KPI.")
    description: str | None = Field(None, description="KPI contextual description.")


class SummaryResponse(BaseModel):
    """Payload returned by the `/api/summary` endpoint."""

    kpis: List[SummaryKPI] = Field(
        ..., description="Collection of key performance indicators."
    )
    filters_applied: VaccineQueryParams = Field(
        ..., description="Echo of filters that produced the summary."
    )


