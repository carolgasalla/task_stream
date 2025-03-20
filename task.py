import streamlit as st
import pandas as pd


@st.cache_data
def load_data():
    df = pd.read_csv("airbnb.csv") 
    return df

data = load_data()


st.sidebar.header("Filters")
neighborhoods = st.sidebar.multiselect("Select Neighborhoods", data['neighborhood'].unique(), default=data['neighborhood'].unique())
listing_types = st.sidebar.multiselect("Select Listing Type", data['listing_type'].unique(), default=data['listing_type'].unique())

data_filtered = data[(data['neighborhood'].isin(neighborhoods)) & (data['listing_type'].isin(listing_types))]


tab1, tab2 = st.tabs(["Analysis", "Simulator"])


with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Listing Type vs Number of People")
        table1 = data_filtered.groupby('listing_type')['num_people'].describe()
        st.dataframe(table1)
    
    with col2:
        st.subheader("Price by Listing Type")
        table2 = data_filtered.groupby('listing_type')['price'].describe()
        st.dataframe(table2)
    
    st.subheader("Top Reviewed Apartments by Neighborhood")
    top_reviews = data_filtered.groupby(['neighborhood', 'listing_type']).agg({'reviews_per_month': 'sum'}).reset_index()
    st.dataframe(top_reviews)


with tab2:
    st.header("Price Recommendation Simulator")
    
   
    sim_neighborhood = st.selectbox("Select Neighborhood", data['neighborhood'].unique())
    sim_type = st.selectbox("Select Listing Type", data['listing_type'].unique())
    sim_people = st.slider("Number of People", 1, max(data['num_people']), 2)
    

    filtered_price = data[(data['neighborhood'] == sim_neighborhood) & (data['listing_type'] == sim_type)]
    recommended_price = filtered_price['price'].median() if not filtered_price.empty else "Not enough data"
    
    st.subheader(f"Recommended Price: ${recommended_price}")
