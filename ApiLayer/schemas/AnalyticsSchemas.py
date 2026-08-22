from pydantic import BaseModel

# --- Pydantic Model ---
class TopTrackResponse(BaseModel):
    track_name: str
    artist_name: str
    total_revenue: float