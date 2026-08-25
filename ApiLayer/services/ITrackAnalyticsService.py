# services.py
from abc import ABC, abstractmethod
from typing import List, Optional, Literal
from schemas.AnalyticsSchemas import TopTrackResponse, SalesTrendResponse 

class ITrackAnalyticsService(ABC):
    @abstractmethod
    def get_top_tracks(self, limit: int, genre: Optional[str] = None) -> List[TopTrackResponse]:
        """Fetch the top performing tracks based on revenue."""
        pass

    @abstractmethod
    def get_sales_trend(self, year: int, granularity: Literal["month", "quarter"]) -> List[SalesTrendResponse]:
        """Fetch revenue trends aggregated by month or quarter for a specific year."""
        pass
