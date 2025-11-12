"""
Service layer orchestrating vaccine data queries and KPI calculations.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Tuple

import pandas as pd

from app.api.schemas.vaccine import SummaryKPI
from app.models.vaccine import VaccineFilters, VaccineRecord
from app.repositories.vaccine_repository import VaccineRepository


@lru_cache
def get_vaccine_repository() -> VaccineRepository:
    """Instantiate a singleton repository instance."""
    return VaccineRepository()


def get_vaccine_records(
    filters: VaccineFilters, limit: int | None = None, offset: int = 0
) -> Tuple[list[VaccineRecord], int]:
    """Fetch vaccine records based on provided filters and pagination."""
    repository = get_vaccine_repository()
    records, total = repository.list_records(filters=filters, limit=limit, offset=offset)
    return list(records), total


def _calculate_cagr(df: pd.DataFrame) -> float:
    """Calculate Compound Annual Growth Rate based on market size."""
    if df.empty:
        return 0.0

    grouped = (
        df.groupby("year")
        .agg(total_market_size=("market_size_usd", "sum"))
        .sort_index()
    )

    if len(grouped) < 2:
        return 0.0

    first_year = grouped.index[0]
    last_year = grouped.index[-1]
    first_value = grouped.loc[first_year, "total_market_size"]
    last_value = grouped.loc[last_year, "total_market_size"]

    periods = last_year - first_year
    if periods <= 0 or first_value <= 0:
        return 0.0

    cagr = (last_value / first_value) ** (1 / periods) - 1
    return round(cagr * 100, 2)


def compute_summary(filters: VaccineFilters) -> list[SummaryKPI]:
    """Generate KPI summaries for the given filters."""
    repository = get_vaccine_repository()
    filtered_df = repository.summary_metrics(filters)

    if filtered_df.empty:
        return [
            SummaryKPI(
                label="Total Market Size",
                value=0.0,
                unit="USD",
                description="Sum of market size in USD for the selected filters.",
            ),
            SummaryKPI(
                label="Average Price",
                value=0.0,
                unit="USD",
                description="Average price per dose for the selected filters.",
            ),
            SummaryKPI(
                label="CAGR",
                value=0.0,
                unit="percent",
                description="Compound annual growth rate for the selected filters.",
            ),
        ]

    total_market_size = round(float(filtered_df["market_size_usd"].sum()), 2)
    average_price = round(float(filtered_df["avg_price_usd"].mean()), 2)
    total_doses = round(
        float(filtered_df["doses_sold_million"].sum()),
        2,
    )
    cagr = _calculate_cagr(filtered_df)

    return [
        SummaryKPI(
            label="Total Market Size",
            value=total_market_size,
            unit="USD",
            description="Sum of market size in USD for the selected filters.",
        ),
        SummaryKPI(
            label="Average Price",
            value=average_price,
            unit="USD",
            description="Average vaccine price per dose across the selection.",
        ),
        SummaryKPI(
            label="Total Doses Sold",
            value=total_doses,
            unit="million doses",
            description="Total doses sold (in millions) in the selected scope.",
        ),
        SummaryKPI(
            label="CAGR",
            value=cagr,
            unit="percent",
            description="Compound annual growth rate derived from total market size.",
        ),
    ]


