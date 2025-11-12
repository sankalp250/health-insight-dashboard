"""
AI-powered endpoints for chat, predictions, and recommendations.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.services.ai_service import get_ai_service

router = APIRouter(prefix="/api/ai", tags=["AI"])


class ChatRequest(BaseModel):
    """Request model for chat queries."""

    query: str
    region: str | None = None
    brand: str | None = None
    year: int | None = None


class ChatResponse(BaseModel):
    """Response model for chat queries."""

    answer: str
    visualization: str | None
    confidence: float


class PredictionResponse(BaseModel):
    """Response model for predictions."""

    predictions: list[dict]
    confidence: float
    method: str
    ai_insight: str | None = None


class RecommendationItem(BaseModel):
    """Single recommendation item."""

    title: str
    description: str
    action: dict


@router.post("/chat", response_model=ChatResponse)
async def chat_with_data(request: ChatRequest) -> ChatResponse:
    """Process natural language queries about vaccine market data."""
    try:
        service = get_ai_service()
        filters = {}
        if request.region:
            filters["region"] = request.region
        if request.brand:
            filters["brand"] = request.brand
        if request.year:
            filters["year"] = request.year

        result = await service.chat_query(request.query, filters)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@router.get("/predictions", response_model=PredictionResponse)
async def get_predictions(
    region: str | None = Query(None, description="Filter by region"),
    brand: str | None = Query(None, description="Filter by brand"),
    years_ahead: int = Query(2, ge=1, le=5, description="Number of years to predict"),
) -> PredictionResponse:
    """Get market predictions based on historical trends."""
    try:
        service = get_ai_service()
        filters = {}
        if region:
            filters["region"] = region
        if brand:
            filters["brand"] = brand

        result = await service.get_predictions(filters, years_ahead)
        
        # Ensure we always return a valid response
        if not result:
            result = {
                "predictions": [],
                "confidence": 0.0,
                "method": "error",
                "ai_insight": "Unable to generate predictions. Please try different filters.",
            }
        
        return PredictionResponse(**result)
    except Exception as e:
        # Return a valid response even on error, don't raise HTTPException
        import traceback
        print(f"Error in predictions endpoint: {e}")
        print(traceback.format_exc())
        return PredictionResponse(
            predictions=[],
            confidence=0.0,
            method="error",
            ai_insight=f"Error generating predictions: {str(e)}",
        )


@router.get("/recommendations", response_model=list[RecommendationItem])
async def get_recommendations(
    region: str | None = Query(None, description="Filter by region"),
    brand: str | None = Query(None, description="Filter by brand"),
    year: int | None = Query(None, description="Filter by year"),
) -> list[RecommendationItem]:
    """Get AI-powered recommendations for data exploration."""
    try:
        service = get_ai_service()
        filters = {}
        if region:
            filters["region"] = region
        if brand:
            filters["brand"] = brand
        if year:
            filters["year"] = year

        recommendations = await service.get_recommendations(filters)
        return [RecommendationItem(**rec) for rec in recommendations]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating recommendations: {str(e)}"
        )

