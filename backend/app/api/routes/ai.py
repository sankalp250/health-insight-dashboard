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
    """
    Get market predictions based on historical trends.
    
    Error Handling Strategy: Graceful Degradation
    - Always returns 200 OK with valid response structure
    - Errors are included in response body, not HTTP status
    - This prevents frontend crashes and provides user-friendly messages
    
    Query Validation: FastAPI automatically validates:
    - years_ahead must be between 1 and 5 (ge=1, le=5)
    - Optional filters can be None
    """
    try:
        service = get_ai_service()
        
        # Filter Building: Only include provided filters
        filters = {}
        if region:
            filters["region"] = region
        if brand:
            filters["brand"] = brand

        result = await service.get_predictions(filters, years_ahead)
        
        # Defensive Programming: Ensure valid response structure
        if not result:
            result = {
                "predictions": [],
                "confidence": 0.0,
                "method": "error",
                "ai_insight": "Unable to generate predictions. Please try different filters.",
            }
        
        return PredictionResponse(**result)
    except Exception as e:
        # Graceful Error Handling: Return error in response, not HTTP exception
        # This ensures frontend always receives valid JSON structure
        import traceback
        print(f"Error in predictions endpoint: {e}")
        print(traceback.format_exc())  # Log full traceback for debugging
        
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

