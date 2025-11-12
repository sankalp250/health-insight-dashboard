"""
Repository handling access to vaccine market data stored in CSV format.
"""

from __future__ import annotations

from typing import Iterable, Tuple

import pandas as pd

from app.core.config import get_settings
from app.models.vaccine import VaccineFilters, VaccineRecord


class VaccineRepository:
    """Provide filtered access to vaccine dataset records."""

    def __init__(self) -> None:
        self._settings = get_settings()
        self._df = self._load_dataset()

    def _load_dataset(self) -> pd.DataFrame:
        """Read the dataset from the configured CSV path."""
        data_file = self._settings.data_file
        if not data_file.exists():
            msg = f"Dataset file not found at {data_file}"
            raise FileNotFoundError(msg)

        df = pd.read_csv(data_file)
        # Normalize column names/types to expected schema.
        df.columns = [col.strip().lower() for col in df.columns]
        df["year"] = df["year"].astype(int)
        numeric_fields = [
            "market_size_usd",
            "avg_price_usd",
            "doses_sold_million",
            "growth_rate_percent",
        ]
        for field in numeric_fields:
            df[field] = pd.to_numeric(df[field], errors="coerce")

        df["region"] = df["region"].str.strip()
        df["brand"] = df["brand"].str.strip()
        df["insight"] = df["insight"].fillna("").astype(str)

        return df

    def _apply_filters(self, filters: VaccineFilters) -> pd.DataFrame:
        """Return dataframe filtered according to the provided filters."""
        df = self._df
        if filters.region:
            df = df[df["region"].str.lower() == filters.region.lower()]
        if filters.brand:
            df = df[df["brand"].str.lower() == filters.brand.lower()]
        if filters.year:
            df = df[df["year"] == filters.year]
        return df.sort_values(["region", "brand", "year"])

    def list_records(
        self, filters: VaccineFilters, limit: int | None = None, offset: int = 0
    ) -> Tuple[Iterable[VaccineRecord], int]:
        """
        Retrieve filtered vaccine records with optional pagination.

        Returns a tuple of (records, total_count).
        """
        filtered_df = self._apply_filters(filters)
        total = len(filtered_df)
        paginated_df = filtered_df.iloc[offset:]
        if limit is not None:
            paginated_df = paginated_df.iloc[:limit]

        records = [
            VaccineRecord(
                region=row["region"],
                brand=row["brand"],
                year=int(row["year"]),
                market_size_usd=float(row["market_size_usd"]),
                avg_price_usd=float(row["avg_price_usd"]),
                doses_sold_million=float(row["doses_sold_million"]),
                growth_rate_percent=float(row["growth_rate_percent"]),
                insight=row["insight"],
            )
            for row in paginated_df.to_dict(orient="records")
        ]

        return records, total

    def summary_metrics(self, filters: VaccineFilters) -> pd.DataFrame:
        """Return a dataframe limited to filtered rows for KPI calculations."""
        return self._apply_filters(filters)

    def distinct_regions(self) -> list[str]:
        """Return sorted list of available regions."""
        return sorted(self._df["region"].dropna().unique())

    def distinct_brands(self) -> list[str]:
        """Return sorted list of available brands."""
        return sorted(self._df["brand"].dropna().unique())

    def distinct_years(self) -> list[int]:
        """Return sorted list of available years."""
        return sorted(int(year) for year in self._df["year"].dropna().unique())


