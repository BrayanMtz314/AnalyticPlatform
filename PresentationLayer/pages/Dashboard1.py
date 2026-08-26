import streamlit as st
import pandas as pd
from api.backend_client import api

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Sales Overview", layout="wide")

st.title("📊 Interactive Analytics Dashboard")
st.markdown("---")

# --- 2. INTERACTIVE SIDEBAR CONTROLS ---
# Streamlit automatically places these widgets into the left-hand sidebar
st.sidebar.header("🎛️ Dashboard Filters")

limit = st.sidebar.slider("Top Tracks Limit", min_value=1, max_value=50, value=10)
year = st.sidebar.selectbox("Sales Year", [2024], index=0)
granularity = st.sidebar.selectbox("Time Granularity", ["month", "quarter"])
min_revenue = st.sidebar.number_input("Min City Revenue ($)", min_value=0.0, value=1.0, step=0.5)

# --- 3. DATA FETCHING ---
try:
    # Notice how we pass the dynamic widget variables directly into your API client
    top_tracks_data = api.get_top_tracks(limit=limit)
    sales_trend_data = api.get_sales_trend(year=year, granularity=granularity)
    city_sales_data = api.get_sales_by_city(min_revenue=min_revenue)
    genre_data = api.get_genre_market_share()

    # Convert to Pandas DataFrames for plotting
    df_top_tracks = pd.DataFrame(top_tracks_data)
    df_sales_trend = pd.DataFrame(sales_trend_data)
    df_city_sales = pd.DataFrame(city_sales_data)
    df_genre = pd.DataFrame(genre_data)



    # --- 4. DATA VISUALIZATION ---
    st.subheader("🏆 Top Selling Tracks")
    if not df_top_tracks.empty:
        # Setting the index to track_name puts the song titles on the X-axis
        st.bar_chart(df_top_tracks.set_index("track_name")["total_revenue"])
    else:
        st.info("No track data available for these filters.")

    st.subheader(f"📈 Sales Trend ({year})")
    if not df_sales_trend.empty:
        # Setting the index to period puts the months/quarters on the X-axis
        st.line_chart(df_sales_trend.set_index("period")["total_revenue"])
    else:
        st.info("No trend data available for this year.")


    st.subheader("🌍 Revenue by City")
    if not df_city_sales.empty:
        # We assume your Pydantic schema returns 'city' and 'extended_amount' (or 'total_revenue')
        revenue_col = "total_revenue" if "total_revenue" in df_city_sales.columns else "extended_amount"
        st.bar_chart(df_city_sales.set_index("city")[revenue_col])
    else:
        st.info("No cities meet the minimum revenue threshold.")

    st.subheader("🎸 Genre Market Share")
    if not df_genre.empty:
        # A scatter plot is perfect for comparing two metrics (quantity vs revenue)
        # Assuming your schema returns 'quantity', 'extended_amount', and 'genre_name'
        qty_col = "quantity_sold" if "quantity_sold" in df_genre.columns else "total_tracks_sold"
        rev_col = "total_revenue" if "total_revenue" in df_genre.columns else "extended_amount"
        
        st.scatter_chart(
            df_genre,
            x=qty_col,
            y=rev_col,
            color="genre_name" if "genre_name" in df_genre.columns else None
        )
    else:
        st.info("No genre data available.")

except Exception as e:
    st.error(f"Failed to fetch data from the API. Is your FastAPI server running? \n\nError: {e}")