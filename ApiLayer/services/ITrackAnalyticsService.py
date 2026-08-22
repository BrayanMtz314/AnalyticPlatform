# services.py
from abc import ABC, abstractmethod
from typing import List, Optional
from schemas.AnalyticsSchemas import TopTrackResponse 

class ITrackAnalyticsService(ABC):
    @abstractmethod
    def get_top_tracks(self, limit: int, genre: Optional[str] = None) -> List[TopTrackResponse]:
        """Fetch the top performing tracks based on revenue."""
        pass