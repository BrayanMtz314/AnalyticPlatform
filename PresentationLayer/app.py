import streamlit as st
import pandas as pd
from api.backend_client import api

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Sales Overview", 
    layout="wide"
)

genres = ['No genre','Rock','Jazz','Metal', 'Alternative & Punk','Rock And Roll','Blues','Latin','Reggae','Pop','Soundtrack','Bossa Nova','Easy Listening','Heavy Metal','R&B/Soul','Electronica/Dance','World','Hip Hop/Rap','Science Fiction','TV Shows','Sci Fi & Fantasy','Drama','Comedy','Alternative','Classical','Opera']

st.title("Analytics Dashboard")
st.markdown("Use the controls inside each section to fetch data. Updating one chart will **not** reload the others.")
st.divider()


# --- 2. CACHED API WRAPPERS ---
# We cache the data for 5 minutes (ttl=300). If a user requests the exact same 
# parameters within 5 minutes, Streamlit skips the API call and loads from memory.
@st.cache_data(ttl=300, show_spinner="Fetching tracks...")
def fetch_top_tracks(limit, genre = None):
    return pd.DataFrame(api.get_top_tracks(limit=limit, genre=genre))

@st.cache_data(ttl=300, show_spinner="Fetching trends...")
def fetch_sales_trend(year, granularity):
    return pd.DataFrame(api.get_sales_trend(year=year, granularity=granularity))

@st.cache_data(ttl=300, show_spinner="Fetching city data...")
def fetch_city_sales(min_revenue):
    return pd.DataFrame(api.get_sales_by_city(min_revenue=min_revenue))

@st.cache_data(ttl=300, show_spinner="Fetching genre data...")
def fetch_genre_market():
    return pd.DataFrame(api.get_genre_market_share())


@st.cache_data(ttl=300, show_spinner="Fetching customer data...")
def fetch_customer_history(customer_id):
    # This will return the JSON dict, or None if a 404 occurs
    return api.get_customer_purchase_history(customer_id)

# --- 3. DASHBOARD FRAGMENTS ---

@st.fragment
def top_tracks_fragment():
    st.subheader("Top Selling Tracks")
    st.markdown("Displays the tracks with the highest sales volume from the dataset; you can adjust the number of tracks using the slider.")
    
    col_ctrl, col_chart = st.columns([1, 3])
    
    with col_ctrl:
        # Using a form ensures the fragment only executes when the button is clicked,
        # rather than updating every time the slider moves.
        with st.form("form_tracks"):
            limit = st.slider("Top Tracks Limit", min_value=1, max_value=50, value=10)
            genre = st.selectbox("Filter by Genre", genres, index=0)
            st.form_submit_button("Fetch Data")
            
    with col_chart:
        try:
            df = fetch_top_tracks(limit, genre if genre != 'No genre' else None)
            if not df.empty:
                st.bar_chart(df.set_index("track_name")["total_revenue"], color="green")
            else:
                st.info("No track data available for these filters.")
        except Exception as e:
            st.error(f"API Error: {e}")
            
    st.divider()


@st.fragment
def sales_trend_fragment():
    st.subheader("Sales Trend")
    st.markdown("Displays sales throughout the year; you can toggle between month and quarter using the select box  .")
    
    col_ctrl, col_chart = st.columns([1, 3])
    
    with col_ctrl:
        with st.form("form_trends"):
            year = st.selectbox("Sales Year", [2021 + i for i in range(5)], index=0)
            granularity = st.selectbox("Time Granularity", ["month", "quarter"])
            st.form_submit_button("Fetch Data")
            
    with col_chart:
        try:
            df = fetch_sales_trend(year, granularity)
            if not df.empty:
                st.line_chart(df.set_index("period")["total_revenue"], color="red")
            else:
                st.info("No trend data available for this year.")
        except Exception as e:
            st.error(f"API Error: {e}")
            
    st.divider()


@st.fragment
def city_sales_fragment():
    st.subheader("Revenue by City")
    st.markdown("Displays revenue by city; you can filter using an amount in the numeric input field.")
    
    col_ctrl, col_chart = st.columns([1, 3])
    
    with col_ctrl:
        with st.form("form_cities"):
            min_revenue = st.number_input("Min City Revenue ($)", min_value=0.0, value=40.0, step=5.0)
            st.form_submit_button("Fetch Data")
            
    with col_chart:
        try:
            df = fetch_city_sales(min_revenue)
            if not df.empty:
                revenue_col = "total_revenue" if "total_revenue" in df.columns else "extended_amount"
                st.bar_chart(df.set_index("city")[revenue_col], color="blue")
            else:
                st.info("No cities meet the minimum revenue threshold.")
        except Exception as e:
            st.error(f"API Error: {e}")
            
    st.divider()


@st.fragment
def genre_market_fragment():
    st.subheader("Genre Market Share")
    st.markdown("It shows the relationships between the quantity sold and total revenue by genre. You can update the endpoint using the button.")
    
    # Even without inputs, wrapping in a fragment and form allows isolated manual refreshes
    with st.form("form_genres"):
        col1, col2 = st.columns([8, 1])
        with col2:
            st.form_submit_button("🔄 Refresh")
            
    try:
        df = fetch_genre_market()
        if not df.empty:
            qty_col = "quantity_sold" if "quantity_sold" in df.columns else "total_tracks_sold"
            rev_col = "total_revenue" if "total_revenue" in df.columns else "extended_amount"
            
            st.scatter_chart(
                df,
                x=qty_col,
                y=rev_col,
                color="genre_name" if "genre_name" in df.columns else None
            )
        else:
            st.info("No genre data available.")
    except Exception as e:
        st.error(f"API Error: {e}")
        
@st.fragment
def customer_history_fragment():
    st.subheader("Customer Purchase History Demo")
    st.markdown("Displays the customer's purchase history. You can select from users 1 to 4.    ")
    
    with st.form("form_customer"):
        # Demo selectbox limited to IDs 1, 2, 3, and 4
        customer_id = st.selectbox("Select Customer ID (Demo)", [1, 2, 3, 4])
        st.form_submit_button("Fetch Customer Data")
        

    try:
        customer_data = fetch_customer_history(customer_id)
        
        # Handle the 404 (None) case returned by your API client
        if customer_data is None:
            st.warning(f"No customer found with ID {customer_id}.")
        else:
            # Top row: Customer Info and Metrics
            info_col1, info_col2 = st.columns([2, 1])
            
            with info_col1:
                st.markdown(f"**Name:** {customer_data.get('customer_name', 'N/A')}")
                st.markdown(f"**Email:** {customer_data.get('email', 'N/A')}")
            
            with info_col2:
                # Format the lifetime value as currency
                ltv = customer_data.get('lifetime_value', 0)
                st.metric("Lifetime Value", f"${ltv:,.2f}")
            
            st.write("") # Add a little vertical spacing
            
            # Bottom row: Transactions Table
            transactions = customer_data.get("transactions", [])
            
            if transactions:
                st.markdown("**Transaction History**")
                df_trans = pd.DataFrame(transactions)
                
                # Streamlit's dataframe automatically makes this sortable and scrollable
                st.dataframe(df_trans, width='stretch', hide_index=True)
            else:
                st.info("No transactions found for this customer.")
                
    except Exception as e:
        st.error(f"API Error: {e}")
            
    st.divider()


# --- 4. RENDER THE FRAGMENTS ---
# Calling the functions here places them on the page. 
# Once loaded, they act completely independently of one another.
top_tracks_fragment()
sales_trend_fragment()
city_sales_fragment()
genre_market_fragment()
customer_history_fragment()