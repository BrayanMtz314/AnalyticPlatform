import pandas as pd
from typing import List, Optional, Literal
from services.ITrackAnalyticsService import ITrackAnalyticsService
from data.mockData import dim_track, fact_sales, dim_date, dim_customer
from schemas.AnalyticsSchemas import (
    TopTrackResponse, 
    SalesTrendResponse, 
    SalesbyCityResponse,
    genreMarketShareResponse,
    CustomerPurchaseHistoryResponse,
    TransactionItem
    ) 

class TrackAnalyticsService(ITrackAnalyticsService):
    def get_top_tracks(self, limit: int, genre: Optional[str] = None) -> List[TopTrackResponse]:
        # 1. Assign to a local variable to protect the global mock data
        df_track = dim_track
        
        # 2. Filter by genre if provided
        if genre:
            df_track = df_track[df_track['genre_name'].str.lower() == genre.lower()]

        # 3. Merge (Join) and Aggregate
        merged = pd.merge(fact_sales, df_track, on='track_id', how='inner')
        grouped = merged.groupby(['track_name', 'artist_name'], as_index=False)['extended_amount'].sum()

        # 4. Sort and Limit
        top_tracks = grouped.sort_values(by='extended_amount', ascending=False).head(limit)

        # 5. Convert back to Pydantic schemas
        return [
            TopTrackResponse(
                track_name=row['track_name'],
                artist_name=row['artist_name'],
                total_revenue=round(row['extended_amount'], 2)
            ) for row in top_tracks.to_dict(orient='records')
        ]

    def get_sales_trend(self, year: int, granularity: Literal["month", "quarter"]) -> List[SalesTrendResponse]:
        # 1. Assign to a local variable to protect the global mock data
        df_date = dim_date

        # 2. Filter dates by year
        df_date = df_date[df_date['year'] == year]

        # 3. Determine columns based on granularity
        period_col = "month_name" if granularity == "month" else "quarter"
        sort_col = "month_number" if granularity == "month" else "quarter"

        # 4. Merge (Join) and Aggregate
        merged = pd.merge(fact_sales, df_date, left_on='invoice_date_key', right_on='date_key', how='inner')
        grouped = merged.groupby([period_col, sort_col], as_index=False)['extended_amount'].sum()

        # 5. Sort chronologically
        trend_data = grouped.sort_values(by=sort_col)

        # 6. Convert back to Pydantic schemas
        return [    
            SalesTrendResponse(
                period=str(row[period_col]),
                total_revenue=round(row['extended_amount'], 2)
            ) for row in trend_data.to_dict(orient='records')
        ]
    
    
    def sales_by_city(self, min_revenue: float) -> List[SalesbyCityResponse]:
        
        # Merge (join) fact and customer, only the data we need
        merged = pd.merge(
            dim_customer[["customer_id", "city", "country"]], 
            fact_sales[["customer_id", "extended_amount"]], 
            how="inner", 
            on="customer_id"
        )
        
        aggregations = {
            'customer_id': 'nunique',  
            'extended_amount': 'sum'
        }
        
        result = merged.groupby(['country','city'], as_index=False).agg(aggregations)
        
        # Reassigned the filtered dataframe back to the variable
        result = result[result['extended_amount'] >= min_revenue]

        # Sort it to put the most valuable cities at the top
        result = result.sort_values(by='extended_amount', ascending=False)

        result.rename(columns={'customer_id': 'total_customers_in_city', 'extended_amount': 'total_revenue'}, inplace=True)
        
        return [
            SalesbyCityResponse(
                country = str(row['country']),
                city = str(row['city']),
                total_revenue = round(row['total_revenue'], 2),
                total_customers_in_city = int(row['total_customers_in_city'])
            ) for row in result.to_dict(orient='records')
        ]
        

    def genre_market_share(self) -> List[genreMarketShareResponse]:
        # Merge (join) fact and track, only the data we need
        merged = pd.merge(
            dim_track[["track_id", "genre_name"]], 
            fact_sales[["track_id", "quantity", "extended_amount"]], 
            how="inner", 
            on="track_id"
        )
        
        aggregations = {
            "quantity":"sum",
            "extended_amount":"sum"
        }
        
        results = merged.groupby('genre_name', as_index=False).agg(aggregations)
        
        results.rename(columns={'quantity': 'quantity_sold', 'extended_amount': 'total_revenue'}, inplace=True)
        
        results.sort_values(by='total_revenue', ascending=False, inplace=True)
        
        return [
            genreMarketShareResponse(
                genre_name = str(row['genre_name']),
                quantity_sold = int(row['quantity_sold']),
                total_revenue = round(row['total_revenue'], 2)
            ) for row in results.to_dict(orient='records')
        ]
        
    def get_customer_purchase_history(self, customer_id: int) -> Optional[CustomerPurchaseHistoryResponse]:
        # 1. Fetch the customer record directly
        df_cust = dim_customer[dim_customer['customer_id'] == customer_id]
        
        # If the customer ID does not exist in the database at all, return None
        if df_cust.empty:
            return None
            
        cust_name = df_cust.iloc[0].get('customer_full_name', 'Unknown')
        cust_email = df_cust.iloc[0].get('email', 'No Email')

        # 2. Filter sales down to just this single customer
        df_sales = fact_sales[fact_sales['customer_id'] == customer_id]
        
        # If they exist but haven't bought anything yet, return a clean 0 LTV profile
        if df_sales.empty:
            return CustomerPurchaseHistoryResponse(
                customer_name=cust_name,
                email=cust_email,
                lifetime_value=0.0,
                transactions=[]
            )

        # 3. Hub-and-Spoke Joins (Slicing columns to keep memory low)
        merged = pd.merge(df_sales, dim_track[['track_id', 'track_name', 'genre_name']], on='track_id', how='inner')
        merged = pd.merge(merged, dim_date[['date_key', 'full_date']], left_on='invoice_date_key', right_on='date_key', how='inner')

        # 4. Sort chronologically (newest purchases first)
        merged = merged.sort_values(by='full_date', ascending=False)

        # 5. Calculate overall Lifetime Value
        ltv = merged['extended_amount'].sum()

        # 6. Format nested transactions
        transactions = [
            TransactionItem(
                track_name=row['track_name'],
                genre_name=row['genre_name'],
                purchase_date=str(row['full_date']),
                price_paid=round(row['extended_amount'], 2)
            ) for _, row in merged.iterrows()
        ]

        return CustomerPurchaseHistoryResponse(
            customer_name=cust_name,
            email=cust_email,
            lifetime_value=round(ltv, 2),
            transactions=transactions
        )
    