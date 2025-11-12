"""
AI service for natural language queries, predictions, and recommendations.
"""

from __future__ import annotations

import json
from typing import Any

import pandas as pd
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

from app.core.config import get_settings
from app.repositories.vaccine_repository import VaccineRepository


class AIService:
    """Service for AI-powered data analysis and recommendations."""

    def __init__(self, repository: VaccineRepository) -> None:
        self.repository = repository
        self.settings = get_settings()
        self.llm = None
        if self.settings.groq_api_key:
            self.llm = ChatGroq(
                groq_api_key=self.settings.groq_api_key,
                model_name="llama-3.1-70b-versatile",
                temperature=0.7,
            )

    def _get_context_data(self, filters: dict[str, Any] | None = None) -> str:
        """Extract relevant context from the dataset for RAG."""
        from app.models.vaccine import VaccineFilters

        vaccine_filters = VaccineFilters(
            region=filters.get("region") if filters else None,
            brand=filters.get("brand") if filters else None,
            year=filters.get("year") if filters else None,
        )

        df = self.repository.summary_metrics(vaccine_filters)
        if df.empty:
            return "No data available for the selected filters."

        context = []
        context.append(f"Total records: {len(df)}")
        context.append(f"Regions: {', '.join(df['region'].unique())}")
        context.append(f"Brands: {', '.join(df['brand'].unique())}")
        context.append(f"Years: {', '.join(map(str, sorted(df['year'].unique())))}")

        # Market size summary
        total_market = df["market_size_usd"].sum()
        avg_price = df["avg_price_usd"].mean()
        total_doses = df["doses_sold_million"].sum()
        context.append(f"Total Market Size: ${total_market:,.0f}")
        context.append(f"Average Price: ${avg_price:.2f}")
        context.append(f"Total Doses Sold: {total_doses:.2f} million")

        # Top brands
        top_brands = (
            df.groupby("brand")["market_size_usd"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
        )
        context.append("Top 5 Brands by Market Size:")
        for brand, size in top_brands.items():
            context.append(f"  - {brand}: ${size:,.0f}")

        # Regional insights
        regional_summary = (
            df.groupby("region")["market_size_usd"].sum().sort_values(ascending=False)
        )
        context.append("Market Size by Region:")
        for region, size in regional_summary.items():
            context.append(f"  - {region}: ${size:,.0f}")

        return "\n".join(context)

    async def chat_query(
        self, query: str, filters: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Process a natural language query about vaccine market data.

        Returns a response with answer and suggested visualizations.
        """
        if not self.llm:
            return {
                "answer": "AI features are not available. Please configure GROQ_API_KEY.",
                "visualization": None,
                "confidence": 0.0,
            }

        context = self._get_context_data(filters)

        system_prompt = """You are an expert data analyst specializing in vaccine market analytics.
Your role is to answer questions about vaccine market data in a clear, concise manner.
When answering:
1. Use specific numbers from the context when available
2. Suggest relevant visualizations (bar_chart, line_chart, pie_chart, table)
3. Provide actionable insights
4. If data is not available, clearly state that

Available visualization types: bar_chart, line_chart, pie_chart, table, none"""

        user_prompt = f"""Context Data:
{context}

User Question: {query}

Please provide:
1. A clear answer to the question
2. A suggested visualization type (one of: bar_chart, line_chart, pie_chart, table, none)
3. Brief reasoning for the visualization choice"""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]
            response = await self.llm.ainvoke(messages)

            # Parse response to extract answer and visualization suggestion
            content = response.content

            # Try to extract structured response
            visualization = "table"  # default
            if "bar_chart" in content.lower() or "bar" in content.lower():
                visualization = "bar_chart"
            elif "line_chart" in content.lower() or "line" in content.lower():
                visualization = "line_chart"
            elif "pie_chart" in content.lower() or "pie" in content.lower():
                visualization = "pie_chart"

            return {
                "answer": content,
                "visualization": visualization,
                "confidence": 0.85,
            }
        except Exception as e:
            return {
                "answer": f"I encountered an error processing your query: {str(e)}",
                "visualization": None,
                "confidence": 0.0,
            }

    async def get_predictions(
        self, filters: dict[str, Any] | None = None, years_ahead: int = 2
    ) -> dict[str, Any]:
        """
        Generate market predictions using simple trend analysis and AI insights.
        """
        from app.models.vaccine import VaccineFilters

        vaccine_filters = VaccineFilters(
            region=filters.get("region") if filters else None,
            brand=filters.get("brand") if filters else None,
        )

        df = self.repository.summary_metrics(vaccine_filters)
        if df.empty or len(df) < 2:
            return {
                "predictions": [],
                "confidence": 0.0,
                "method": "insufficient_data",
            }

        # Simple linear trend prediction
        df_sorted = df.sort_values("year")
        latest_year = df_sorted["year"].max()

        # Group by year for aggregate predictions
        yearly_data = (
            df_sorted.groupby("year")
            .agg(
                {
                    "market_size_usd": "sum",
                    "avg_price_usd": "mean",
                    "doses_sold_million": "sum",
                    "growth_rate_percent": "mean",
                }
            )
            .reset_index()
        )

        predictions = []
        for i in range(1, years_ahead + 1):
            future_year = latest_year + i

            # Simple linear extrapolation
            if len(yearly_data) >= 2:
                market_trend = (
                    yearly_data["market_size_usd"].iloc[-1]
                    - yearly_data["market_size_usd"].iloc[-2]
                ) / (yearly_data["year"].iloc[-1] - yearly_data["year"].iloc[-2])
                predicted_market = (
                    yearly_data["market_size_usd"].iloc[-1]
                    + market_trend * i
                )

                price_trend = (
                    yearly_data["avg_price_usd"].iloc[-1]
                    - yearly_data["avg_price_usd"].iloc[-2]
                ) / (yearly_data["year"].iloc[-1] - yearly_data["year"].iloc[-2])
                predicted_price = (
                    yearly_data["avg_price_usd"].iloc[-1] + price_trend * i
                )

                avg_growth = yearly_data["growth_rate_percent"].mean()
            else:
                predicted_market = yearly_data["market_size_usd"].iloc[-1]
                predicted_price = yearly_data["avg_price_usd"].iloc[-1]
                avg_growth = 0

            predictions.append(
                {
                    "year": future_year,
                    "predicted_market_size_usd": max(0, predicted_market),
                    "predicted_avg_price_usd": max(0, predicted_price),
                    "predicted_growth_rate_percent": avg_growth,
                    "confidence_interval_lower": predicted_market * 0.85,
                    "confidence_interval_upper": predicted_market * 1.15,
                }
            )

        # Get AI insight on predictions
        ai_insight = ""
        if self.llm:
            try:
                context = self._get_context_data(filters)
                prompt = f"""Based on this vaccine market data:
{context}

And these predictions for {years_ahead} years ahead:
{json.dumps(predictions, indent=2)}

Provide a brief (2-3 sentence) insight about the predicted market trends."""
                response = await self.llm.ainvoke([HumanMessage(content=prompt)])
                ai_insight = response.content
            except Exception:
                ai_insight = "AI analysis unavailable."

        return {
            "predictions": predictions,
            "confidence": 0.75,
            "method": "linear_extrapolation",
            "ai_insight": ai_insight,
        }

    async def get_recommendations(
        self, filters: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """
        Generate RAG-powered recommendations for data exploration.
        """
        if not self.llm:
            return [
                {
                    "title": "Explore by Region",
                    "description": "Filter data by different regions to compare market performance.",
                    "action": {"type": "filter", "field": "region"},
                }
            ]

        context = self._get_context_data(filters)

        prompt = f"""Based on this vaccine market data:
{context}

Generate 3-4 specific, actionable recommendations for exploring this data.
Each recommendation should:
1. Be specific and data-driven
2. Suggest a particular filter or analysis
3. Explain why it's interesting

Format as JSON array with: title, description, action (with type and field)"""

        try:
            response = await self.llm.ainvoke(
                [HumanMessage(content=prompt)]
            )
            content = response.content

            # Try to extract JSON from response
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                content = content[json_start:json_end].strip()
            elif "```" in content:
                json_start = content.find("```") + 3
                json_end = content.find("```", json_start)
                content = content[json_start:json_end].strip()

            recommendations = json.loads(content)
            if isinstance(recommendations, list):
                return recommendations
        except Exception:
            pass

        # Fallback recommendations
        return [
            {
                "title": "Compare Top Brands",
                "description": "Analyze market share differences between leading vaccine brands.",
                "action": {"type": "filter", "field": "brand"},
            },
            {
                "title": "Regional Performance",
                "description": "Explore how different regions compare in market size and growth.",
                "action": {"type": "filter", "field": "region"},
            },
            {
                "title": "Year-over-Year Trends",
                "description": "Examine how the market has evolved over time.",
                "action": {"type": "analysis", "type": "time_series"},
            },
        ]


def get_ai_service() -> AIService:
    """Get a singleton AI service instance."""
    from functools import lru_cache

    @lru_cache
    def _get_service() -> AIService:
        repository = VaccineRepository()
        return AIService(repository)

    return _get_service()

