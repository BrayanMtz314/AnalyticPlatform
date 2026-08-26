import os
import requests
from typing import List, Dict, Any, Optional

# Pull the base URL from the environment, defaulting to your local FastAPI server
API_BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000/api/analytics")

class AnalyticsClient:
    def __init__(self):
        # Using a session improves performance by reusing the underlying TCP connection
        self.session = requests.Session()

    def get_top_tracks(self, limit: int = 10, genre: Optional[str] = None) -> List[Dict[str, Any]]:
        url = f"{API_BASE_URL}/top-tracks"
        params = {"limit": limit}
        if genre:
            params["genre"] = genre
            
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_sales_trend(self, year: int, granularity: str = "month") -> List[Dict[str, Any]]:
        url = f"{API_BASE_URL}/sales-trend"
        params = {"year": year, "granularity": granularity}
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_sales_by_city(self, min_revenue: float = 0.0) -> List[Dict[str, Any]]:
        url = f"{API_BASE_URL}/sales-by-city"
        params = {"min_revenue": min_revenue}
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_genre_market_share(self) -> List[Dict[str, Any]]:
        url = f"{API_BASE_URL}/genre-market-share"
        
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_customer_purchase_history(self, customer_id: int) -> Optional[Dict[str, Any]]:
        url = f"{API_BASE_URL}/customers/{customer_id}/purchase-history"
        
        response = self.session.get(url)
        
        # Handle the specific 404 case gracefully so Streamlit can show a "User not found" message
        if response.status_code == 404:
            return None
            
        response.raise_for_status()
        return response.json()

# Instantiate a single client to be imported and used across all your Streamlit pages
api = AnalyticsClient()