from services.ITrackAnalyticsService import ITrackAnalyticsService
from services.TrackAnalyticsService import TrackAnalyticsService

def get_track_analytics_service() -> ITrackAnalyticsService:
    # Later, if you need to pass a database session to the service, 
    # you can inject it here before returning the service instance.
    return TrackAnalyticsService()