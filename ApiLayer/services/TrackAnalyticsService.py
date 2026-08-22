from collections import defaultdict
from services.ITrackAnalyticsService import ITrackAnalyticsService
from data.mockData import dim_track, fact_sales
from schemas.AnalyticsSchemas import TopTrackResponse
from typing import List, Optional

class TrackAnalyticsService(ITrackAnalyticsService):
    def get_top_tracks(self, limit: int, genre: Optional[str] = None) -> List[TopTrackResponse]:
        valid_tracks = {}
        for track in dim_track:
            if genre and track.get("genre_name").lower() != genre.lower():
                continue
            valid_tracks[track["track_id"]] = track

        revenue_by_track = defaultdict(float)
        for sale in fact_sales:
            track_id = sale["track_id"]
            if track_id in valid_tracks:
                revenue_by_track[track_id] += sale["extended_amount"]

        results = []
        for track_id, revenue in revenue_by_track.items():
            track_info = valid_tracks[track_id]
            results.append(TopTrackResponse(
                track_name=track_info["track_name"],
                artist_name=track_info["artist_name"],
                total_revenue=round(revenue, 2)
            ))

        results.sort(key=lambda x: x.total_revenue, reverse=True)
        return results[:limit]