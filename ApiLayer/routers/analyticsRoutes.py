from fastapi import APIRouter, Query, Depends, Path, HTTPException
from typing import List, Optional, Literal
from dependencies.dependencies import get_track_analytics_service
from services.ITrackAnalyticsService import ITrackAnalyticsService
from schemas.AnalyticsSchemas import (
    SalesbyCityResponse, 
    TopTrackResponse, 
    SalesTrendResponse,
    genreMarketShareResponse,
    CustomerPurchaseHistoryResponse
    )

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

@router.get("/sales-by-city", response_model=List[SalesbyCityResponse])
def get_sales_by_city_endpoint(
    min_revenue: float = Query(0.0, description="Minimum revenue threshold for cities"),
    service: ITrackAnalyticsService = Depends(get_track_analytics_service)
):
    return service.sales_by_city(min_revenue=min_revenue)


@router.get("/genre-market-share", response_model=List[genreMarketShareResponse])
def get_genre_market_share_endpoint(
    service: ITrackAnalyticsService = Depends(get_track_analytics_service)
):
    return service.genre_market_share()

@router.get("/customers/{customer_id}/purchase-history", response_model=CustomerPurchaseHistoryResponse)
def get_customer_purchase_history_endpoint(
    customer_id: int = Path(..., description="The ID of the customer to lookup"),
    service: ITrackAnalyticsService = Depends(get_track_analytics_service)
):
    result = service.get_customer_purchase_history(customer_id=customer_id)
    
    if result is None:
        raise HTTPException(status_code=404, detail=f"Customer with ID {customer_id} not found.")
        
    return result
