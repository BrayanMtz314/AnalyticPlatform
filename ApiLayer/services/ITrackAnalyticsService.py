# services.py
from abc import ABC, abstractmethod
from typing import List, Optional, Literal
from schemas.AnalyticsSchemas import (
    TopTrackResponse, 
    SalesTrendResponse, 
    SalesbyCityResponse,
    genreMarketShareResponse,
    CustomerPurchaseHistoryResponse
    )

class ITrackAnalyticsService(ABC):
    @abstractmethod
    def get_top_tracks(self, limit: int, genre: Optional[str] = None) -> List[TopTrackResponse]:
        """Fetch the top performing tracks based on revenue."""
        pass

    @abstractmethod
    def get_sales_trend(self, year: int, granularity: Literal["month", "quarter"]) -> List[SalesTrendResponse]:
        """Fetch revenue trends aggregated by month or quarter for a specific year."""
        pass
    
    @abstractmethod
    def sales_by_city(self, min_revenue: float) -> List[SalesbyCityResponse]:
        """"Get the cities with the highest revenue and the customer count."""
        pass

    @abstractmethod
    def genre_market_share(self) -> List[genreMarketShareResponse]:
        """Get the genres with the hightest revenue and total of quantity sold"""
        pass
    
    @abstractmethod
    def get_customer_purchase_history(self, customer_id: int) -> Optional[CustomerPurchaseHistoryResponse]:
        """Fetch a specific customer's lifetime value and itemized transaction history."""
        pass