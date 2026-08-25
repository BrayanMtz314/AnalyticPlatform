from pydantic import BaseModel
from typing import List

# --- Pydantic Model ---
class TopTrackResponse(BaseModel):
    track_name: str
    artist_name: str
    total_revenue: float

class SalesTrendResponse(BaseModel):
    period: str  
    total_revenue: float

class SalesbyCityResponse(BaseModel):
    country: str
    city: str
    total_revenue: float
    total_customers_in_city: int
    
    
class genreMarketShareResponse(BaseModel):
    genre_name: str
    quantity_sold: int
    total_revenue: float
    
class TransactionItem(BaseModel):
    track_name: str
    genre_name: str
    purchase_date: str
    price_paid: float

class CustomerPurchaseHistoryResponse(BaseModel):
    customer_name: str
    email: str
    lifetime_value: float
    transactions: List[TransactionItem]