from pydantic import BaseModel

# --- Pydantic Model ---
class TopTrackResponse(BaseModel):
    track_name: str
    artist_name: str
    total_revenue: float

class SalesTrendResponse(BaseModel):
    period: str  # Will hold either the month name (e.g., "January") or quarter (e.g., "Q1")
    total_revenue: float

