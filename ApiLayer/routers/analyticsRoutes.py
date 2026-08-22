from fastapi import APIRouter, Query, Depends
from typing import List, Optional
from schemas.AnalyticsSchemas import TopTrackResponse
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