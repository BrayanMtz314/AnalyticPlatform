import pandas as pd
from typing import List, Optional, Literal
from services.ITrackAnalyticsService import ITrackAnalyticsService
from data.mockData import dim_track, fact_sales, dim_date
from schemas.AnalyticsSchemas import TopTrackResponse, SalesTrendResponse

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