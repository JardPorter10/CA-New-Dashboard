import streamlit as st
import pandas as pd
from rapidfuzz import process

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Cleaned_FEU_Spot_Rate_Data.csv")
    return df

df = load_data()

# Extract unique origins and destinations
unique_origins = df["Qualifier_Description"].unique().tolist()
unique_destinations = df["Qualifier"].unique().tolist()

def get_best_match(query, choices):
    matches = process.extract(query, choices, limit=5, score_cutoff=50)
    return [match[0] for match in matches]

# Streamlit App
st.set_page_config(page_title="Container Atlas", layout="wide")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["My Dashboard", "Lane Dashboard", "Settings"])

if page == "Lane Dashboard":
    st.title("Lane Dashboard")
    
    # Search fields
    origin_query = st.text_input("Search Origin:")
    destination_query = st.text_input("Search Destination:")
    
    # Suggestions for origins
    if origin_query:
        suggested_origins = get_best_match(origin_query, unique_origins)
        selected_origin = st.selectbox("Select Origin", suggested_origins, index=0 if suggested_origins else None)
    else:
        selected_origin = None
    
    # Suggestions for destinations
    if destination_query:
        suggested_destinations = get_best_match(destination_query, unique_destinations)
        selected_destination = st.selectbox("Select Destination", suggested_destinations, index=0 if suggested_destinations else None)
    else:
        selected_destination = None
    
    # Filter data based on selection
    if selected_origin and selected_destination:
        filtered_df = df[(df["Qualifier_Description"] == selected_origin) & (df["Qualifier"] == selected_destination)]
        
        if not filtered_df.empty:
            st.success("Data loaded successfully!")
            st.dataframe(filtered_df)
        else:
            st.warning("No data found for the selected lane.")


