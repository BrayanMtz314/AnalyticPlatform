from fastapi import APIRouter, Query, Depends
from typing import List, Optional, Literal
from schemas.AnalyticsSchemas import TopTrackResponse, SalesTrendResponse
from dependencies.dependencies import get_track_analytics_service
from services.ITrackAnalyticsService import ITrackAnalyticsService

router = APIRouter()

@router.get("/top-tracks", response_model=List[TopTrackResponse])
def get_top_tracks_endpoint(
    limit: int = Query(10, ge=1),
    genre: Optional[str] = Query(None),
    service: ITrackAnalyticsService = Depends(get_track_analytics_service)
):
    return service.get_top_tracks(limit=limit, genre=genre)



@router.get("/sales-trend", response_model=List[SalesTrendResponse])
def get_sales_trend_endpoint(
    year: int = Query(..., description="The year to analyze, e.g., 2024"),
    granularity: Literal["month", "quarter"] = Query("month", description="Group by month or quarter"),
    service: ITrackAnalyticsService = Depends(get_track_analytics_service)
):
    return service.get_sales_trend(year=year, granularity=granularity)

