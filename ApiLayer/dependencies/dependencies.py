# dependencies/dependencies.py
from fastapi import Depends
import snowflake.connector
from database import get_db_connection
from services.ITrackAnalyticsService import ITrackAnalyticsService
from services.SnowflakeTrackAnalyticsService import SnowflakeTrackAnalyticsService

"""
# You can use this dependency to use mock data for testing or development purposes. it works only for the TrackAnalyticsService class.
def get_track_analytics_service() -> ITrackAnalyticsService:
    # Later, if you need to pass a database session to the service, 
    # you can inject it here before returning the service instance.
    return TrackAnalyticsService() 
"""

def get_track_analytics_service(
    db_conn: snowflake.connector.SnowflakeConnection = Depends(get_db_connection)
) -> ITrackAnalyticsService:
    """
    Injects the database connection into the Snowflake service, 
    and returns the service mapped to the interface.
    """
    return SnowflakeTrackAnalyticsService(conn=db_conn)