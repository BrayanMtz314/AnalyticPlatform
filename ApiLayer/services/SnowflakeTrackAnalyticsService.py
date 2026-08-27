# src/services/SnowflakeTrackAnalyticsService.py
import snowflake.connector
from snowflake.connector import DictCursor
from typing import List, Optional, Literal
from services.ITrackAnalyticsService import ITrackAnalyticsService
from schemas.AnalyticsSchemas import (
    TopTrackResponse, 
    SalesTrendResponse, 
    SalesbyCityResponse,
    genreMarketShareResponse,
    CustomerPurchaseHistoryResponse,
    TransactionItem
)

class SnowflakeTrackAnalyticsService(ITrackAnalyticsService):
    def __init__(self, conn: snowflake.connector.SnowflakeConnection):
        # We inject the Snowflake connection provided by our dependency generator
        self.conn = conn

    def get_top_tracks(self, limit: int, genre: Optional[str] = None) -> List[TopTrackResponse]:
        query = """
            SELECT t.TRACK_NAME, t.ARTIST_NAME, SUM(s.EXTENDED_AMOUNT) as TOTAL_REVENUE
            FROM FACT_SALES s
            JOIN DIM_TRACKS t ON s.TRACK_ID = t.TRACK_ID
            {genre_clause}
            GROUP BY t.TRACK_NAME, t.ARTIST_NAME
            ORDER BY TOTAL_REVENUE DESC
            LIMIT %(limit)s
        """
        params = {"limit": limit}
        genre_clause = ""
        
        if genre:
            genre_clause = "WHERE LOWER(t.GENRE_NAME) = LOWER(%(genre)s)"
            params["genre"] = genre

        with self.conn.cursor(DictCursor) as cur:
            # We use pyformat binding (%(param)s) to prevent SQL injection
            cur.execute(query.format(genre_clause=genre_clause), params)
            rows = cur.fetchall()

        return [
            TopTrackResponse(
                track_name=row['TRACK_NAME'],
                artist_name=row['ARTIST_NAME'],
                total_revenue=round(float(row['TOTAL_REVENUE']), 2)
            ) for row in rows
        ]

    def get_sales_trend(self, year: int, granularity: Literal["month", "quarter"]) -> List[SalesTrendResponse]:
        period_col = "MONTH_NAME" if granularity == "month" else "QUARTER"
        sort_col = "MONTH_NUMBER" if granularity == "month" else "QUARTER"
        
        query = f"""
            SELECT d.{period_col} as period, SUM(s.EXTENDED_AMOUNT) as TOTAL_REVENUE
            FROM FACT_SALES s
            JOIN DIM_DATES d ON s.INVOICE_DATE_KEY = d.DATE_KEY
            WHERE d.YEAR = %(year)s
            GROUP BY d.{period_col}, d.{sort_col}
            ORDER BY d.{sort_col}
        """
        
        with self.conn.cursor(DictCursor) as cur:
            cur.execute(query, {"year": year})
            rows = cur.fetchall()

        return [    
            SalesTrendResponse(
                period=str(row['PERIOD']),
                total_revenue=round(float(row['TOTAL_REVENUE']), 2)
            ) for row in rows
        ]

    def sales_by_city(self, min_revenue: float) -> List[SalesbyCityResponse]:
        query = """
            SELECT c.COUNTRY, c.CITY, 
                   COUNT(DISTINCT s.CUSTOMER_ID) as TOTAL_CUSTOMERS, 
                   SUM(s.EXTENDED_AMOUNT) as TOTAL_REVENUE
            FROM FACT_SALES s
            JOIN DIM_CUSTOMER c ON s.CUSTOMER_ID = c.CUSTOMER_ID
            GROUP BY c.COUNTRY, c.CITY
            HAVING SUM(s.EXTENDED_AMOUNT) >= %(min_revenue)s
            ORDER BY TOTAL_REVENUE DESC
        """
        
        with self.conn.cursor(DictCursor) as cur:
            cur.execute(query, {"min_revenue": min_revenue})
            rows = cur.fetchall()

        return [
            SalesbyCityResponse(
                country=str(row['COUNTRY']),
                city=str(row['CITY']),
                total_revenue=round(float(row['TOTAL_REVENUE']), 2),
                total_customers_in_city=int(row['TOTAL_CUSTOMERS'])
            ) for row in rows
        ]

    def genre_market_share(self) -> List[genreMarketShareResponse]:
        query = """
            SELECT t.GENRE_NAME, SUM(s.QUANTITY) as QUANTITY_SOLD, SUM(s.EXTENDED_AMOUNT) as TOTAL_REVENUE
            FROM FACT_SALES s
            JOIN DIM_TRACKS t ON s.TRACK_ID = t.TRACK_ID
            GROUP BY t.GENRE_NAME
            ORDER BY TOTAL_REVENUE DESC
        """
        
        with self.conn.cursor(DictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()

        return [
            genreMarketShareResponse(
                genre_name=str(row['GENRE_NAME']),
                quantity_sold=int(row['QUANTITY_SOLD']),
                total_revenue=round(float(row['TOTAL_REVENUE']), 2)
            ) for row in rows
        ]

    def get_customer_purchase_history(self, customer_id: int) -> Optional[CustomerPurchaseHistoryResponse]:
        with self.conn.cursor(DictCursor) as cur:
            # 1. Fetch customer details
            cur.execute("SELECT FULL_NAME, EMAIL FROM DIM_CUSTOMER WHERE CUSTOMER_ID = %(cust_id)s", {"cust_id": customer_id})
            cust_row = cur.fetchone()
            
            if not cust_row:
                return None
                
            cust_name = cust_row['FULL_NAME']
            cust_email = cust_row['EMAIL']

            # 2. Fetch transaction history 
            hist_query = """
                SELECT t.TRACK_NAME, t.GENRE_NAME, d.FULL_DATE as PURCHASE_DATE, s.EXTENDED_AMOUNT as PRICE_PAID
                FROM FACT_SALES s
                JOIN DIM_TRACKS t ON s.TRACK_ID = t.TRACK_ID
                JOIN DIM_DATES d ON s.INVOICE_DATE_KEY = d.DATE_KEY
                WHERE s.CUSTOMER_ID = %(cust_id)s
                ORDER BY d.FULL_DATE DESC
            """
            cur.execute(hist_query, {"cust_id": customer_id})
            transactions = cur.fetchall()

        # 3. Aggregate LTV and map
        ltv = sum(float(row['PRICE_PAID']) for row in transactions)
        
        return CustomerPurchaseHistoryResponse(
            customer_name=cust_name,
            email=cust_email,
            lifetime_value=round(ltv, 2),
            transactions=[
                TransactionItem(
                    track_name=row['TRACK_NAME'],
                    genre_name=row['GENRE_NAME'],
                    purchase_date=str(row['PURCHASE_DATE']),
                    price_paid=round(float(row['PRICE_PAID']), 2)
                ) for row in transactions
            ]
        )