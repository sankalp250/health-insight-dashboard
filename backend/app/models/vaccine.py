"""
Pydantic data models representing vaccine market records.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class VaccineRecord(BaseModel):
    """Domain model for a single vaccine record."""

    region: str = Field(..., description="Geographical region.")
    brand: str = Field(..., description="Vaccine manufacturer or brand.")
    year: int = Field(..., ge=1900, description="Calendar year of the record.")
    market_size_usd: float = Field(..., ge=0, description="Market size in USD.")
    avg_price_usd: float = Field(..., ge=0, description="Average price per dose in USD.")
    doses_sold_million: float = Field(
        ..., ge=0, description="Number of doses sold in millions."
    )
    growth_rate_percent: float = Field(
        ..., description="Year-over-year growth rate percentage."
    )
    insight: str = Field(..., description="Qualitative market insight.")


class VaccineFilters(BaseModel):
    """Supported query filters for vaccine records."""

    region: str | None = Field(None, description="Filter by region.")
    brand: str | None = Field(None, description="Filter by brand.")
    year: int | None = Field(None, description="Filter by calendar year.")


